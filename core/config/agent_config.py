import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEASON_MODIFIER_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'season_modifiers.json')
AGENT_CONFIG_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_agent.json')


class AgentConfig:
    _instance = None

    @staticmethod
    def get():
        return AgentConfig()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentConfig, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        try:
            with open(SEASON_MODIFIER_PATH, 'r') as f:
                self.season_modifiers = json.load(f)
            with open(AGENT_CONFIG_PATH, 'r') as f:
                self.agent_variables = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Missing configuration file: {e.filename}") from e

    def agent_var(self, var_type, season):
        required_variables = self.agent_variables.get(f"{var_type}_variables", {})
        season_config = self.season_modifiers.get(season, {}).get("agent", {})

        result = {}

        for key, value in required_variables.items():
            if isinstance(value, (int, float)):
                result[key] = round(value * season_config.get(key, 1.0), 4)
            else:
                result[key] = value
        return result
