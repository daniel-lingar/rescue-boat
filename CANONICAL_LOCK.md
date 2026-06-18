# CANONICAL LOCK — The Rescue Boat (Public Edition)

**Status:** LOCKED  
**Version:** 1.0.0  
**Locked:** 2026-06-18  
**Owner:** Daniel Bret Lingar / Capitol Contracts LLC  
**Repository:** https://github.com/daniel-lingar/rescue-boat  
**Live site:** https://daniel-lingar.github.io/rescue-boat/

---

## What Is Locked

This lock applies to the **10-article public counter-narrative edition** plus supporting appendix/resources. It does **not** include the long-form `book/` manuscript (separate work in progress).

| Layer | Role |
|-------|------|
| `content/` | **Canonical source** — edit here first |
| `client/src/content/` | SPA reader mirror |
| `client/public/content/` | Static/public mirror |
| `client/src/lib/articles.ts` | Article registry (10 counter-narratives) |
| `index.html` | Static hub (10-article index) |

---

## Article Manifest (Part I — Counter-Narratives)

| # | File | Title |
|---|------|-------|
| 1 | `article_01.md` | The Rescue Boat |
| 2 | `article_02.md` | Shame Is the Glue |
| 3 | `article_03.md` | Staying Stoic Is a Cage |
| 4 | `article_04.md` | I Got Clean. I Didn't Get Free. |
| 5 | `article_05.md` | Translation Between the System and Trauma *(merges former Art 5 + freeze/withdrawal)* |
| 6 | `article_06.md` | Normal Is the Most Addictive State |
| 7 | `article_07.md` | The Mirror Lies |
| 8 | `article_08.md` | I Needed a Co-Regulator, Not a Savior |
| 9 | `article_09.md` | You Can't Outrun Your Nervous System |
| 10 | `article_10.md` | Healing Is a Spiral |

**Retired in this lock:** `article_11.md`, `article_12.md` (content folded into Article 5 where applicable).

---

## Supporting Content (locked with edition)

- `appendix.md` — Part II Technical Appendix  
- `missing_pieces_overview.md` — Part III  
- `freeze_protocol.md`, `26_laws.md`, `harm_reduction.md`, `co_regulation_barriers.md`, `15_defaults.md` — Resources  
- `about_author.md`

---

## Case Study Integration

Lived examples pull from *From the Storm to the Fire* per:

- `C:\Users\linga\Documents\Lingar-Archive\02-Storm-Fire-Memoir\CASE_STUDY_INDEX.md`
- `CASE_STUDY_RULES.md`

Article 1 includes case study footer (CS-01, CS-05, CS-11). Expand footers in future unlocks only.

---

## Scope Boundary (unchanged)

Non-clinical public education. Not therapy, diagnosis, treatment, crisis care, medical advice, or legal advice.

---

## Unlock Policy

To change locked content:

1. Edit `content/` canonical files  
2. Run sync: copy `content/*.md` → `client/src/content/` and `client/public/content/`  
3. Update this file version + date + checksums  
4. Commit with `UNLOCK:` or `LOCK:` prefix in message  
5. Rebuild and verify live site

---

## File Checksums (SHA-256, canonical `content/`)

See `LOCK_CHECKSUMS.txt` generated at lock time.

---

*I already paid the tuition. You get the language.*