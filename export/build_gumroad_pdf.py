#!/usr/bin/env python3
"""Build branded Gumroad PDF from locked canonical content/."""

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
OUT_PDF = OUT_DIR / "rescue-boat-gumroad-v1.0.0.pdf"

EDITION = "v1.0.0"
LOCK_DATE = "2026-06-18"

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
    <p class="subtitle">Plain-language counter-narratives on trauma, addiction, shame, freeze, and survival — for peers, families, helpers, and systems that need better translation.</p>
    <p class="meta">Daniel Bret Lingar · Capitol Contracts LLC<br>daniel-lingar.github.io/rescue-boat</p>
    <div class="edition">Canonical Edition {EDITION} · Locked {LOCK_DATE}</div>
  </section>

  <section class="front-matter">
    <h2>Scope Boundary</h2>
    <div class="scope-box">
      <p><strong>Non-clinical public education.</strong> This manuscript is psychoeducation and lived-experience translation. It is <strong>not</strong> therapy, medical advice, legal advice, diagnosis, treatment, crisis care, or a substitute for licensed professional support.</p>
      <p>If you or someone you support is in immediate danger, contact local emergency services or a qualified crisis resource in your area.</p>
      <p><strong>Audience:</strong> survivors and peers, families and supporters, peer workers, legal and reentry support staff, and clinicians who want plain-language translation tools — without forcing disclosure or replacing clinical care.</p>
    </div>
    <h2>How to Read This Edition</h2>
    <p><strong>Part I</strong> delivers ten counter-narratives that challenge shame-and-blame interpretations of trauma, addiction, freeze, and avoidance.</p>
    <p><strong>Part II</strong> provides supporting science and citations in plain language.</p>
    <p><strong>Part III</strong> names tools and reframes systems often overlook.</p>
    <p><strong>Part IV</strong> offers practical protocols and heuristic resources.</p>
    <p style="color: var(--gold-soft); font-style: italic; margin-top: 1.5rem;">I already paid the tuition. You get the language.</p>
  </section>

  <section class="toc">
    <h2>Contents</h2>
    {''.join(toc_parts)}
  </section>

  {''.join(chapters)}

  <section class="back-matter">
    <h2>Edition &amp; Rights</h2>
    <p>Generated from the locked canonical source at <strong>github.com/daniel-lingar/rescue-boat</strong> ({EDITION}, {LOCK_DATE}).</p>
    <p>© Daniel Bret Lingar / Capitol Contracts LLC. Educational peer resource. Not therapy. No disclosure required.</p>
    <p>Contact: capitolcontracts@outlook.com</p>
    <div class="footer-line">The Rescue Boat &amp; Other Counter-Narratives · Gumroad Digital Edition {EDITION}</div>
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