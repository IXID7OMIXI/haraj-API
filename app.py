from flask import Flask, render_template, request, jsonify
from haraj.client import client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from config import KEYWORDS_MANUAL, KEYWORDS_AUTO

@app.route('/api/search', methods=['POST'])
def search():
    print("DEBUG: /api/search hit!")
    data = request.json
    tag = data.get('tag', 'حراج السيارات')
    page = data.get('page', 1)
    req_limit = data.get('limit', 20)
    
    # Client is already instantiated in haraj.client
    # In a real app you might want to instantiate it per request or globally in a better way, 
    # but for this script it's fine.
    
    # Refresh client_id if needed? For now assume it persists.
    
    # Fetch more items to increase chances of finding matches after filtering
    fetch_limit = 60 
    results = client.search(tag=tag, page=page, limit=fetch_limit)
    
    # Apply filters? 
    # Ideally the API does it, but Haraj API is limited.
    # We can filter here if the user wants "Manual" specifically.
    gear_filter = data.get('gear_filter') # "MANUAL", "AUTO", or None
    user_keywords = data.get('keywords', [])
    
    filtered_results = []
    if gear_filter or user_keywords:
        # Determine fallback keywords based on gear filter
        fallback_gear_keywords = []
        if gear_filter == "MANUAL":
            fallback_gear_keywords = KEYWORDS_MANUAL
        elif gear_filter == "AUTO":
            fallback_gear_keywords = KEYWORDS_AUTO

        for item in results:
            # 1. Check Gear Filter (Smart Logic)
            if gear_filter:
                car_info = item.get('carInfo') or {}
                # Ensure car_info is a dict
                if not isinstance(car_info, dict):
                    car_info = {}
                    
                item_gear = car_info.get('gear')
                
                match = False
                
                # Case A: Gear is explicitly set in API
                if item_gear: 
                    # Strict check: must match filter
                    if str(item_gear).upper() == gear_filter.upper():
                        match = True
                    else:
                        match = False # Explicit mismatch (e.g. says AUTO but we want MANUAL)
                
                # Case B: Gear is missing/None -> Fallback to keyword search in title/body
                else:
                    text = (item.get('title') or "") + "\n" + (item.get('bodyTEXT') or "")
                    if any(k.lower() in text.lower() for k in fallback_gear_keywords):
                        match = True
                    else:
                        match = False
                
                if not match:
                    continue

            # 2. Check User Keywords (Additional Filter)
            if user_keywords:
                text = (item.get('title') or "") + " " + (item.get('bodyTEXT') or "")
                if not any(k.lower() in text.lower() for k in user_keywords):
                    continue
            
            filtered_results.append(item)
    else:
        filtered_results = results

    return jsonify({"items": filtered_results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
