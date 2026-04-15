# Save Firecrawl Results to knowledge/raw/ Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `scrape_pipeline.py` to save each Firecrawl search result as a dated markdown file with YAML front matter in `knowledge/raw/`, skipping files that already exist.

**Architecture:** A `save_result()` helper function is added to `scrape_pipeline.py`. It derives a filename from the run date and URL slug, writes YAML front matter plus scraped markdown, and skips if the file already exists. The loop calls this helper for each result after `knowledge/raw/` is created.

**Tech Stack:** Python 3.12, pathlib, re, datetime (all stdlib)

---

### Task 1: Write and pass unit tests for `save_result()`

**Files:**
- Create: `tests/test_save_result.py`
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Create the tests file**

Create `tests/test_save_result.py` with the following content:

```python
import datetime
from pathlib import Path
import pytest
from scrape_pipeline import save_result

FAKE_RESULT = {
    "title": "News Releases - Chipotle Mexican Grill",
    "url": "https://ir.chipotle.com/news-releases",
    "markdown": "# News Releases\n\nSome content here.",
}

RUN_DATE = "2026-04-15"


def test_creates_file_with_correct_name(tmp_path):
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    expected = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    assert expected.exists()


def test_file_contains_front_matter(tmp_path):
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    path = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    content = path.read_text()
    assert "---" in content
    assert "title: News Releases - Chipotle Mexican Grill" in content
    assert "url: https://ir.chipotle.com/news-releases" in content
    assert f"scraped_at: {RUN_DATE}" in content


def test_file_contains_markdown_body(tmp_path):
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    path = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    content = path.read_text()
    assert "# News Releases" in content
    assert "Some content here." in content


def test_skips_existing_file(tmp_path):
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    path = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    original_mtime = path.stat().st_mtime

    # Call again — should not overwrite
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    assert path.stat().st_mtime == original_mtime


def test_empty_markdown_still_creates_file(tmp_path):
    result = {**FAKE_RESULT, "markdown": None}
    save_result(result, RUN_DATE, tmp_path)
    path = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    assert path.exists()
    content = path.read_text()
    assert "url: https://ir.chipotle.com/news-releases" in content
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
venv/bin/pytest tests/test_save_result.py -v
```

Expected: `ImportError` or `AttributeError` — `save_result` does not exist yet.

- [ ] **Step 3: Add `import datetime` and `save_result()` to `scrape_pipeline.py`**

Add `import datetime` to the imports at the top of `scrape_pipeline.py`:

```python
import datetime
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
import requests
```

Then add the `save_result` function before the `load_dotenv()` call (or after imports, before any script logic):

```python
def save_result(result, run_date, out_dir):
    slug = re.sub(r'[^a-z0-9]+', '-',
                  result['url'].lower()
                  .replace('https://', '')
                  .replace('http://', '')
                  ).strip('-')
    filename = f"{run_date}-{slug}.md"
    path = out_dir / filename

    if path.exists():
        print(f"  [skip] {filename} already exists")
        return

    front_matter = (
        f"---\n"
        f"title: {result.get('title', '')}\n"
        f"url: {result['url']}\n"
        f"scraped_at: {run_date}\n"
        f"---\n\n"
    )
    path.write_text(front_matter + (result.get('markdown') or ''))
    print(f"  [saved] {filename}")
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
venv/bin/pytest tests/test_save_result.py -v
```

Expected output:
```
tests/test_save_result.py::test_creates_file_with_correct_name PASSED
tests/test_save_result.py::test_file_contains_front_matter PASSED
tests/test_save_result.py::test_file_contains_markdown_body PASSED
tests/test_save_result.py::test_skips_existing_file PASSED
tests/test_save_result.py::test_empty_markdown_still_creates_file PASSED

5 passed
```

- [ ] **Step 5: Commit**

```bash
git add scrape_pipeline.py tests/test_save_result.py
git commit -m "feat: add save_result() with tests"
```

---

### Task 2: Wire `save_result()` into the pipeline loop

**Files:**
- Modify: `scrape_pipeline.py`

- [ ] **Step 1: Replace the existing print statements in the loop**

The current end of `scrape_pipeline.py` looks like:

```python
for r in results:
    print(f"  - {r['title']}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")
```

Replace it with:

```python
out_dir = Path("knowledge/raw")
out_dir.mkdir(parents=True, exist_ok=True)
run_date = datetime.date.today().isoformat()

for r in results:
    print(f"  - {r['title']}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")
    save_result(r, run_date, out_dir)
```

- [ ] **Step 2: Run the full pipeline and verify files are created**

```bash
venv/bin/python scrape_pipeline.py
```

Expected output includes lines like:
```
  [saved] 2026-04-15-ir-chipotle-com-news-releases.md
  [saved] 2026-04-15-newsroom-chipotle-com-press-releases.md
  ...
```

Then verify the files exist:

```bash
ls knowledge/raw/
```

Expected: 5 `.md` files, each starting with today's date.

Spot-check one file:

```bash
head -10 knowledge/raw/2026-04-15-ir-chipotle-com-news-releases.md
```

Expected:
```
---
title: News Releases - Chipotle Mexican Grill
url: https://ir.chipotle.com/news-releases
scraped_at: 2026-04-15
---
```

- [ ] **Step 3: Run the pipeline a second time to verify skip behavior**

```bash
venv/bin/python scrape_pipeline.py
```

Expected: all 5 lines say `[skip] ... already exists` — no files overwritten.

- [ ] **Step 4: Run tests one more time to confirm nothing broke**

```bash
venv/bin/pytest tests/test_save_result.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add scrape_pipeline.py
git commit -m "feat: save Firecrawl results to knowledge/raw/"
```
