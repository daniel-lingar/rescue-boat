#!/usr/bin/env python3
"""Verify content/ SHA-256 hashes against LOCK_CHECKSUMS.txt."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
CHECKSUMS = ROOT / "LOCK_CHECKSUMS.txt"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_checksums() -> dict[str, str]:
    expected: dict[str, str] = {}
    for line in CHECKSUMS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([a-f0-9]{64})\s{2}(.+)$", line)
        if match:
            expected[match.group(2)] = match.group(1)
    return expected


def main() -> int:
    expected = parse_checksums()
    errors: list[str] = []

    for name, want in sorted(expected.items()):
        path = CONTENT / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        got = file_hash(path)
        if got != want:
            errors.append(f"mismatch: {name}")

    for path in sorted(CONTENT.glob("*.md")):
        if path.name not in expected:
            errors.append(f"untracked in LOCK_CHECKSUMS.txt: {path.name}")

    if errors:
        print("LOCK VERIFY: FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"LOCK VERIFY: OK ({len(expected)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())