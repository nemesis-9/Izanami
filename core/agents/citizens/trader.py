from core.agents.agent import BaseAgent


class Trader(BaseAgent):
    def __init__(self, model, wealth):
        super().__init__(model, wealth, "Trader")

        self.inventory = {"food": 0}
        self.max_inventory = 30
        self.buying_power = 10          # Max units of goods they can try to buy
        self.buying_aggression = 0.8    # Buy if the current price is 80% or less of base price

        self.path = None
        self.destination = None

    def move(self):
        current_pos = self.pos
        city_center = self.model.city_network.points_of_interest["city_center"]

        return self.execute_pathfinding_move(current_pos, self.destination)

    def trade(self):
        if self.pos == self.model.city_network.points_of_interest["city_center"]:
            resource_to_buy = "food"
            current_food_in_stock = self.inventory[resource_to_buy]
            base_price = self.model.economy.base_food_price
            price_per_unit = self.model.economy.calculate_price(resource_to_buy)

            if current_food_in_stock >= self.max_inventory:
                return
            if price_per_unit >= base_price * self.buying_aggression:
                return

            amount_to_buy = min(
                self.buying_power,
                self.max_inventory - current_food_in_stock
            )
            if amount_to_buy <= 0:
                return
            total_cost = price_per_unit * amount_to_buy

            if self.wealth >= total_cost:
                food_gained = self.model.economy.request_resource(resource_to_buy, amount_to_buy)
                if food_gained > 0:
                    self.wealth -= total_cost
                    self.model.economy.add_resource("gold", total_cost)
                    self.inventory[resource_to_buy] += food_gained
            else:
                pass

    def step(self):
        if not self.alive:
            return
        self.move()
        if self.path is None or len(self.path) <= 1:
            self.trade()
        super().step()
