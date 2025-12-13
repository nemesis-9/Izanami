from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
location_config = global_config.location_item_list()
crafter_config = global_config.agent_item_list('crafter')


class CrafterBuy:
    def __init__(self, crafter):
        self.crafter = crafter

    def need_to_buy(self):
        if self.crafter.wealth <= 0 or sum(self.crafter.inventory.values()) >= self.crafter.max_inventory:
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

        if not buying_resources:
            return False
        return buying_resources

    def buy_materials(self):
        market = self.crafter.model.city_network.points_of_interest["market"]
        market_goods = location_config['market']

        city_center = self.crafter.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_config['city_center']

        buying_resources = self.need_to_buy()
        if not buying_resources:
            self.crafter.toggle_mode()
            return

        buy_candidates = []
        for resource in buying_resources:
            current_price = self.crafter.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))
        buy_candidates.sort(key=lambda x: x[1])

        final_list = []

        for resource, current_price in buy_candidates:
            if self.crafter.wealth <= 0 or sum(self.crafter.inventory.values()) >= self.crafter.max_inventory:
                break

            if resource in market_goods and self.crafter.pos != market:
                continue
            if resource in city_center_goods and self.crafter.pos != city_center:
                continue

            max_buy_by_power = int(self.crafter.buying_power.get(resource, 0) / current_price) if current_price > 0 else 0
            max_buy_by_wealth = int(self.crafter.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = self.crafter.max_inventory - sum(self.crafter.inventory.values())

            quantity = min(max_buy_by_power, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                if quantity > 0:
                    final_list.append((resource, quantity))

            return final_list
