#!/usr/bin/env python3
"""Build branded Gumroad PDF from locked canonical content/.

Style: Register 4 wrapper + Register 2 body per MASTER_STYLE_GUIDE.md.
See Lingar-Archive/00-Master-Style-Guide/REGISTER_MAP.md
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
EXPORT = Path(__file__).resolve().parent
THEME = EXPORT / "gumroad-theme.css"
COVER = ROOT / "assets" / "cover.png"
OUT_DIR = Path(
    r"C:\Users\linga\Downloads\Books-Organized\10-Trauma-CPTSD-Content"
)
OUT_HTML = EXPORT / "gumroad-preview.html"
OUT_PDF = OUT_DIR / "rescue-boat-gumroad-v1.1.0.pdf"

GUMROAD_EDITION = "v1.1.0"
SOURCE_LOCK = "v1.1.0"
LOCK_DATE = "2026-06-19"

PART_BRIDGE_HTML = {
    "Part II — Technical Appendix": """
<section class="bridge-page">
  <h2>Before the Appendix</h2>
  <p>Part I gave you the counter-narratives — language for naming survival patterns without shame.</p>
  <p>The following sections contain additional tools and language for supporters and systems: science you can cite, reframes systems skip, and protocols you can hand to a peer worker, family member, or court support staff without forcing anyone to disclose trauma.</p>
  <div class="metaphor-box">The boat was never the enemy. Parts II–IV help you see the storm, name the alarm, and offer other vessels — not by shaming the old one, but by translating what the nervous system is actually doing.</div>
</section>
""",
    "Part IV — Resources": """
<section class="bridge-page">
  <h2>For Supporters and Systems</h2>
  <p>These resources are operational. They are meant to be used in parking lots, court hallways, supervision meetings, and kitchen tables — anywhere someone is being read as defiant when they are actually frozen.</p>
  <div class="metaphor-box">When someone freezes or reaches for their old boat, they are not choosing chaos — they are using the only vessel they were given when the alarm wouldn't turn off. Your job is not to sink the boat. It is to help them find other tools while the storm is still loud.</div>
  <p>Start with the freeze protocol if you work in legal or reentry contexts. Use the 26 Laws when you need plain-language pattern recognition. The harm-reduction and co-regulation notes are for anyone supporting someone still in the water.</p>
</section>
""",
}

STRUCTURE = [
    ("Part I — Counter-Narratives", [
        ("article_01.md", 1, "The Rescue Boat", "Addiction is survival, not weakness"),
        ("article_02.md", 2, "Shame Is the Glue", "Shame motivates hiding, not change"),
        ("article_03.md", 3, "Staying Stoic Is a Cage", "Stoicism is suffocation, not strength"),
        ("article_04.md", 4, "I Got Clean. I Didn't Get Free.", "Sobriety is the starting gate, not the finish line"),
        ("article_05.md", 5, "Translation Between the System and Trauma", "Freeze is not defiance. Consequences don't teach — they trigger."),
        ("article_06.md", 6, "Normal Is the Most Addictive State", "Addicts chase normal, not highs"),
        ("article_07.md", 7, "The Mirror Lies", "Shame distorts everything. Trust the data, not the feeling."),
        ("article_08.md", 8, "I Needed a Co-Regulator, Not a Savior", "Find a steady presence, not a rescuer"),
        ("article_09.md", 9, "You Can't Outrun Your Nervous System", "The fire follows you. You have to face it."),
        ("article_10.md", 10, "Healing Is a Spiral", "Setbacks are not resets."),
    ]),
    ("Part II — Technical Appendix", [
        ("appendix.md", None, "Deep Science and Reframes", "Citations, neurobiology, and the research behind the counter-narratives"),
    ]),
    ("Part III — Missing Pieces", [
        ("missing_pieces_overview.md", None, "What the System Leaves Out", "Tools and reframes traditional systems overlook"),
    ]),
    ("Part IV — Resources", [
        ("freeze_protocol.md", None, "Freeze Response Protocol for Courtrooms", "Operational reframes for legal support staff"),
        ("26_laws.md", None, "The 26 Laws of Survival", "Heuristic tools for pattern recognition"),
        ("harm_reduction.md", None, "Harm Reduction Note", "Regulation, not perfection"),
        ("co_regulation_barriers.md", None, "Co-Regulation Barriers & Low-Bar Alternatives", "Building scaffolds for connection"),
        ("15_defaults.md", None, "The 15 Core Defaults", "Rules of the system"),
    ]),
    ("About", [
        ("about_author.md", None, "About the Author", None),
    ]),
]


def strip_internal(text: str) -> str:
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    return text.strip()


def parse_article_body(raw: str) -> tuple[str, str | None, str]:
    """Return title, tagline, body markdown (without top heading/tagline)."""
    lines = raw.splitlines()
    title = ""
    tagline = None
    body_start = 0

    if lines and lines[0].startswith("# "):
        title = re.sub(r"^#\s*(ARTICLE\s+\d+:\s*)?", "", lines[0][2:], flags=re.I).strip()
        body_start = 1

    if body_start < len(lines) and lines[body_start].strip().startswith(">"):
        tagline = lines[body_start].strip().lstrip(">").strip()
        body_start += 1

    while body_start < len(lines) and not lines[body_start].strip():
        body_start += 1

    body = "\n".join(lines[body_start:])
    return title, tagline, body


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "smarty"],
    )


def build_html() -> str:
    css = THEME.read_text(encoding="utf-8")
    cover_uri = COVER.as_uri() if COVER.exists() else ""

    toc_parts: list[str] = []
    chapters: list[str] = []

    for part_name, items in STRUCTURE:
        toc_items = []
        for idx, (filename, num, title, subtitle) in enumerate(items):
            label = f"Article {num}" if num else title
            toc_items.append(f"<li><span>{label}</span> — {title}</li>")

            raw = strip_internal((CONTENT / filename).read_text(encoding="utf-8"))
            parsed_title, parsed_tagline, body_md = parse_article_body(raw)
            use_title = parsed_title or title
            use_tagline = parsed_tagline or subtitle

            num_html = (
                f'<div class="article-num">Article {num}</div>' if num else ""
            )
            tagline_html = (
                f'<p class="tagline">{use_tagline}</p>' if use_tagline else ""
            )

            is_part_open = idx == 0
            if is_part_open and part_name in PART_BRIDGE_HTML:
                chapters.append(PART_BRIDGE_HTML[part_name])

            part_class = "part-break" if is_part_open and part_name != "About" else ""
            part_label = (
                f'<div class="part-label">{part_name}</div>' if is_part_open else ""
            )
            chapters.append(
                f"""
<section class="chapter {part_class}">
  {part_label}
  {num_html}
  <h1>{use_title}</h1>
  {tagline_html}
  <div class="chapter-body">{md_to_html(body_md)}</div>
</section>
"""
            )

        toc_parts.append(
            f'<div class="toc-part">{part_name}</div><ol>{"".join(toc_items)}</ol>'
        )

    cover_img = (
        f'<img src="{cover_uri}" alt="The Rescue Boat cover" />'
        if cover_uri
        else '<div class="cover-mark">RB</div>'
    )

    how_to_raw = strip_internal((CONTENT / "how_to_use.md").read_text(encoding="utf-8"))
    _, _, how_to_body = parse_article_body(how_to_raw)
    how_to_html = md_to_html(how_to_body)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>The Rescue Boat &amp; Other Counter-Narratives — Gumroad Edition</title>
  <style>{css}</style>
</head>
<body>
  <section class="cover">
    {cover_img}
    <h1>The Rescue Boat<br>&amp; Other Counter-Narratives</h1>
    <p class="subtitle">When the alarm won't shut off, you reach for the nearest thing that keeps you afloat. This book names that pattern — and gives you language that doesn't require you to bleed for it.</p>
    <div class="cover-metaphor">
      <strong>The core metaphor</strong>
      The rescue boat is not the enemy. Addiction, freeze, avoidance, and shutdown are often survival responses — clumsy vessels launched in storms nobody asked about. This edition teaches the language. You decide what you share.
    </div>
    <p class="meta">Daniel Bret Lingar · Capitol Contracts LLC<br>daniel-lingar.github.io/rescue-boat</p>
    <div class="edition">Gumroad Edition {GUMROAD_EDITION} · Source lock {SOURCE_LOCK} ({LOCK_DATE})</div>
  </section>

  <section class="front-matter">
    <h2>Scope Boundary</h2>
    <div class="scope-box">
      <p><strong>Non-clinical public education.</strong> This manuscript is psychoeducation and lived-experience translation. It is <strong>not</strong> therapy, medical advice, legal advice, diagnosis, treatment, crisis care, or a substitute for licensed professional support.</p>
      <p>If you or someone you support is in immediate danger, contact local emergency services or a qualified crisis resource in your area.</p>
      <p><strong>This is not the full memoir.</strong> It is a focused counter-narrative edition — ten articles plus tools — drawn from lived experience without requiring disclosure.</p>
    </div>
    <div class="metaphor-box">You don't have to explain your whole storm to use this language. The boat is proof someone wanted to live. The work is finding other tools while the alarm is still loud.</div>
  </section>

  <section class="how-to-use">
    <h2>How to Use This Book</h2>
    <div class="how-to-body">{how_to_html}</div>
  </section>

  <section class="toc">
    <h2>Contents</h2>
    {''.join(toc_parts)}
  </section>

  {''.join(chapters)}

  <section class="back-matter">
    <h2>Edition &amp; Rights</h2>
    <p>Generated from the locked canonical source at <strong>github.com/daniel-lingar/rescue-boat</strong> (source {SOURCE_LOCK}, {LOCK_DATE}; Gumroad layout {GUMROAD_EDITION}).</p>
    <p>© Daniel Bret Lingar / Capitol Contracts LLC. Educational peer resource. Not therapy. No disclosure required.</p>
    <p>Contact: capitolcontracts@outlook.com</p>
    <div class="footer-line">The Rescue Boat &amp; Other Counter-Narratives · Gumroad Digital Edition {GUMROAD_EDITION}</div>
  </section>
</body>
</html>
"""


def find_edge() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("Edge or Chrome not found for PDF export")


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    browser = find_edge()
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(f"PDF export failed: {result.stderr or result.stdout}")
    if not pdf_path.exists():
        raise RuntimeError("PDF file was not created")


def main() -> int:
    html = build_html()
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"HTML: {OUT_HTML}")

    print_pdf(OUT_HTML, OUT_PDF)
    size_mb = OUT_PDF.stat().st_size / (1024 * 1024)
    print(f"PDF:  {OUT_PDF} ({size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())