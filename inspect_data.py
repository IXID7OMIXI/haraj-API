from haraj.client import client
import json

try:
    results = client.search(tag="بي ام دبليو")
    if results:
        item = results[0]
        print("First Item Data:")
        print(f"URL: {item.get('URL')}")
        print(f"thumbURL: {item.get('thumbURL')}")
        print(f"imagesList: {item.get('imagesList')}")
    else:
        print("No results found to inspect.")
except Exception as e:
    print(f"Error: {e}")
