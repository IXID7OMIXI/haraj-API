
import re
import requests

def get_client_id():
    """
    Attempts to extract the Haraj GraphQL Client ID from the homepage.
    """
    try:
        # 1. Fetch homepage
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get("https://haraj.com.sa/", headers=headers, timeout=10)
        r.raise_for_status()
        html = r.text

        # 2. Look for build ID or Next.js config that often contains the clientId
        # Pattern often looks like: "clientId":"..." or clientId:"..."
        # It's usually inside a script tag with __NEXT_DATA__ or similar
        
        # Regex for common key-value pattern in JS objects
        match = re.search(r'["\']?clientId["\']?\s*:\s*["\']([^"\']+)["\']', html)
        if match:
             return match.group(1)
        
        print("Regex didn't match. Using fallback ID.")
        return "mjuzkQiE-BBvR-…Ip3YBt0wfv3"

    except Exception as e:
        print(f"Error extracting Client ID: {e}")
        return "mjuzkQiE-BBvR-…Ip3YBt0wfv3"
