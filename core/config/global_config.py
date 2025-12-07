import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

ITEM_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_items.json')
LOCATION_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_location.json')

try:
    with open(ITEM_DETAILS_FILE, 'r') as f:
        loaded_items = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing item details file: {ITEM_DETAILS_FILE}")

try:
    with open(LOCATION_DETAILS_FILE, 'r') as f:
        loaded_locations = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing item details file: {LOCATION_DETAILS_FILE}")

result = {
    'items': loaded_items,
    'locations': loaded_locations
}

# print(result)
