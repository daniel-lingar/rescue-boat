#!/usr/bin/env python3
"""Attempt Gumroad product upload via API token or logged-in browser session."""

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
LISTING = Path(
    r"C:\Users\linga\Downloads\Books-Organized\10-Trauma-CPTSD-Content\rescue-boat-gumroad-listing.md"
)

TITLE = "The Rescue Boat & Other Counter-Narratives — Digital Edition (v1.1.1)"
PRICE_CENTS = 1800  # $18 mid-band
DESCRIPTION = """Plain-language counter-narratives on trauma, addiction, shame, and freeze — for peers, families, helpers, and systems that keep misreading survival as defiance.

Ten counter-narratives plus a dual-audience reading guide, appendix, missing-pieces tools, and practical resources — written for people who have been labeled weak, noncompliant, or broken when their nervous system was trying to survive.

Includes: Start Here guide · 10 counter-narrative articles · Technical appendix · Missing pieces · Freeze protocol · 26 Laws · Harm reduction · Co-regulation barriers · 15 defaults

Non-clinical public education. Not therapy, diagnosis, treatment, or crisis care.

I already paid the tuition. You get the language."""


def api_upload(token: str, pdf: Path) -> dict:
    """Create product and attach file via Gumroad API v2."""
    create = requests.post(
        "https://api.gumroad.com/v2/products",
        data={
            "access_token": token,
            "name": TITLE,
            "description": DESCRIPTION,
            "price": PRICE_CENTS,
            "published": "false",
            "custom_permalink": "rescue-boat-counter-narratives-v1-1-1",
        },
        timeout=120,
    )
    create.raise_for_status()
    product = create.json()
    if not product.get("success"):
        raise RuntimeError(product)

    product_id = product["product"]["id"]
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
    return product["product"]


def browser_upload(pdf: Path, headless: bool = False) -> int:
    from playwright.sync_api import sync_playwright

    edge_data = Path.home() / "AppData/Local/Microsoft/Edge/User Data"
    with sync_playwright() as p:
        if edge_data.is_dir():
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(edge_data),
                channel="msedge",
                headless=headless,
                args=["--profile-directory=Default"],
            )
        else:
            browser = p.chromium.launch(channel="msedge", headless=headless)
            context = browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://app.gumroad.com/products", wait_until="domcontentloaded", timeout=60000)
        time.sleep(3)
        url = page.url
        if "login" in url or "sign_in" in url or "users/sign" in url:
            print("GUMROAD: login required — complete sign-in in the browser window.")
            print("Waiting up to 180s for authenticated session...")
            for _ in range(36):
                time.sleep(5)
                page.goto("https://app.gumroad.com/products", wait_until="domcontentloaded")
                if "login" not in page.url and "sign_in" not in page.url:
                    break
            else:
                print("GUMROAD: timed out waiting for login", file=sys.stderr)
                context.close()
                return 1

        # New product flow
        new_btn = page.get_by_role("link", name="New product")
        if new_btn.count() == 0:
            new_btn = page.get_by_text("New product", exact=True)
        new_btn.first.click(timeout=15000)
        time.sleep(2)

        page.get_by_label("Name", exact=False).first.fill(TITLE, timeout=15000)
        desc = page.locator("textarea").first
        desc.fill(DESCRIPTION, timeout=15000)

        price = page.get_by_label("Price", exact=False)
        if price.count():
            price.first.fill("18", timeout=10000)

        file_input = page.locator('input[type="file"]').first
        file_input.set_input_files(str(pdf), timeout=120000)
        time.sleep(5)

        save = page.get_by_role("button", name="Save")
        if save.count() == 0:
            save = page.get_by_text("Save changes")
        save.first.click(timeout=30000)
        time.sleep(3)

        print(f"GUMROAD: product draft saved — {page.url}")
        context.close()
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--browser", action="store_true", help="Use Edge session")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"PDF missing: {args.pdf}", file=sys.stderr)
        return 1

    token = os.environ.get("GUMROAD_ACCESS_TOKEN", "").strip()
    if token:
        product = api_upload(token, args.pdf)
        print(json.dumps({"ok": True, "product_id": product.get("id"), "url": product.get("short_url")}, indent=2))
        return 0

    if args.browser:
        return browser_upload(args.pdf, headless=args.headless)

    print(
        "GUMROAD: set GUMROAD_ACCESS_TOKEN or pass --browser to use Edge login session.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())