from core.agents.agent import BaseAgent
from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
trader_global_var = global_variables.get('agent_items', {}).get('trader', {})


class Trader(BaseAgent):
    def __init__(self, model, wealth, initial_trader_config):
        super().__init__(model, wealth, "Trader")

        self.inventory = {"food": 2}

        self.path = None

        self.home_location = None
        self.destination = None
        self.mode = 'selling'

        self.max_inventory = initial_trader_config.get("max_inventory", 0)
        self.buying_power = initial_trader_config.get("buying_power", {})
        self.buying_aggression = initial_trader_config.get("buying_aggression", 1.0)
        self.selling_power = initial_trader_config.get("selling_power", {})
        self.selling_aggression = initial_trader_config.get("selling_aggression", 1.0)
        self.inventory_margin = initial_trader_config.get("inventory_margin", 0)
        self.wealth_margin = initial_trader_config.get("wealth_margin", 0)

    def update_agent_config(self):
        super().update_agent_config()
        trader_vars = self.model.trader_variables
        self.max_inventory = trader_vars.get("max_inventory", 0)
        self.buying_power = trader_vars.get("buying_power", {})
        self.buying_aggression = trader_vars.get("buying_aggression", 1.0)
        self.selling_power = trader_vars.get("selling_power", {})
        self.selling_aggression = trader_vars.get("selling_aggression", 1.0)
        self.inventory_margin = trader_vars.get("inventory_margin", 0)
        self.wealth_margin = trader_vars.get("wealth_margin", 0)

    def toggle_mode(self):
        if self.mode == 'selling':
            self.mode = 'buying'
        elif self.mode == 'buying':
            self.mode = 'selling'

    def move(self):
        current_pos = self.pos

        city_center = self.model.city_network.points_of_interest["city_center"]
        market = self.model.city_network.points_of_interest["market"]

        if self.mode == 'selling':
            selling_resources = self.need_to_sell()
            if not selling_resources:
                self.toggle_mode()
            else:
                self.destination = market

        elif self.mode == 'buying':
            buying_resources = self.need_to_buy()
            if not buying_resources:
                self.toggle_mode()
            else:
                self.destination = city_center

        else:
            self.destination = self.home_location

        if self.destination and self.destination != self.pos:
            return self.execute_pathfinding_move(current_pos, self.destination)
        return False

    def need_to_buy(self):
        if self.wealth <= 0 or sum(self.inventory.values()) >= self.max_inventory:
            return False

        buying_resources = []
        resources_available = [
            resource
            for resource, amount in self.model.economy.resource_pools.items()
            if resource in trader_global_var['buy'] and amount >= 1
        ]

        if not resources_available:
            return False

        for resource in resources_available:
            base_price = self.model.economy.base_prices.get(resource)
            current_price = self.model.economy.calculate_price(resource)

            buying_price = round(base_price * self.buying_aggression, 3)
            if current_price <= buying_price:
                buying_resources.append(resource)

        if not buying_resources:
            return False
        return buying_resources

    def need_to_sell(self):
        if sum(self.inventory.values()) <= 0:
            return False

        selling_resources = []
        resource_available = [
            resource
            for resource, amount in self.inventory.items()
            if resource in trader_global_var['sell'] and amount >= 1
        ]

        if not resource_available:
            return False

        for resource in resource_available:
            base_price = self.model.economy.base_price[resource]
            current_price = self.model.economy.calculate_price(resource)
            selling_price = round(base_price * self.selling_aggression, 3)
            if current_price >= selling_price:
                selling_resources.append(resource)

        if not selling_resources:
            return False
        return selling_resources

    def buy_goods(self):
        market = self.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = self.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        buying_resources = self.need_to_buy()
        if not buying_resources:
            self.toggle_mode()
            return

        buy_candidates = []
        for resource in buying_resources:
            current_price = self.model.economy.calculate_price(resource)
            buy_candidates.append((resource, current_price))
        buy_candidates.sort(key=lambda x: x[1])

        for resource, current_price in buy_candidates:
            if self.wealth <= 0 or sum(self.inventory.values()) >= self.max_inventory:
                break

            if resource in market_goods and self.pos != market:
                continue
            elif resource in city_center_goods and self.pos != city_center:
                continue

            max_buy_by_power = int(self.buying_power.get(resource, 0) / current_price) if current_price > 0 else 0
            max_buy_by_wealth = int(self.wealth / current_price) if current_price > 0 else 0
            max_buy_by_inventory = self.max_inventory - sum(self.inventory.values())

            quantity = min(max_buy_by_power, max_buy_by_wealth, max_buy_by_inventory)

            if quantity > 0:
                buying_quantity = self.model.economy.request_resource(resource, quantity)
                if buying_quantity > 0:
                    cost = current_price * buying_quantity
                    self.wealth -= cost
                    self.model.economy.wealth += cost
                    self.inventory[resource] = self.inventory.get(resource, 0) + buying_quantity

        if sum(self.inventory.values()) >= self.max_inventory * self.inventory_margin or self.wealth < self.wealth_margin:
            self.toggle_mode()

    def sell_goods(self):
        market = self.model.city_network.points_of_interest["market"]
        market_goods = location_global_var['market']

        city_center = self.model.city_network.points_of_interest["city_center"]
        city_center_goods = location_global_var['city_center']

        selling_resources = self.need_to_sell()
        if not selling_resources:
            self.toggle_mode()
            return

        sell_candidates = []
        for resource in selling_resources:
            current_price = self.model.economy.calculate_price(resource)
            sell_candidates.append((resource, current_price))
        sell_candidates.sort(key=lambda x: x[1], reverse=True)

        for resource, current_price in sell_candidates:
            if sum(self.inventory.values()) <= 0:
                break

            if resource in market_goods and self.pos != market:
                continue
            elif resource in city_center_goods and self.pos != city_center:
                continue

            quantity = min(self.inventory.get(resource, 0), self.selling_power.get(resource, 0))

            if quantity > 0:
                selling_quantity = self.model.economy.add_resource(resource, quantity)
                if selling_quantity > 0:
                    income = current_price * selling_quantity
                    self.wealth += income
                    self.model.economy.wealth -= income
                    self.inventory[resource] -= selling_quantity

    def step(self):
        super().step()
        if not self.alive:
            return

        market = self.model.city_network.points_of_interest["market"]
        city_center = self.model.city_network.points_of_interest["city_center"]

        self.update_agent_config()
        is_moving = self.move()

        if not is_moving:
            if self.pos == market:
                self.sell_goods()
                self.buy_goods()
            elif self.pos == city_center:
                self.sell_goods()
                self.buy_goods()
