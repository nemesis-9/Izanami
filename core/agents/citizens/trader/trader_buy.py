from core.config.global_config import GlobalConfig

global_config = GlobalConfig().get()
location_config = global_config.location_item_list()
trader_config = global_config.agent_item_list('trader')


class TraderBuy:
    def __init__(self, trader):
        self.trader = trader

    def need_to_buy(self):
        if self.trader.wealth <= 0 or sum(self.trader.inventory.values()) >= self.trader.max_inventory:
            return False

        buying_resources = []
        resources_available = [
            resource
            for resource, amount in self.trader.model.economy.resource_pools.items()
            if resource in trader_config['buy'] and amount >= 1
        ]

        if not resources_available:
            return False

        for resource in resources_available:
            base_price = self.trader.model.economy.base_prices.get(resource)
            current_price = self.trader.model.economy.calculate_price(resource)

            buying_price = round(base_price * self.trader.buying_aggression, 3)
            if current_price <= buying_price:
                buying_resources.append(resource)

        if not buying_resources:
            return False
        return buying_resources

    def buy_goods(self):
        market = self.trader.model.city_network.points_of_interest["market"]
        market_goods = location_config['market']

        city_center = self.trader.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_config['city_center']

        buying_resources = self.need_to_buy()
        if not buying_resources:
            self.trader.toggle_mode()
            return

        buy_candidates = []
        for resource in buying_resources:
            current_price = self.trader.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))
        buy_candidates.sort(key=lambda x: x[1])

        final_list = []

        for resource, current_price in buy_candidates:
            if self.trader.wealth <= 0 or sum(self.trader.inventory.values()) >= self.trader.max_inventory:
                break

            if resource in market_goods and self.trader.pos != market:
                continue
            elif resource in city_center_goods and self.trader.pos != city_center:
                continue

            max_buy_by_power = int(self.trader.buying_power.get(resource, 0) / current_price) if current_price > 0 else 0
            max_buy_by_wealth = int(self.trader.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = self.trader.max_inventory - sum(self.trader.inventory.values())

            quantity = min(max_buy_by_power, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list
