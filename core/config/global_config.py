import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

ITEM_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_items.json')
LOCATION_DETAILS_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'details_location.json')
AGENT_CONFIG_FILE = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_agent.json')


class GlobalConfig:
    _instance = None

    @staticmethod
    def get():
        return GlobalConfig()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        try:
            with open(ITEM_DETAILS_FILE, 'r') as f:
                self.items = json.load(f)
            with open(LOCATION_DETAILS_FILE, 'r') as f:
                self.locations = json.load(f)
            with open(AGENT_CONFIG_FILE, 'r') as f:
                self.agents = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Missing configuration file: {e.filename}") from e

    def location_item_list(self):
        result = {}
        for location, values in self.locations.items():
            result[location] = values.get('items', [])
        return result

    def agent_item_list(self, agent_type):
        result = {}
        for agent, values in self.agents.items():
            key = agent.split('_')[0]
            if key == agent_type:
                buy_list = [key for key in values.get('buying_power', {}).keys()]
                sell_list = [key for key in values.get('selling_power', {}).keys()]
                result = {
                    'buy': buy_list,
                    'sell': sell_list
                }
        return result


# global_config = GlobalConfig().get()
# crafter_config = global_config.agent_item_list('crafter')
# print(f"crafter config: {crafter_config}")
