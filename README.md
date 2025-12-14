# Haraj API Scraper

A Python script to scrape car listings from [Haraj.com.sa](https://haraj.com.sa) (Saudi Arabia's largest classified ads marketplace).

## Requirements

- Python 3.x
- `requests` library

## Installation

```bash
# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize the scraper:

### 1. `TAGS` - What to Search For

```python
TAGS = ["بي ام دبليو"]
```

**What it does:** Specifies which Haraj category tags to scrape. The script fetches posts that have these tags.

**How to use:**
- Single tag: `TAGS = ["بي ام دبليو"]`
- Multiple tags: `TAGS = ["بي ام دبليو", "تويوتا", "مرسيدس"]`

**Examples of valid tags:**
| Tag | Description |
|-----|-------------|
| `"حراج السيارات"` | All cars (main category) |
| `"بي ام دبليو"` | BMW (all models) |
| `"الفئة الخامسة"` | BMW 5 Series |
| `"الفئة السابعة"` | BMW 7 Series |
| `"الفئة X"` | BMW X Series (SUVs) |
| `"الفئة الثالثة"` | BMW 3 Series |
| `"الفئة M"` | BMW M Performance |
| `"تويوتا"` | Toyota |
| `"مرسيدس"` | Mercedes |

> **⚠️ API Limitation:** Each tag has a pagination limit of ~500 posts. To get more posts, use multiple specific sub-tags instead of one general tag.

---

### 2. `KEYWORDS` - Filter by Keywords

```python
KEYWORDS = ["manual", "قير عادي", "جير عادي"]
```

**What it does:** After fetching posts by tag, filters them to keep only posts containing ANY of these keywords in the title OR description.

**How to use:**
- Disabled (keep all posts): `KEYWORDS = []`
- Filter for manual transmission: `KEYWORDS = ["manual", "قير عادي", "جير عادي"]`
- Filter for specific models: `KEYWORDS = ["520", "530", "540"]`

**Behavior:**
- Case-insensitive matching
- Post is kept if ANY keyword matches (OR logic, not AND)
- Searches both `title` and `description` fields

---

### 3. `TARGET_PER_TAG` - How Many Posts to Collect

```python
TARGET_PER_TAG = 200
```

**What it does:** Maximum number of unique posts to collect for each tag.

**Example:** If `TAGS = ["الفئة الخامسة", "الفئة السابعة"]` and `TARGET_PER_TAG = 200`, the script will try to collect up to 200 posts from each tag (400 total max).

---

### 4. `OUT_FILE` - Output Filename

```python
OUT_FILE = "haraj_clean_posts.json"
```

**What it does:** Name of the JSON file where results are saved.

---

### 5. `SLEEP_SECONDS_BETWEEN_REQUESTS` - Request Delay

```python
SLEEP_SECONDS_BETWEEN_REQUESTS = 0.4
```

**What it does:** Delay (in seconds) between API requests to avoid rate-limiting.

---

### 6. `MAX_REQUESTS_PER_TAG` - Safety Limit

```python
MAX_REQUESTS_PER_TAG = 500
```

**What it does:** Maximum number of API requests per tag (safety limit to prevent infinite loops).

---

### 7. `CLIENT_ID` - Haraj API Client ID

```python
CLIENT_ID = "qQGfZHPh-wko1-6XYa-TFfK-namWpCJ6MW1xv3"
```

**What it does:** Authentication token for Haraj's GraphQL API.

**⚠️ Important:** Each user should get their own client ID to avoid shared rate-limiting.

**How to get your own client ID:**
1. Go to [https://haraj.com.sa](https://haraj.com.sa) in your browser
2. Open Developer Tools (press `F12`)
3. Go to the **Network** tab
4. Search for any listing or browse a category on the site
5. Look for requests to `graphql.haraj.com.sa`
6. Find the `clientId` parameter in the URL and copy its value

---

## Running the Script

```bash
python main.py
```

**Output:**
- Progress is displayed in the terminal
- Results are saved to the configured output file (default: `haraj_clean_posts.json`)

---

## Output Format

The script outputs a JSON file with an array of posts:

```json
[
  {
    "id": 171417053,
    "url": "https://haraj.com.sa/11171417053/BMW_X3_شبه_مخزنة/",
    "city": "جده",
    "title": "BMW X3 شبه مخزنة",
    "tags": ["حراج السيارات", "بي ام دبليو", "الفئة X"],
    "description": "ما شاء الله\nكل مواصفات BMW المعروفة...",
    "postDate": "2025-12-11 15:25:53"
  }
]
```

---

## Common Use Cases

### Get all BMW posts (using sub-tags for more coverage)
```python
TAGS = [
    "الفئة الخامسة",
    "الفئة السابعة",
    "الفئة X",
    "الفئة الثالثة",
    "الفئة M",
]
TARGET_PER_TAG = 200
KEYWORDS = []  # No keyword filter
```

### Find manual transmission cars only
```python
TAGS = ["حراج السيارات"]
TARGET_PER_TAG = 500
KEYWORDS = ["manual", "قير عادي", "جير عادي", "عادي"]
```

### Get specific BMW models
```python
TAGS = ["الفئة الخامسة"]
TARGET_PER_TAG = 300
KEYWORDS = ["520", "530", "540", "M5"]
```

---

## Known Limitations

1. **Pagination Limit:** The Haraj API limits pagination to ~500 posts per tag. Use specific sub-tags to access more posts.

2. **Date Range:** Only recent posts are accessible (approximately last 6-8 weeks).

3. **Rate Limiting:** Making requests too fast may result in temporary blocks. Adjust `SLEEP_SECONDS_BETWEEN_REQUESTS` if needed.

---

## Assumptions Made

1. **City Field:** The script uses `geoCity` when available, falling back to `city` field.
2. **Date Format:** Unix timestamps are converted to `YYYY-MM-DD HH:MM:SS` format in local timezone.
3. **Page Numbering:** API pagination starts at page 1 (not 0).

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script stops early with few posts | API pagination limit reached. Use more specific sub-tags. |
| `401/403` errors | API authentication may have changed. Report the issue. |
| No posts returned | Check if the tag name is correct (Arabic spelling matters). |
| Rate limit errors | Increase `SLEEP_SECONDS_BETWEEN_REQUESTS` value. |
