from core.config.global_config import global_var

global_variables = global_var()
crafter_global_var = global_variables.get('agent_items', {}).get('crafter', {})
items_global_var = global_variables.get('items', {})


class CrafterCraft:
    def craft(self, crafter):
        return True