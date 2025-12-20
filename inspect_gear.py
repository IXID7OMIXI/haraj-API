from haraj.client import client
import json

try:
    # Toyota is good for finding mixed manual/auto
    results = client.search(tag="تويوتا") 
    print(f"Found {len(results)} items")
    for i, item in enumerate(results[:5]):
        car_info = item.get('carInfo', {})
        gear = car_info.get('gear')
        print(f"Item {i} Gear: '{gear}' (Type: {type(gear)})")
except Exception as e:
    print(f"Error: {e}")
