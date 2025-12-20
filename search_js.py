
import re

def find_client_id(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for clientId:"..." or clientId="..." or similar
            matches = re.findall(r'clientId:"([^"]+)"', content)
            if matches:
                print(f"Found matches: {matches}")
            else:
                print("No matches found with regex clientId:\"...\"")
                
            # Try looser regex
            matches2 = re.findall(r'clientId:\s*["\']([^"\']+)["\']', content)
            if matches2:
                print(f"Found loose matches: {matches2}")

    except Exception as e:
        print(f"Error: {e}")

find_client_id('client_js.js')
