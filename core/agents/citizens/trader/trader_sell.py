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
            base_price = self.trader.model.economy.base_price[resource]
            current_price = self.trader.model.economy.calculate_price(resource)
            selling_price = round(base_price * self.trader.selling_aggression, 3)
            if current_price >= selling_price:
                selling_resources.append(resource)

        if not selling_resources:
            return False
        return selling_resources

    def sell_goods(self):
        market = self.trader.model.city_network.points_of_interest["market"]
        market_goods = location_config['market']

        city_center = self.trader.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_config['city_center']

        selling_resources = self.need_to_sell()
        if not selling_resources:
            self.trader.toggle_mode()
            return

        sell_candidates = []
        for resource in selling_resources:
            current_price = self.trader.model.economy.calculate_price(resource)
            sell_candidates.append((resource, current_price))
        sell_candidates.sort(key=lambda x: x[1], reverse=True)

        final_list = []

        for resource, current_price in sell_candidates:
            if sum(self.trader.inventory.values()) <= 0:
                break

            if resource in market_goods and self.trader.pos != market:
                continue
            elif resource in city_center_goods and self.trader.pos != city_center:
                continue

            quantity = min(self.trader.inventory.get(resource, 0), self.trader.selling_power.get(resource, 0))

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list
