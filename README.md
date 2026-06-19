# The Rescue Boat & Other Counter-Narratives

A public education and counter-narrative manuscript site exploring trauma, addiction, nervous-system adaptation, shame, freeze responses, and survival patterns in plain language.

## Canonical Lock (v1.1.2)

The **10-article public edition** is locked as of **2026-06-19**. See [`CANONICAL_LOCK.md`](CANONICAL_LOCK.md) and [`LOCK_CHECKSUMS.txt`](LOCK_CHECKSUMS.txt).

| Rule | Detail |
| :--- | :--- |
| **Canonical source** | Edit `content/` first, then run `scripts/sync-content.ps1` |
| **Edition scope** | `how_to_use.md` + 10 counter-narratives + appendix, missing pieces, and resources |
| **Out of scope** | `book/` long-form manuscript (separate work in progress) |
| **Gumroad PDF** | `python export/build_gumroad_pdf.py` → `rescue-boat-gumroad-v1.1.1.pdf` |
| **Verify lock** | `python export/verify_lock.py` |
| **Unlock** | Follow the unlock policy in `CANONICAL_LOCK.md` |

## Overview

**The Rescue Boat** is a digital manuscript and educational platform designed to translate survival patterns that are often mislabeled as defiance, weakness, noncompliance, laziness, or character failure.

Instead of forcing disclosure or diagnosis, this project offers language: a way to recognize how the nervous system, shame, avoidance, addiction, collapse, and survival behavior can operate under pressure.

The site is built as a high-performance, single-page application (SPA) optimized for reading and accessibility. It serves as the public article and manuscript hub for the WRH counter-narrative work.

## Live Site

The manuscript is live and can be accessed at:
[https://daniel-lingar.github.io/rescue-boat/](https://daniel-lingar.github.io/rescue-boat/)

Source repository:
[https://github.com/daniel-lingar/rescue-boat](https://github.com/daniel-lingar/rescue-boat)

## Content Structure

The manuscript is organized into four key sections:

| Section | Title | Description |
| :--- | :--- | :--- |
| **Part I** | The Counter-Narratives | Ten core articles challenging shame-and-blame interpretations of trauma, addiction, freeze, and avoidance. |
| **Part II** | Technical Appendix | Plain-language science, nervous-system concepts, and supporting references. |
| **Part III** | Missing Pieces | Tools and reframes often overlooked by traditional recovery, legal, and support systems. |
| **Part IV** | Resources | Practical protocols, the "26 Laws of Survival," and harm-reduction-oriented notes. |

## Purpose & Audience

This is a **non-clinical public education** site. It is intended for:

- **Survivors & Peers:** To provide language for naming and understanding survival patterns.
- **Families & Supporters:** To help reframe behavior without excusing harm or removing accountability.
- **Peer Workers & Helpers:** To offer plain-language tools for recognizing freeze, shame, avoidance, and collapse.
- **Legal and Reentry Support Staff:** To provide operational reframes for missed appointments, shutdown, and avoidant noncompliance patterns.
- **Clinicians & Providers:** To offer plain-language translation tools that may support communication, while remaining outside clinical treatment.

## Scope Boundary

This project is not therapy, medical advice, legal advice, diagnosis, treatment, crisis care, or a substitute for licensed professional support. It is public-facing psychoeducation and lived-experience translation.

If a reader is in immediate danger or crisis, they should contact local emergency services, trusted support, or a qualified crisis resource in their area.

## Development & Deployment

### Tech Stack

- **Framework:** React 19 with Vite
- **Styling:** Tailwind CSS
- **Routing:** Wouter (configured for GitHub Pages sub-paths)
- **Content:** Markdown-based article system

### Build Instructions

To run the project locally or build for production, ensure you have `pnpm` installed:

1.  **Install Dependencies:**
    ```bash
    pnpm install
    ```

2.  **Local Development:**
    ```bash
    pnpm run dev
    ```

3.  **Build for Production:**
    ```bash
    pnpm run build
    ```
    *Note: The build process automatically generates the `404.html` required for GitHub Pages routing.*

4.  **Type Check:**
    ```bash
    pnpm run check
    ```

### Deployment

The site is deployed to GitHub Pages. The build output in `dist/public` is designed to be served from the `/rescue-boat/` base path. Routing for direct article links is handled via a custom `404.html` redirection script.

---
*This repository serves as the public article and manuscript hub for The Rescue Boat counter-narrative project.*
