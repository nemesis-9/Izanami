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
            base_price = self.trader.model.economy.base_prices.get(resource, 0)
            current_price = self.trader.model.economy.current_price(resource)

            buying_price = round(base_price * self.trader.buying_aggression, 3)
            if current_price <= buying_price:
                buying_resources.append(resource)

        return buying_resources or False

    def buy_goods(self):
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

        buying_resources = self.need_to_buy()
        if not buying_resources:
            return None

        buy_candidates = []
        for resource in buying_resources:
            if resource not in allowed_goods:
                continue

            current_price = self.trader.model.economy.current_price(resource)
            buy_candidates.append((resource, current_price))

        buy_candidates.sort(key=lambda x: x[1])

        final_list = []
        for resource, current_price in buy_candidates:
            inv_total = sum(self.trader.inventory.values())
            if self.trader.wealth <= 0 or inv_total >= self.trader.max_inventory:
                break

            target_qty = self.trader.buying_power.get(resource, 0)
            owned_qty = self.trader.inventory.get(resource, 0)
            needed_qty = max(0, target_qty - owned_qty)

            max_buy_by_wealth = int(self.trader.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = self.trader.max_inventory - inv_total

            quantity = min(needed_qty, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                final_list.append((resource, quantity))

        return final_list or None
