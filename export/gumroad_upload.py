#!/usr/bin/env python3
"""Update existing Gumroad product with Rescue Boat PDF (API or browser)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

PDF = Path(
    r"C:\Users\linga\Downloads\Books-Organized\10-Trauma-CPTSD-Content\rescue-boat-gumroad-v1.1.1.pdf"
)

PERMALINK = "ibctgw"
LIVE_URL = f"https://lingar.gumroad.com/l/{PERMALINK}"
EDIT_URL = f"https://app.gumroad.com/products/{PERMALINK}/edit"
PUBLIC_TITLE = "The Rescue Boat: Survival Doctrine."

DESCRIPTION = """Plain-language counter-narratives on trauma, addiction, shame, and freeze — for peers, families, helpers, and systems that keep misreading survival as defiance.

Ten counter-narratives plus a dual-audience reading guide, appendix, missing-pieces tools, and practical resources.

Includes: Start Here guide · 10 counter-narrative articles · Technical appendix · Missing pieces · Freeze protocol · 26 Laws · Harm reduction · Co-regulation barriers · 15 defaults

Digital edition v1.1.1 — cream, gold, and purple on near-black. Page numbers and edition footer on every page.

Non-clinical public education. Not therapy, diagnosis, treatment, or crisis care.

I already paid the tuition. You get the language."""


def find_product_by_permalink(token: str, permalink: str) -> dict | None:
    page = 1
    while True:
        resp = requests.get(
            "https://api.gumroad.com/v2/products",
            params={"access_token": token, "page": page},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        if not payload.get("success"):
            raise RuntimeError(payload)
        for product in payload.get("products", []):
            if product.get("custom_permalink") == permalink:
                return product
            short = product.get("short_url") or ""
            if permalink in short:
                return product
        if not payload.get("next_page_url"):
            break
        page += 1
    return None


def api_update(token: str, pdf: Path, permalink: str) -> dict:
    product = find_product_by_permalink(token, permalink)
    if not product:
        raise RuntimeError(f"product not found for permalink: {permalink}")

    product_id = product["id"]
    with pdf.open("rb") as handle:
        attach = requests.post(
            f"https://api.gumroad.com/v2/products/{product_id}/files",
            data={"access_token": token},
            files={"file": (pdf.name, handle, "application/pdf")},
            timeout=300,
        )
    attach.raise_for_status()
    result = attach.json()
    if not result.get("success"):
        raise RuntimeError(result)

    update = requests.put(
        f"https://api.gumroad.com/v2/products/{product_id}",
        data={
            "access_token": token,
            "description": DESCRIPTION,
            "published": "true",
        },
        timeout=120,
    )
    update.raise_for_status()
    updated = update.json()
    if not updated.get("success"):
        raise RuntimeError(updated)

    return updated["product"]


def wait_for_auth(page, timeout_s: float = 180.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        url = page.url.lower()
        if "login" not in url and "sign_in" not in url and "users/sign" not in url:
            if "/edit" in url or "/products" in url:
                return True
        time.sleep(3)
        page.goto(EDIT_URL, wait_until="domcontentloaded", timeout=60000)
    return False


def browser_update(pdf: Path, permalink: str, headless: bool = False) -> int:
    from playwright.sync_api import sync_playwright

    edit_url = f"https://app.gumroad.com/products/{permalink}/edit"
    edge_data = Path.home() / "AppData/Local/Microsoft/Edge/User Data"

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(edge_data),
            channel="msedge",
            headless=headless,
            args=["--profile-directory=Default"],
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(edit_url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(2)

        if not wait_for_auth(page):
            print("GUMROAD: login required at", page.url)
            print("Sign in to lingar Gumroad in the Edge window (up to 3 min)...")
            if not wait_for_auth(page, timeout_s=180.0):
                print("GUMROAD: timed out waiting for login", file=sys.stderr)
                context.close()
                return 1

        print(f"GUMROAD: on edit page — {page.url}")

        file_input = page.locator('input[type="file"]')
        if file_input.count() == 0:
            # Expand content / files section if collapsed
            for label in ("Content", "Files", "Add file", "Upload"):
                btn = page.get_by_text(label, exact=False)
                if btn.count():
                    btn.first.click(timeout=5000)
                    time.sleep(1)
                    break
            file_input = page.locator('input[type="file"]')

        if file_input.count() == 0:
            page.screenshot(path=str(Path(__file__).parent / "gumroad-edit-debug.png"))
            print("GUMROAD: file input not found — saved gumroad-edit-debug.png", file=sys.stderr)
            context.close()
            return 1

        file_input.first.set_input_files(str(pdf), timeout=180000)
        time.sleep(8)

        for save_label in ("Save and continue", "Save changes", "Publish", "Save"):
            save = page.get_by_role("button", name=save_label)
            if save.count():
                save.first.click(timeout=30000)
                time.sleep(4)
                break
            save = page.get_by_text(save_label, exact=False)
            if save.count():
                save.first.click(timeout=30000)
                time.sleep(4)
                break

        print(f"GUMROAD: file uploaded to {LIVE_URL}")
        context.close()
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--permalink", default=PERMALINK)
    parser.add_argument("--browser", action="store_true", help="Use Edge profile")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"PDF missing: {args.pdf}", file=sys.stderr)
        return 1

    token = os.environ.get("GUMROAD_ACCESS_TOKEN", "").strip()
    if token:
        product = api_update(token, args.pdf, args.permalink)
        print(
            json.dumps(
                {
                    "ok": True,
                    "product_id": product.get("id"),
                    "short_url": product.get("short_url"),
                    "live_url": LIVE_URL,
                    "file": args.pdf.name,
                },
                indent=2,
            )
        )
        return 0

    if args.browser:
        return browser_update(args.pdf, args.permalink, headless=args.headless)

    print("GUMROAD: set GUMROAD_ACCESS_TOKEN or pass --browser", file=sys.stderr)
    print(f"Product: {LIVE_URL}", file=sys.stderr)
    print(f"Edit:    {EDIT_URL}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())