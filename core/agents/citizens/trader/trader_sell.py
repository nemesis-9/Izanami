from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
trader_global_var = global_variables.get('agent_items', {}).get('trader', {})


class TraderSell:
    def need_to_sell(self, trader):
        if sum(trader.inventory.values()) <= 0:
            return False

        selling_resources = []
        resource_available = [
            resource
            for resource, amount in trader.inventory.items()
            if resource in trader_global_var['sell'] and amount >= 1
        ]

        if not resource_available:
            return False

        for resource in resource_available:
            base_price = trader.model.economy.base_price[resource]
            current_price = trader.model.economy.calculate_price(resource)
            selling_price = round(base_price * trader.selling_aggression, 3)
            if current_price >= selling_price:
                selling_resources.append(resource)

        if not selling_resources:
            return False
        return selling_resources

    def sell_goods(self, trader):
        market = trader.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = trader.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        selling_resources = self.need_to_sell(trader)
        if not selling_resources:
            trader.toggle_mode()
            return

        sell_candidates = []
        for resource in selling_resources:
            current_price = trader.model.economy.calculate_price(resource)
            sell_candidates.append((resource, current_price))
        sell_candidates.sort(key=lambda x: x[1], reverse=True)

        final_list = []

        for resource, current_price in sell_candidates:
            if sum(trader.inventory.values()) <= 0:
                break

            if resource in market_goods and trader.pos != market:
                continue
            elif resource in city_center_goods and trader.pos != city_center:
                continue

            quantity = min(trader.inventory.get(resource, 0), trader.selling_power.get(resource, 0))

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list
