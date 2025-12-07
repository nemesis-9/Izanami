from core.agents.agent import BaseAgent
from core.config.global_config import global_var

global_variables = global_var()
location_global_var = global_variables.get('location_items', {})
crafter_global_var = global_variables.get('agent_items', {}).get('crafter', {})


class Craftsman(BaseAgent):
    def __init__(self, model, wealth, initial_craftsman_config):
        super().__init__(model, wealth, "Craftsman")

        self.inventory = {"iron": 20, "copper": 15}
        self.crafting_rate = self.random.randrange(4, 10)

        self.has_craft_plot = True
        self.path = None
        self.home_location = None
        self.destination = None
        self.mode = 'crafting'

        self.max_inventory = initial_craftsman_config.get("max_inventory", 0)
        self.buying_power = initial_craftsman_config.get("buying_power", {})
        self.selling_power = initial_craftsman_config.get("selling_power", {})
        self.inventory_margin = initial_craftsman_config.get("inventory_margin", 0)
        self.wealth_margin = initial_craftsman_config.get("wealth_margin", 0)

    def update_agent_config(self):
        super().update_agent_config()
        crafter_vars = self.model.crafter_variables
        self.max_inventory = crafter_vars.get("max_inventory", 0)
        self.buying_power = crafter_vars.get("buying_power", {})
        self.selling_power = crafter_vars.get("selling_power", {})
        self.inventory_margin = crafter_vars.get("inventory_margin", 0)
        self.wealth_margin = crafter_vars.get("wealth_margin", 0)


    def toggle_mode(self):
        if self.mode == 'buying':
            self.mode = 'crafting'
        elif self.mode == 'crafting':
            self.mode = 'selling'
        elif self.mode == 'selling':
            self.mode = 'buying'
        else:
            self.mode = 'crafting'

    def move(self):
        current_pos = self.pos

        city_center = self.model.city_network.points_of_interest["city_center"]
        market = self.model.city_network.points_of_interest["market"]

        if self.mode == 'selling':
            selling_resources = self.need_to_sell()
            if not selling_resources:
                self.toggle_mode()
            else:
                self.destination = city_center

        elif self.mode == 'buying':
            buying_resources = self.need_to_buy()
            if not buying_resources:
                self.toggle_mode()
            else:
                self.destination = market

        else:
            self.destination = self.home_location

        if self.destination and self.destination != self.pos:
            return self.execute_pathfinding_move(current_pos, self.destination)
        return False

    def need_to_buy(self):
        if self.wealth <= 0 or sum(self.inventory.values()) >= self.max_inventory:
            return False

        buying_resources = [
            resource
            for resource, amount in self.model.economy.resource_pools.items()
            if resource in crafter_global_var['buy'] and amount >= 1 and self.inventory.get(resource, 0) < self.buying_power.get(resource, 0)
        ]

        if not buying_resources:
            return False
        return buying_resources

    def need_to_sell(self):
        if sum(self.inventory.values()) <= 0:
            return False

        selling_resources = [
            resource
            for resource, amount in self.inventory.items()
            if resource in crafter_global_var['sell'] and amount > self.selling_power.get(resource, 0)
        ]

        if not selling_resources:
            return False
        return selling_resources

    def buy_materials(self):
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
            if resource in city_center_goods and self.pos != city_center:
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
        sell_candidates.sort(key=lambda x: x[1])

        for resource, current_price in sell_candidates:
            if sum(self.inventory.values()) <= 0:
                break

            if resource in market_goods and self.pos != market:
                continue
            if resource in city_center_goods and self.pos != city_center:
                continue

            quantity = min(self.inventory.get(resource, 0), self.selling_power.get(resource, 0))

            if quantity > 0:
                selling_quantity = self.model.economy.add_resource(resource, quantity)
                if selling_quantity > 0:
                    income = current_price * selling_quantity
                    self.wealth += income
                    self.model.economy.wealth -= income
                    self.inventory[resource] -= selling_quantity

    # TODO: Create craft function
    def craft(self):
        return True

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
                self.buy_materials()
            elif self.pos == city_center:
                self.sell_goods()
            elif self.pos == self.home_location:
                self.craft()
