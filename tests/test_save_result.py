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
    path.write_text("sentinel")          # overwrite with known content
    save_result(FAKE_RESULT, RUN_DATE, tmp_path)
    assert path.read_text() == "sentinel"  # proves the second call was a no-op


def test_empty_markdown_still_creates_file(tmp_path):
    result = {**FAKE_RESULT, "markdown": None}
    save_result(result, RUN_DATE, tmp_path)
    path = tmp_path / "2026-04-15-ir-chipotle-com-news-releases.md"
    assert path.exists()
    content = path.read_text()
    assert "url: https://ir.chipotle.com/news-releases" in content
