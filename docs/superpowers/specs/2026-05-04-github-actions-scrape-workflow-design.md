# Design: GitHub Actions Scheduled Scrape Workflow

## Overview

Add a GitHub Actions workflow that runs `scrape_pipeline.py` on a weekly schedule and auto-commits any new `knowledge/raw/` files back to `main`. A manual trigger is also provided for on-demand runs.

## Trigger

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'   # Mondays at 9 AM UTC
  workflow_dispatch:        # manual trigger from GitHub UI
```

Weekly cadence matches Chipotle's press release frequency. `workflow_dispatch` allows ad-hoc runs (e.g. around earnings).

## Job: `scrape`

Runner: `ubuntu-latest`. Single job, no matrix.

### Permissions

```yaml
permissions:
  contents: write
```

Uses the built-in `GITHUB_TOKEN` to push back to the repo. No personal access token required.

### Steps

1. **Checkout** — `actions/checkout@v4`
2. **Set up Python** — `actions/setup-python@v5`, version `3.11`
3. **Install dependencies** — `pip install -r requirements.txt`
4. **Run scrape** — `python scrape_pipeline.py`
   - `FIRECRAWL_API_KEY` injected from GitHub Secrets as an environment variable
5. **Commit and push** — inline shell script:
   - Configure git user as `github-actions[bot]`
   - Check `git status --porcelain knowledge/raw/`
   - If no new files: print "No new files" and exit 0
   - If new files: `git add knowledge/raw/`, commit with message `chore: weekly scrape <YYYY-MM-DD>`, push to `main`

## Secrets

| Secret name         | Purpose                        | Where to add              |
|---------------------|--------------------------------|---------------------------|
| `FIRECRAWL_API_KEY` | Authenticates Firecrawl API calls | GitHub repo → Settings → Secrets and variables → Actions |

No `.env` file is used in CI. The key is passed purely via the `env:` block in the workflow step.

## Error Handling

- **API failure:** `scrape_pipeline.py` raises or produces unexpected output → job fails → GitHub emails the repo owner. No retry logic.
- **No new files:** commit step detects empty `git status` output and exits 0 without creating an empty commit.
- **Push conflict:** job fails visibly. Acceptable for a solo project; resolve manually if it occurs.

## File Layout

```
.github/
  workflows/
    scrape.yml       ← new file
```

No changes to `scrape_pipeline.py` or any existing file.

## Out of Scope

- Retry logic on API failure
- Notifications (Slack, email) beyond GitHub's default failure emails
- Multi-branch strategy or PR-based review of scraped content
- Any downstream processing (wiki build) in this workflow
