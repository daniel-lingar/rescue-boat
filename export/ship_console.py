#!/usr/bin/env python3
"""Rescue Boat ship console — verify lock → footers → sync → PDF → Gumroad checklist."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = Path(__file__).resolve().parent
HUB = Path(r"C:\Users\linga\Hub")
OPPORTUNITIES = HUB / "config" / "opportunities.json"

PDF_DIRS = [
    Path(
        r"C:\Users\linga\Downloads_Organized\02_Writing_Projects\Books\Books-Organized\Books-Organized\10-Trauma-CPTSD-Content"
    ),
    Path(r"C:\Users\linga\Downloads\Books-Organized\10-Trauma-CPTSD-Content"),
]


def run_step(label: str, cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n== {label} ==")
    result = subprocess.run(cmd, cwd=cwd or ROOT, text=True)
    if result.returncode != 0:
        raise SystemExit(f"{label} failed (exit {result.returncode})")


def load_gumroad_opportunity() -> dict:
    if not OPPORTUNITIES.is_file():
        return {}
    data = json.loads(OPPORTUNITIES.read_text(encoding="utf-8"))
    for opp in data.get("opportunities", []):
        if opp.get("id") == "rescue-boat-gumroad":
            return opp
    return {}


def find_pdf(opp: dict) -> Path | None:
    asset = opp.get("asset")
    if asset:
        path = Path(asset)
        if path.is_file():
            return path
    edition = opp.get("edition", "v1.1.1").replace("v", "")
    for directory in PDF_DIRS:
        candidate = directory / f"rescue-boat-gumroad-v{edition}.pdf"
        if candidate.is_file():
            return candidate
    for directory in PDF_DIRS:
        matches = sorted(directory.glob("rescue-boat-gumroad-v*.pdf"), reverse=True)
        if matches:
            return matches[0]
    return None


def print_checklist(opp: dict, pdf_path: Path | None) -> None:
    print("\n" + "=" * 60)
    print("GUMROAD SHIP CHECKLIST")
    print("=" * 60)
    if pdf_path and pdf_path.is_file():
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        print(f"PDF:     {pdf_path} ({size_mb:.1f} MB)")
    else:
        print("PDF:     NOT FOUND — run without --skip-pdf")
    listing = opp.get("listing_copy")
    if listing and Path(listing).is_file():
        print(f"Listing: {listing}")
    print(f"Edition: {opp.get('edition_label', opp.get('edition', 'see product_lock'))}")
    print(f"Action:  {opp.get('next_action', 'Upload at app.gumroad.com/products')}")
    if opp.get("blocker"):
        print(f"Blocker: {opp['blocker']}")
    print("\nManual steps:")
    print("  1. Log in at https://app.gumroad.com/products")
    print("  2. New product → Digital product → upload PDF only")
    print("  3. Paste title/description from listing_copy file")
    print("  4. Suggested tags: trauma, CPTSD, addiction, shame, freeze response")
    print("  5. Mark opportunity shipped in Hub after publish")
    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-footers", action="store_true")
    parser.add_argument("--skip-sync", action="store_true")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--skip-hub", action="store_true", help="Skip Hub refresh")
    parser.add_argument("--build-pdf", action="store_true", help="Force PDF rebuild")
    args = parser.parse_args()

    print("RESCUE BOAT SHIP CONSOLE")
    print(f"Repo: {ROOT}")

    run_step("Lock verify", [sys.executable, str(EXPORT / "verify_lock.py")])

    if not args.skip_footers:
        run_step(
            "Case study footers",
            [sys.executable, str(EXPORT / "case_study_footers.py"), "--validate"],
        )

    if not args.skip_sync:
        sync_ps1 = ROOT / "scripts" / "sync-content.ps1"
        if sync_ps1.is_file():
            run_step("Sync mirrors", ["pwsh", "-File", str(sync_ps1)])
        else:
            print("\n== Sync mirrors == (skipped — script missing)")

    if args.build_pdf or not args.skip_pdf:
        run_step("Gumroad PDF", [sys.executable, str(EXPORT / "build_gumroad_pdf.py")])

    if not args.skip_hub and (HUB / "scripts" / "refresh.py").is_file():
        run_step("Hub refresh", [sys.executable, str(HUB / "scripts" / "refresh.py")])

    opp = load_gumroad_opportunity()
    pdf_path = find_pdf(opp)
    print_checklist(opp, pdf_path)

    print("\nSHIP CONSOLE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())