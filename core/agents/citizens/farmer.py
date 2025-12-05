from core.agents.agent import BaseAgent


class Farmer(BaseAgent):
    def __init__(self, model, wealth):
        super().__init__(model, wealth, "Farmer")

        self.food_production_rate = self.random.randrange(3,7)

        self.has_farm_plot = True
        self.path = None

        self.goods_to_sell = 0
        self.selling_threshold = 10

        self.home_location = None
        self.destination = None

    def move(self):
        current_pos = self.pos
        market = self.model.city_network.points_of_interest["market"]

        if self.goods_to_sell > self.selling_threshold:
            self.destination = market
        elif self.pos == market:
            self.destination = self.home_location
        else:
            self.destination = self.home_location

        if self.destination and self.destination != current_pos:
            return self.execute_pathfinding_move(current_pos, self.destination)
        return False

    def produce(self):
        production_amount = self.food_production_rate
        self.goods_to_sell += production_amount

    def sell(self):
        if self.goods_to_sell > 0:
            current_price = self.model.economy.calculate_price("food")
            income = current_price * self.goods_to_sell
            self.model.economy.add_resource("food", self.goods_to_sell)
            self.wealth += income
            self.goods_to_sell = 0

    def step(self):
        if not self.alive:
            return

        self.consume()

        is_moving = self.move()

        if not is_moving:
            if self.pos == self.home_location:
                self.produce()
            elif self.pos == self.model.city_network.points_of_interest["market"]:
                self.sell()

        super().step()
