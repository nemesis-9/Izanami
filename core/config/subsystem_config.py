import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEASON_MODIFIER_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'season_modifiers.json')
SUBSYSTEM_VARIABLE_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_subsystem.json')

try:
    with open(SEASON_MODIFIER_PATH, 'r') as f:
        loaded_season_modifiers = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing season modifiers: {SEASON_MODIFIER_PATH}")

try:
    with open(SUBSYSTEM_VARIABLE_PATH, 'r') as f:
        loaded_subsystem_variables = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Missing subsystem variables: {SUBSYSTEM_VARIABLE_PATH}")


def get_subsystem_variables(season):

    base_economy_config = loaded_subsystem_variables["economy"].copy()

    economy_modifiers = loaded_season_modifiers.get(season, {}).get("economy", {})

    for section_name, resource_dict in base_economy_config.items():
        for resource_name, base_value in resource_dict.items():
            resource_modifier_dict = economy_modifiers.get(resource_name, {})
            final_multiplier = resource_modifier_dict.get(section_name, 1.0)

            if isinstance(base_value, (int, float)):
                base_economy_config[section_name][resource_name] = round(base_value * final_multiplier, 4)

    return base_economy_config
