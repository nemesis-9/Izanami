from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
crafter_global_var = global_variables.get('agent_items', {}).get('crafter', {})


class CrafterBuy:
    def need_to_buy(self, crafter):
        if crafter.wealth <= 0 or sum(crafter.inventory.values()) >= crafter.max_inventory:
            return False

        buying_resources = [
            resource
            for resource, amount in crafter.model.economy.resource_pools.items()
            if (
                    resource in crafter_global_var['buy'] and
                    amount >= 1 and
                    crafter.inventory.get(resource, 0) < crafter.buying_power.get(resource, 0)
            )
        ]

        if not buying_resources:
            return False
        return buying_resources

    def buy_materials(self, crafter):
        market = crafter.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = crafter.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        buying_resources = self.need_to_buy(crafter)
        if not buying_resources:
            crafter.toggle_mode()
            return

        buy_candidates = []
        for resource in buying_resources:
            current_price = crafter.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))
        buy_candidates.sort(key=lambda x: x[1])

        final_list = []

        for resource, current_price in buy_candidates:
            if crafter.wealth <= 0 or sum(crafter.inventory.values()) >= crafter.max_inventory:
                break

            if resource in market_goods and crafter.pos != market:
                continue
            if resource in city_center_goods and crafter.pos != city_center:
                continue

            max_buy_by_power = int(crafter.buying_power.get(resource, 0) / current_price) if current_price > 0 else 0
            max_buy_by_wealth = int(crafter.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = crafter.max_inventory - sum(crafter.inventory.values())

            quantity = min(max_buy_by_power, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                if quantity > 0:
                    final_list.append((resource, quantity))

            return final_list
