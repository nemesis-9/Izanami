from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
location_config = global_config.location_item_list()
crafter_config = global_config.agent_item_list('crafter')


class CrafterBuy:
    def __init__(self, crafter):
        self.crafter = crafter

    def need_to_buy(self):
        if self.crafter.wealth <= 0:
            return False

        if sum(self.crafter.inventory.values()) >= self.crafter.max_inventory:
            return False

        buying_resources = [
            resource
            for resource, amount in self.crafter.model.economy.resource_pools.items()
            if (
                    resource in crafter_config['buy'] and
                    amount >= 1 and
                    self.crafter.inventory.get(resource, 0) < self.crafter.buying_power.get(resource, 0)
            )
        ]

        return buying_resources or False

    def buy_materials(self):
        buying_resources = self.need_to_buy()
        if not buying_resources:
            return None

        buy_candidates = []
        for resource in buying_resources:
            current_price = self.crafter.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))

        buy_candidates.sort(key=lambda x: x[1])

        final_list = []
        for resource, current_price in buy_candidates:
            current_inv = sum(self.crafter.inventory.values())
            if self.crafter.wealth <= 0 or current_inv >= self.crafter.max_inventory:
                break

            target_qty = self.crafter.buying_power.get(resource, 0)
            owned_qty = self.crafter.inventory.get(resource, 0)
            needed_qty = max(0, target_qty - owned_qty)

            max_buy_by_wealth = int(self.crafter.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = self.crafter.max_inventory - current_inv

            quantity = min(needed_qty, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list or None
