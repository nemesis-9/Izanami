import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEASON_MODIFIER_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'season_modifiers.json')
SUBSYSTEM_VARIABLE_PATH = os.path.join(CURRENT_DIR, '..', '..', 'data', 'input', 'variables_subsystem.json')


class SubsystemConfig:
    _instance = None

    @staticmethod
    def get():
        return SubsystemConfig()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SubsystemConfig, cls).__new__(cls)
            cls._instance._load_configs()
        return cls._instance

    def _load_configs(self):
        try:
            with open(SEASON_MODIFIER_PATH, 'r') as f:
                self.season_modifiers = json.load(f)
            with open(SUBSYSTEM_VARIABLE_PATH, 'r') as f:
                self.subsystem_variables = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Missing configuration file: {e.filename}") from e

    def subsystem_var(self, sub_type, season):
        base_subsystem_config = self.subsystem_variables.get(sub_type, {})
        season_modifiers = self.season_modifiers.get(season, {}).get(sub_type, {})

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
