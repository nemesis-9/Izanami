from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
location_config = global_config.location_item_list()
trader_config = global_config.agent_item_list('trader')


class TraderSell:
    def __init__(self, trader):
        self.trader = trader

    def need_to_sell(self):
        if sum(self.trader.inventory.values()) <= 0:
            return False

        selling_resources = []
        resource_available = [
            resource
            for resource, amount in self.trader.inventory.items()
            if resource in trader_config['sell'] and amount >= 1
        ]

        if not resource_available:
            return False

        for resource in resource_available:
            base_price = self.trader.model.economy.base_prices[resource]
            current_price = self.trader.model.economy.current_price(resource)
            selling_price = round(base_price * self.trader.selling_aggression, 3)
            if current_price >= selling_price:
                selling_resources.append(resource)

        return selling_resources or False

    def sell_goods(self):
        market = self.trader.model.city_network.points_of_interest["market"]
        market_goods = location_config['market']

        city_center = self.trader.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_config['city_center']

        if self.trader.pos == market:
            allowed_goods = location_config["market"]
        elif self.trader.pos == city_center:
            allowed_goods = location_config["city_center"]
        else:
            return None

        selling_resources = self.need_to_sell()
        if not selling_resources:
            return None

        sell_candidates = []
        for resource in selling_resources:
            if resource not in allowed_goods:
                continue

            current_price = self.trader.model.economy.current_price(resource)
            sell_candidates.append((resource, current_price))

        sell_candidates.sort(key=lambda x: x[1], reverse=True)

        final_list = []
        for resource, current_price in sell_candidates:
            quantity = min(self.trader.inventory.get(resource, 0), self.trader.selling_power.get(resource, 0))

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list or None
