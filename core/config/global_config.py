import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

ITEM_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_items.json')
LOCATION_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_location.json')
AGENT_CONFIG_FILR = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_agent.json')

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

try:
    with open(AGENT_CONFIG_FILR, 'r') as f:
        loaded_agents = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing item details file: {AGENT_CONFIG_FILR}")


def location_item_list():
    result = {}
    for location, values in loaded_locations.items():
        result[location] = values.get('items', [])
    return result


def agent_item_list():
    result = {}
    for agent, values in loaded_agents.items():
        key = agent.split('_')[0]
        buy_list = [key for key in values.get('buying_power', {}).keys()]
        sell_list = [key for key in values.get('selling_power', {}).keys()]
        result[key] = {
            'buy': buy_list,
            'sell': sell_list
        }
    return result


def global_var():
    result = {
        'location_item': location_item_list(),
        'agent_items': agent_item_list(),
    }

    return result


print(global_var())
