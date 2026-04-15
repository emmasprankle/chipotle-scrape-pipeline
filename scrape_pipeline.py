import datetime
import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
import requests


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


load_dotenv()

api_key = os.getenv("FIRECRAWL_API_KEY")

# --- Step 01: Search + scrape with Firecrawl ---

api_url = "https://api.firecrawl.dev/v2/search"

headers = {
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "query": "Chipotle investor relations press releases",
    "limit": 5,
    "scrapeOptions": {"formats": ["markdown"]}
}

response = requests.post(api_url, headers=headers, json=payload)

data = response.json() # convert response to JSON
results = data["data"]["web"] # get the results from the response
print(f"Firecrawl returned {len(results)} results")

for r in results:
    print(f"  - {r['title']}")
    print(f"    {r['url']}")
    print(f"    markdown length: {len(r.get('markdown') or '')} chars")