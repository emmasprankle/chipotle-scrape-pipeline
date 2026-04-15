# Design: Save Firecrawl Search Results to knowledge/raw/

## Overview

Extend `scrape_pipeline.py` to persist each Firecrawl search result as a markdown file in `knowledge/raw/`. Files include a YAML front matter header and the raw scraped markdown body. Existing files are skipped.

## File Naming

- Capture `run_date = datetime.date.today().isoformat()` once at the start of the script (e.g. `"2026-04-15"`).
- Derive a slug from each result URL: strip the scheme (`https://`), lowercase, replace all non-alphanumeric characters with `-`, collapse repeated dashes, strip leading/trailing dashes.
- Final filename pattern: `knowledge/raw/{run_date}-{url-slug}.md`
- Example: `2026-04-15-ir-chipotle-com-news-releases.md`

## File Content

Each file is written as:

```markdown
---
title: <result title>
url: <result url>
scraped_at: <run_date>
---

<raw markdown from Firecrawl>
```

If `markdown` is absent or empty, the body below the front matter is empty. The file is still written so the URL visit is recorded.

## Implementation

### `save_result(result, run_date, out_dir)` helper

Added to `scrape_pipeline.py` above the main loop.

- Derives slug and constructs the file path.
- If the file already exists: prints `[skip] <filename>` and returns early.
- Otherwise: writes front matter + markdown body, prints `[saved] <filename>`.

### Loop integration

Before the loop:
- `out_dir = Path("knowledge/raw")` — created with `mkdir(parents=True, exist_ok=True)`.
- `run_date = datetime.date.today().isoformat()` — captured once.

Inside the loop:
- Call `save_result(r, run_date, out_dir)` for each result.

### Imports

Add `import datetime` at the top of the script. `re` and `Path` are already imported.

## Constraints

- No new files — all logic stays in `scrape_pipeline.py`.
- Skip (do not overwrite) files that already exist for the same date + URL.
