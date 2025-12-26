from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
crafter_config = global_config.agent_item_list('crafter')
items_config = global_config.items


class CrafterCraft:
    def __init__(self, crafter):
        self.crafter = crafter

    def can_craft_anything(self):
        for item_name, item_details in items_config.items():
            if item_name not in crafter_config['sell']:
                continue

            mats = item_details.get('crafting_material', {})
            if all(self.crafter.inventory.get(m, 0) >= qty for m, qty in mats.items()):
                return True

        return False

    def craft(self):
        if not self.can_craft_anything():
            return None

        space_left = self.crafter.max_inventory - sum(self.crafter.inventory.values())
        if space_left <= 0:
            return None

        craftable = {}

        for item, details in items_config.items():
            if item not in crafter_config['sell']:
                continue

            mats = details.get('crafting_material', {})
            max_crafts = min(
                self.crafter.inventory.get(m, 0) // q
                for m, q in mats.items()
            )

            if max_crafts > 0:
                profit = (
                    self.crafter.model.economy.calculate_price(item) -
                    sum(
                        q * self.crafter.model.economy.calculate_price(m)
                        for m, q in mats.items()
                    )
                )
                craftable[item] = (profit, max_crafts, mats)

        if not craftable:
            return None

        item, (profit, max_crafts, mats) = max(craftable.items(), key=lambda x: x[1][0])
        qty = min(max_crafts, space_left)

        for mat, q in mats.items():
            self.crafter.inventory[mat] -= q * qty

        self.crafter.inventory[item] = self.crafter.inventory.get(item, 0) + qty
        return item, qty
