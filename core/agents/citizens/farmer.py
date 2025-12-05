from core.agents.agent import BaseAgent


class Farmer(BaseAgent):
    def __init__(self, model, wealth):
        super().__init__(model, wealth, "Farmer")

        self.food_production_rate = self.random.randrange(3,7)

        self.has_farm_plot = True
        self.path = None

        self.surplus_threshold = 10      # Food amount needed for market trip
        self.survival_buffer = 10       # Minimum food to keep after selling

        self.home_location = None
        self.destination = None

    def move(self):
        current_pos = self.pos
        market = self.model.city_network.points_of_interest["market"]

        if self.personal_food_supply > self.surplus_threshold:
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
        self.personal_food_supply += production_amount

    def sell(self):
        surplus = self.personal_food_supply - self.survival_buffer
        if surplus > 0:
            current_price = self.model.economy.calculate_price("food")
            income = current_price * surplus
            self.model.economy.add_resource("food", surplus)
            self.wealth += income
            self.personal_food_supply = self.survival_buffer

    def step(self):
        if not self.alive:
            return

        is_moving = self.move()

        if not is_moving:
            if self.pos == self.home_location:
                self.produce()
            elif self.pos == self.model.city_network.points_of_interest["market"]:
                self.sell()

        super().step()
