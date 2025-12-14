# =========================
# CONFIG (edit these only)
# =========================

# (1) Tags:
# - For one tag: set TAGS = ["بي ام دبليو"]
# - For multiple tags: set TAGS = ["بي ام دبليو", "تويوتا", ...]
# NOTE: The main "بي ام دبليو" tag has API pagination limit (~500 posts visible)
# Using sub-categories can access more posts
TAGS = ["بي ام دبليو"]


# (2) Target number of unique posts to collect PER TAG
# When using KEYWORDS filter, set this HIGH since we're filtering down from many posts
# The script will stop early if it reaches this target
TARGET_PER_TAG = 500000

# (3) Output file
OUT_FILE = "haraj_clean_posts.json"

# (4) Gear filter - filter by transmission type
# Options:
#   "MANUAL"  - Only manual transmission cars
#   "AUTO"    - Only automatic transmission cars  
#   None      - No gear filter (get all cars)
GEAR_FILTER = None

# (5) Optional keyword filter (additional text search)
# Set KEYWORDS = [] to disable keyword filtering.
# If enabled AND GEAR_FILTER is set, keywords are used as fallback when carInfo.gear is missing.
# If GEAR_FILTER is None, keywords filter posts by title/description text.

# ═══════════════════════════════════════════════════════════
# KEYWORD PRESETS - Define your keyword groups here
# ═══════════════════════════════════════════════════════════

# Manual transmission keywords (Arabic + English variations)
KEYWORDS_MANUAL = [
    # English
    "manual", "stick", "standard",
    # Arabic - قير/جير عادي variations
    "قير عادي", "جير عادي", "قير عادى", "جير عادى",
    # Arabic - مانيوال variations  
    "مانيوال", "مانوال", "مانويل",
    # Arabic - other terms
    "يدوي", "ستيك", "ستاندرد",
]

# Automatic transmission keywords
KEYWORDS_AUTO = [
    # English
    "automatic", "auto",
    # Arabic
    "قير اوتوماتيك", "جير اوتوماتيك", "اوتوماتيك", "تماتك",
]

# Add more presets as needed:
# KEYWORDS_DRIFT = ["درفت", "drift", ...]
# KEYWORDS_CHEAP = ["رخيص", "مستعجل", ...]

# ═══════════════════════════════════════════════════════════
# ACTIVE KEYWORDS - Choose which preset to use
# ═══════════════════════════════════════════════════════════
# Options:
#   KEYWORDS = []                  → No keyword filtering
#   KEYWORDS = KEYWORDS_MANUAL     → Use manual transmission keywords
#   KEYWORDS = KEYWORDS_AUTO       → Use automatic transmission keywords
#   KEYWORDS = KEYWORDS_MANUAL + KEYWORDS_AUTO  → Combine multiple presets
#   KEYWORDS = KEYWORDS_MANUAL + CUSTOM_KEYWORDS → Preset + your own keywords

# Your custom keywords (add whatever you want here)
CUSTOM_KEYWORDS = []

# ACTIVE KEYWORDS - mix and match as you like:
KEYWORDS = KEYWORDS_MANUAL + CUSTOM_KEYWORDS

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
