#!/usr/bin/env python3
"""Generate and validate Storm-to-Fire case study footers on Rescue Boat articles."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DEFAULT_INDEX = Path(
    r"C:\Users\linga\Documents\Lingar-Archive\02-Storm-Fire-Memoir\CASE_STUDY_INDEX.md"
)

FOOTER_START = re.compile(r"<!--\s*\nCASE STUDY — From the Storm to the Fire", re.M)
FOOTER_BLOCK = re.compile(
    r"<!--\s*\nCASE STUDY — From the Storm to the Fire[\s\S]*?-->",
    re.M,
)

# Canonical footers (curated; may compress index scene map for public articles)
CANONICAL_FOOTERS: dict[int, dict[str, str]] = {
    1: {
        "scene": "CS-01 Glass Box · CS-05 Hydrocodone Dishes · CS-11 I Chose Not to Die",
        "teaches": "Substances as rescue boat — survival regulation, not moral failure",
        "memoir": "Part I Ch 1–3 · Part II Ch 4",
        "wrh": "S09 The Loop",
        "laws": "#3 Dangerous shelter · #14 Gas pedal sticks",
        "field_line": "I wasn't choosing drugs over my family. I was choosing not to die.",
        "ownership": "It hurt them. It hurt me. I own what the boat cost.",
    },
    2: {
        "scene": "CS-09 Closets & Erasure · CS-16 Trinity Spiral",
        "teaches": "Shame glues survival behavior — hiding is regulation, not character",
        "memoir": "Part II Ch 4 · Ch 8",
        "wrh": "S07 Disappearing Act · S05 Mask · S09 Loop",
        "laws": "#7 Learned to disappear · #15 Shame is glue",
        "field_line": "My presence felt like something to hide.",
        "ownership": "I erased myself to keep peace. That wasn't love — it was survival.",
    },
    3: {
        "scene": "CS-09 Closets & Erasure · CS-13 Garrett's Loss",
        "teaches": "Stoicism as cage — grief blocked, emotions suffocated",
        "memoir": "Part II Ch 4 · Ch 6",
        "wrh": "S07 Disappearing Act · S06 Crash",
        "laws": "#7 Learned to disappear · #4 What you couldn't mourn haunts you",
        "field_line": "Grief isn't a wave. It's a tide.",
        "ownership": "I didn't wake him. I carry that non-decision every day.",
    },
    4: {
        "scene": "CS-15 Burning in Cold Places",
        "teaches": "Sobriety without regulation — clean not free, performance until miss cue",
        "memoir": "Part II Ch 8",
        "wrh": "S06 Crash · S13 Threshold",
        "laws": "#17 Exhaustion warning light",
        "field_line": "Getting clean gave me a chance. It didn't give me peace.",
        "ownership": "People loved the performance until I missed a cue.",
    },
    5: {
        "scene": "CS-06 System Betrayal · CS-12 Mom Collapse · CS-00 Predictive Model",
        "teaches": "Freeze is not defiance — systems punish shutdown as noncompliance",
        "memoir": "Part I Prologue · Part II Ch 5",
        "wrh": "S14 Fight/Flight/Freeze · S29 System Optimization",
        "laws": "#9 Stop when can't fight/run · #11 System that should help hurts again",
        "field_line": "Punishment didn't wake me up. It shut me down harder.",
        "ownership": "Mom was on the floor. I couldn't move. That failure lives in me.",
    },
    6: {
        "scene": "CS-05 Hydrocodone Dishes",
        "teaches": "Normal is the addictive state — relief mistaken for moral victory",
        "memoir": "Part I Ch 2–3",
        "wrh": "S06 Crash · S09 Loop",
        "laws": "#3 Dangerous shelter · #14 Gas pedal sticks",
        "field_line": "Normal was the drug.",
        "ownership": "I performed normal while my kids watched the mask slip.",
    },
    7: {
        "scene": "CS-10 Two-Minute Therapy · CS-00b Preface Wiring",
        "teaches": "Shame distorts the mirror — misdiagnosis becomes identity",
        "memoir": "Part I Preface · Part II Ch 4",
        "wrh": "S00 Intro · S20 Constructed Self",
        "laws": "#6 Broken mirror · #15 Shame is glue",
        "field_line": "It's not what's wrong with you. It's what happened to you.",
        "ownership": "I turned the knife on myself for years. The labels weren't all mine.",
    },
    8: {
        "scene": "CS-27 Connection",
        "teaches": "Co-regulation vs savior — steady presence, not rescue",
        "memoir": "Part VI Ch 19",
        "wrh": "S24 Stable Contact",
        "laws": "#23 Need others",
        "field_line": "I needed a co-regulator, not a savior.",
        "ownership": "I reached for rescuers when I needed scaffolds. The wreckage was still real.",
    },
    9: {
        "scene": "CS-14 North Dakota · CS-19 Echoes and Amplifiers",
        "teaches": "Geographic escape fails — the nervous system follows the storm",
        "memoir": "Part II Ch 7 · Part III Ch 11",
        "wrh": "S05 Mask · S02 Blueprint",
        "laws": "#5 Work as war · #8 Scan every room",
        "field_line": "I kept changing scenery but brought the storm with me.",
        "ownership": "I couldn't say no. I broke anyway.",
    },
    10: {
        "scene": "CS-20 60 Reflections · CS-28 Ongoing Path",
        "teaches": "Healing is spiral — setbacks are data, not moral resets",
        "memoir": "Part III Ch 12 · Part VI Ch 20",
        "wrh": "S23 Pattern Veto · S26 Accountability",
        "laws": "#22 Spiral recovery · #25 Write next chapter",
        "field_line": "Recovery isn't straight. It's a spiral with better tools.",
        "ownership": "Accountability isn't self-flagellation. It's looking at the wreckage.",
    },
}


def _strip_md(value: str) -> str:
    value = value.strip()
    if value.startswith("*") and value.endswith("*"):
        value = value.strip("*").strip()
    value = value.replace("*", "")
    return value.strip()


def parse_scene_map(index_text: str) -> dict[int, list[str]]:
    match = re.search(
        r"## Rescue Boat Articles[^\n]*\n+([\s\S]*?)(?:\n---\n|\n## )",
        index_text,
    )
    if not match:
        raise ValueError("Rescue Boat scene map not found in CASE_STUDY_INDEX.md")
    block = match.group(1)
    mapping: dict[int, list[str]] = {}
    for line in block.splitlines():
        match = re.match(r"^\|\s*(\d+)\s+.+?\|\s*(.+?)\s*\|", line)
        if not match:
            continue
        num = int(match.group(1))
        raw_ids = match.group(2)
        ids: list[str] = []
        for token in re.split(r"[·,]", raw_ids):
            token = token.strip()
            token = re.sub(r"\s*\(.*$", "", token)
            if re.match(r"^CS-", token):
                ids.append(token)
        if ids:
            mapping[num] = ids
    return mapping


def parse_scene_entries(index_text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}

    for match in re.finditer(r"^### (CS-[\w-]+) — (.+)$", index_text, re.M):
        scene_id = match.group(1)
        short_title = match.group(2).strip()
        block = index_text[match.end() : match.end() + 1200]
        fields: dict[str, str] = {"title": short_title}
        for row in re.finditer(r"\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|", block):
            key = row.group(1).strip()
            val = _strip_md(row.group(2))
            fields[key] = val
        entries[scene_id] = fields

    compact = index_text.split("| Scene ID | Memoir | Teaches | WRH | Ownership line |", 1)
    if len(compact) == 2:
        for row in re.finditer(
            r"^\|\s*(CS-\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
            compact[1],
            re.M,
        ):
            scene_id = row.group(1).strip()
            entries.setdefault(scene_id, {})
            entries[scene_id].update(
                {
                    "title": entries[scene_id].get("title", scene_id),
                    "Memoir": row.group(2).strip(),
                    "Mechanism": row.group(3).strip(),
                    "WRH": row.group(4).strip(),
                    "Ownership": _strip_md(row.group(5)),
                }
            )

    return entries


def scene_label(scene_id: str, entries: dict[str, dict[str, str]]) -> str:
    title = entries.get(scene_id, {}).get("title", scene_id)
    return f"{scene_id} {title}"


def combine_wrh(scene_ids: list[str], entries: dict[str, dict[str, str]]) -> str:
    parts: list[str] = []
    seen: set[str] = set()
    for sid in scene_ids:
        raw = entries.get(sid, {}).get("WRH", "")
        for token in re.split(r"[·,]", raw):
            token = token.strip()
            if token and token not in seen:
                seen.add(token)
                parts.append(token)
    return " · ".join(parts)


def combine_laws(scene_ids: list[str], entries: dict[str, dict[str, str]]) -> str:
    parts: list[str] = []
    seen: set[str] = set()
    for sid in scene_ids:
        raw = entries.get(sid, {}).get("26 Laws", "")
        for token in re.split(r"[·,]", raw):
            token = token.strip()
            if token and token not in seen:
                seen.add(token)
                parts.append(token)
    return " · ".join(parts)


def build_footer(article_num: int) -> str:
    data = CANONICAL_FOOTERS[article_num]
    return (
        "<!--\n"
        "CASE STUDY — From the Storm to the Fire\n"
        f"Scene: {data['scene']}\n"
        f"Teaches: {data['teaches']}\n"
        f"Memoir: {data['memoir']}\n"
        f"WRH: {data['wrh']}\n"
        f"26 Laws: {data['laws']}\n"
        f'Field line: "{data["field_line"]}"\n'
        "Note: Example from author lived experience. Not required disclosure for participants.\n"
        f"Ownership: {data['ownership']}\n"
        "-->"
    )


def build_footer_from_index(
    article_num: int,
    scene_ids: list[str],
    entries: dict[str, dict[str, str]],
) -> str:
    """Draft footer from CASE_STUDY_INDEX (use --from-index to apply)."""
    labels = [scene_label(sid, entries) for sid in scene_ids]
    primary = scene_ids[-1]
    primary_entry = entries.get(primary, {})
    field_line = _strip_md(primary_entry.get("Field line", ""))
    ownership = _strip_md(primary_entry.get("Ownership", ""))
    teaches = primary_entry.get("Mechanism", CANONICAL_FOOTERS[article_num]["teaches"])

    return (
        "<!--\n"
        "CASE STUDY — From the Storm to the Fire\n"
        f"Scene: {' · '.join(labels)}\n"
        f"Teaches: {teaches}\n"
        f"Memoir: {primary_entry.get('Memoir', '')}\n"
        f"WRH: {combine_wrh(scene_ids, entries)}\n"
        f"26 Laws: {combine_laws(scene_ids, entries)}\n"
        f'Field line: "{field_line}"\n'
        "Note: Example from author lived experience. Not required disclosure for participants.\n"
        f"Ownership: {ownership}\n"
        "-->"
    )


def article_path(num: int) -> Path:
    return CONTENT / f"article_{num:02d}.md"


def extract_footer(text: str) -> str | None:
    match = FOOTER_BLOCK.search(text)
    return match.group(0) if match else None


def normalize_footer(block: str) -> str:
    lines = [line.rstrip() for line in block.strip().splitlines()]
    return "\n".join(lines)


def load_index(path: Path) -> tuple[dict[int, list[str]], dict[str, dict[str, str]]]:
    text = path.read_text(encoding="utf-8")
    return parse_scene_map(text), parse_scene_entries(text)


def validate(index_path: Path, check_index: bool = False) -> list[str]:
    scene_map, _entries = load_index(index_path)
    errors: list[str] = []
    for num in range(1, 11):
        path = article_path(num)
        if not path.is_file():
            errors.append(f"missing article: {path.name}")
            continue
        text = path.read_text(encoding="utf-8")
        existing = extract_footer(text)
        if not existing:
            errors.append(f"no footer: article_{num:02d}.md")
            continue
        expected = build_footer(num)
        if normalize_footer(existing) != normalize_footer(expected):
            errors.append(f"footer mismatch: article_{num:02d}.md (run --apply to refresh)")
        if check_index and num in scene_map:
            scene_line = CANONICAL_FOOTERS[num]["scene"]
            for sid in scene_map[num]:
                if sid not in scene_line:
                    errors.append(
                        f"index drift: article_{num:02d}.md missing {sid} from scene map"
                    )
    return errors


def apply(index_path: Path, force: bool = False, from_index: bool = False) -> list[str]:
    scene_map, entries = load_index(index_path)
    changed: list[str] = []
    for num in range(1, 11):
        path = article_path(num)
        if from_index and num in scene_map:
            footer = build_footer_from_index(num, scene_map[num], entries)
        else:
            footer = build_footer(num)
        text = path.read_text(encoding="utf-8")
        existing = extract_footer(text)
        if existing:
            if not force and normalize_footer(existing) == normalize_footer(footer):
                continue
            text = FOOTER_BLOCK.sub(footer, text, count=1)
        else:
            text = text.rstrip() + "\n\n---\n\n" + footer + "\n"
        path.write_text(text, encoding="utf-8")
        changed.append(path.name)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--validate", action="store_true", help="Check footers against index")
    parser.add_argument("--apply", action="store_true", help="Write missing footers")
    parser.add_argument("--force", action="store_true", help="Replace existing footers")
    parser.add_argument(
        "--from-index",
        action="store_true",
        help="Draft footers from CASE_STUDY_INDEX (not canonical curated)",
    )
    parser.add_argument(
        "--check-index",
        action="store_true",
        help="Warn when canonical footers omit index scene IDs",
    )
    parser.add_argument("--print", type=int, metavar="N", help="Print footer for article N")
    args = parser.parse_args()

    if not args.index.is_file():
        print(f"CASE STUDY FOOTERS: index not found — {args.index}", file=sys.stderr)
        return 1

    if args.print:
        num = args.print
        if args.from_index:
            scene_map, entries = load_index(args.index)
            print(build_footer_from_index(num, scene_map[num], entries))
        else:
            print(build_footer(num))
        return 0

    if args.apply:
        changed = apply(args.index, force=args.force, from_index=args.from_index)
        if changed:
            print(f"CASE STUDY FOOTERS: applied ({len(changed)} files)")
            for name in changed:
                print(f"  - {name}")
        else:
            print("CASE STUDY FOOTERS: nothing to apply")
        return 0

    errors = validate(args.index, check_index=args.check_index)
    if errors:
        print("CASE STUDY FOOTERS: FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("CASE STUDY FOOTERS: OK (10 articles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())