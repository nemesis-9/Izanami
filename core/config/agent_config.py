import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEASON_MODIFIER_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'season_modifiers.json')
AGENT_CONFIG_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_agent.json')

try:
    with open(SEASON_MODIFIER_PATH, 'r') as f:
        loaded_season_modifiers = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing season modifiers: {SEASON_MODIFIER_PATH}")

try:
    with open(AGENT_CONFIG_PATH, 'r') as f:
        loaded_agent_variables = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing agent variables: {AGENT_CONFIG_PATH}")


def get_variables(var_type, season):
    required_variables = loaded_agent_variables[f"{var_type}_variables"]
    season_config = loaded_season_modifiers.get(season, {}).get("agent", {})

    result = {}

    for key, value in required_variables.items():
        if isinstance(value, (int, float)):
            result[key] = round(value * season_config.get(key, 1.0), 4)
        else:
            result[key] = value

    return result
