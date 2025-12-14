# =========================
# CONFIG (edit these only)
# =========================

# (1) Tags:
# - For one tag: set TAGS = ["بي ام دبليو"]
# - For multiple tags: set TAGS = ["بي ام دبليو", "تويوتا", ...]
# NOTE: The main "بي ام دبليو" tag has API pagination limit (~500 posts visible)
# Using sub-categories can access more posts
TAGS = ["بي ام دبليو","BMW"]


# (2) Target number of unique posts to collect PER TAG
TARGET_PER_TAG = 200

# (3) Output file
OUT_FILE = "haraj_clean_posts.json"

# (4) Optional keyword filter (to catch posts even if tags are wrong)
# Set KEYWORDS = [] to disable (default).
# If enabled, a post is kept if ANY keyword appears in title OR description (case-insensitive).
# Example: KEYWORDS = ["manual", "قير عادي", "جير عادي"]
KEYWORDS = KEYWORDS = ["manual", "قير عادي", "جير عادي"]

# Request pacing (be nice to the server; avoids rate-limits)
SLEEP_SECONDS_BETWEEN_REQUESTS = 0.4

# Hard safety limit so it doesn't run forever if something changes
MAX_REQUESTS_PER_TAG = 500

# (5) Haraj API Client ID
# Each user should get their own client ID to avoid rate-limiting issues.
# How to get your client ID:
#   1. Go to https://haraj.com.sa in your browser
#   2. Open Developer Tools (F12) → Network tab
#   3. Search for any listing or browse a category
#   4. Look for requests to "graphql.haraj.com.sa" and find the "clientId" parameter
CLIENT_ID = "qQGfZHPh-wko1-6XYa-TFfK-namWpCJ6MW1xv3"
