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


def get_subsystem_variables(sub_type, season):

    base_subsystem_config = loaded_subsystem_variables[sub_type].copy()

    season_modifiers = loaded_season_modifiers.get(season, {}).get(sub_type, {})
    print(base_subsystem_config.items())

    for section_name, resource_dict in base_subsystem_config.items():

        if isinstance(resource_dict, dict):
            for resource_name, base_value in resource_dict.items():
                resource_modifier_dict = season_modifiers.get(resource_name, {})
                final_multiplier = resource_modifier_dict.get(section_name, 1.0)

                if isinstance(base_value, (int, float)):
                    base_subsystem_config[section_name][resource_name] = round(base_value * final_multiplier, 4)

        elif isinstance(resource_dict, (int, float)):
            final_multiplier = season_modifiers.get(section_name, 1.0)
            base_subsystem_config[section_name] = round(resource_dict * final_multiplier, 4)

    return base_subsystem_config


# print(get_subsystem_variables("governance", "sprint"))
# print(get_subsystem_variables("governance", "summer"))
# print(get_subsystem_variables("governance", "autumn"))
# print(get_subsystem_variables("governance", "winter"))
