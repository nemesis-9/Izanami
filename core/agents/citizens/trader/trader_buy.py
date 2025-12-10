from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
trader_global_var = global_variables.get('agent_items', {}).get('trader', {})


class TraderBuy:
    def need_to_buy(self, trader):
        if trader.wealth <= 0 or sum(trader.inventory.values()) >= trader.max_inventory:
            return False

        buying_resources = []
        resources_available = [
            resource
            for resource, amount in trader.model.economy.resource_pools.items()
            if resource in trader_global_var['buy'] and amount >= 1
        ]

        if not resources_available:
            return False

        for resource in resources_available:
            base_price = trader.model.economy.base_prices.get(resource)
            current_price = trader.model.economy.calculate_price(resource)

            buying_price = round(base_price * trader.buying_aggression, 3)
            if current_price <= buying_price:
                buying_resources.append(resource)

        if not buying_resources:
            return False
        return buying_resources

    def buy_goods(self, trader):
        market = trader.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = trader.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        buying_resources = self.need_to_buy(trader)
        if not buying_resources:
            trader.toggle_mode()
            return

        buy_candidates = []
        for resource in buying_resources:
            current_price = trader.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))
        buy_candidates.sort(key=lambda x: x[1])

        final_list = []

        for resource, current_price in buy_candidates:
            if trader.wealth <= 0 or sum(trader.inventory.values()) >= trader.max_inventory:
                break

            if resource in market_goods and trader.pos != market:
                continue
            elif resource in city_center_goods and trader.pos != city_center:
                continue

            max_buy_by_power = int(trader.buying_power.get(resource, 0) / current_price) if current_price > 0 else 0
            max_buy_by_wealth = int(trader.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = trader.max_inventory - sum(trader.inventory.values())

            quantity = min(max_buy_by_power, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list
