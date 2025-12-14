import json
import time
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional, Set

from config import (
    TAGS,
    TARGET_PER_TAG,
    OUT_FILE,
    KEYWORDS,
    SLEEP_SECONDS_BETWEEN_REQUESTS,
    MAX_REQUESTS_PER_TAG,
    CLIENT_ID,
)

API_URL = (
    "https://graphql.haraj.com.sa/"
    "?queryName=posts"
    f"&clientId={CLIENT_ID}"
    "&version=N0.0.1%20,%202025-12-11%2015/"
)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    # If you later see 401/403, do NOT guess—tell me and we can add the exact headers/cookies needed.
}

# Minimal query: only request fields you want to keep
# Using HYBRID pagination: page + beforePostDate cursor
# The API limits page-based pagination to ~10 pages, so we use beforePostDate 
# to shift the window of results when we exhaust pages
QUERY = """
query FetchAds($tag: String = null, $limit: Int = null, $page: Int = null, $beforePostDate: Int = null) {
  posts(tag: $tag, limit: $limit, page: $page, beforePostDate: $beforePostDate) {
    items {
      id
      title
      URL
      city
      geoCity
      tags
      bodyTEXT
      postDate
      updateDate
    }
    pageInfo {
      hasNextPage
    }
  }
}
"""

def contains_keywords(title: Optional[str], desc: Optional[str], keywords: List[str]) -> bool:
    if not keywords:
        return True  # filter disabled
    hay = ((title or "") + "\n" + (desc or "")).lower()
    return any(k.lower() in hay for k in keywords)

def clean_item(p: Dict[str, Any]) -> Dict[str, Any]:
    # NOTE (explicit assumption):
    # Use geoCity when available; fallback to city.
    city = p.get("geoCity") or p.get("city")

    url_rel = p.get("URL")
    full_url = ("https://haraj.com.sa/" + url_rel.lstrip("/")) if isinstance(url_rel, str) else None

    # Convert Unix timestamp to readable date (postDate is in seconds)
    post_date_ts = p.get("postDate")
    post_date_str = None
    if isinstance(post_date_ts, int):
        post_date_str = datetime.fromtimestamp(post_date_ts).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "id": p.get("id"),
        "url": full_url,
        "city": city,
        "title": p.get("title"),
        "tags": p.get("tags") if isinstance(p.get("tags"), list) else [],
        "description": p.get("bodyTEXT"),
        "postDate": post_date_str,
    }

def fetch_page(tag: str, limit: int, page: int, before_post_date: Optional[int] = None) -> Dict[str, Any]:
    payload = {
        "query": QUERY,
        "variables": {
            "tag": tag,
            "limit": limit,
            "page": page,
            "beforePostDate": before_post_date
        }
    }
    r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data

def collect_for_tag(tag: str) -> List[Dict[str, Any]]:
    collected: List[Dict[str, Any]] = []
    seen_ids: Set[int] = set()

    limit = 50  # batch size per request
    # HYBRID PAGINATION:
    # - Use page (1-10) within each "window"
    # - Use beforePostDate cursor to shift to older posts when pages exhausted
    page = 1
    cursor: Optional[int] = None  # beforePostDate cursor
    max_page_per_window = 10  # API seems to limit pagination to ~10 pages
    stale_cursor_count = 0  # Track if cursor isn't advancing

    for req_i in range(MAX_REQUESTS_PER_TAG):
        cursor_str = f" | cursor={cursor}" if cursor else ""
        print(f"\r  Page {page}{cursor_str} | Collected: {len(collected)}/{TARGET_PER_TAG} posts | Fetching...", end="", flush=True)

        data = fetch_page(tag=tag, limit=limit, page=page, before_post_date=cursor)

        print(f"\r  Page {page}{cursor_str} | Collected: {len(collected)}/{TARGET_PER_TAG} posts | Done         ", end="", flush=True)

        posts = data["data"]["posts"]
        items = posts["items"]
        has_next = posts["pageInfo"]["hasNextPage"]

        if not items:
            print(f"\n  ⚠ No items returned (page {page}, cursor={cursor})")
            break

        # Track the oldest postDate in this batch for cursor advancement
        # beforePostDate gets posts BEFORE that time, so we need the MINIMUM to go back further
        min_post_date = None
        new_in_batch = 0

        for p in items:
            pid = p.get("id")
            if pid is None:
                continue
            
            # Track oldest postDate (minimum value = oldest)
            pd = p.get("postDate")
            if isinstance(pd, int):
                if min_post_date is None or pd < min_post_date:
                    min_post_date = pd

            if pid in seen_ids:
                continue

            cleaned = clean_item(p)
            if not contains_keywords(cleaned.get("title"), cleaned.get("description"), KEYWORDS):
                continue

            seen_ids.add(pid)
            collected.append(cleaned)
            new_in_batch += 1

            if len(collected) >= TARGET_PER_TAG:
                break

        # Stop if we hit our target
        if len(collected) >= TARGET_PER_TAG:
            break

        # Stop if API says no more pages
        if not has_next:
            print(f"\n  ✓ Reached end of results. Total: {len(collected)}")
            break

        # If we got items but no new ones, need to shift cursor
        if new_in_batch == 0:
            if min_post_date is not None and (cursor is None or min_post_date < cursor):
                # Shift cursor to oldest post to get even older posts
                print(f"\n  → Shifting cursor from {cursor} to {min_post_date}")
                cursor = min_post_date
                page = 1  # Reset to page 1 with new cursor
                stale_cursor_count = 0
                continue
            else:
                stale_cursor_count += 1
                if stale_cursor_count >= 3:
                    print(f"\n  ⚠ Cursor stuck at {cursor}, can't find more unique posts. Stopping.")
                    break
                # Try next page even with no new items
                page += 1
                continue

        stale_cursor_count = 0  # Reset stale counter when we find new items

        # Check if we should shift cursor or increment page
        if page >= max_page_per_window:
            # Hit page limit, shift cursor to oldest item seen
            if min_post_date is not None and (cursor is None or min_post_date < cursor):
                print(f"\n  → Page limit reached, shifting cursor from {cursor} to {min_post_date}")
                cursor = min_post_date
                page = 1
            else:
                # Can't advance cursor, try higher page anyway
                page += 1
        else:
            page += 1

        time.sleep(SLEEP_SECONDS_BETWEEN_REQUESTS)

    return collected

def main():
    all_results: List[Dict[str, Any]] = []
    for tag in TAGS:
        print(f"Collecting tag={tag!r} ...")
        results = collect_for_tag(tag)
        # Print newline to move past the \r progress line, then show final count
        print(f"\n  ✓ Finished: {len(results)} unique posts")
        all_results.extend(results)

    # Save cleaned JSON (Arabic preserved)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)  # keep Arabic readable [web:316]

    print(f"Saved total {len(all_results)} posts to {OUT_FILE}")

if __name__ == "__main__":
    main()
