from core.agents.agent import BaseAgent


class Farmer(BaseAgent):
    def __init__(self, model, wealth, initial_farmer_config):
        super().__init__(model, wealth, "Farmer")

        self.food_production_rate = self.random.randrange(3, 7)

        self.has_farm_plot = True
        self.path = None

        self.surplus_threshold = initial_farmer_config.get("surplus_threshold", 0)
        self.survival_buffer = initial_farmer_config.get("survival_buffer", 0)

        self.home_location = None
        self.destination = None

    def update_agent_config(self):
        super().update_agent_config()
        farmer_vars = self.model.farmer_variables
        self.surplus_threshold = farmer_vars.get("surplus_threshold", 0)
        self.survival_buffer = farmer_vars.get("survival_buffer", 0)

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
        current_price = self.model.economy.calculate_price("food")
        surplus = self.personal_food_supply - self.survival_buffer
        if surplus > 0:
            selling_quantity = self.model.economy.add_resource("food", surplus)
            if selling_quantity > 0:
                income = current_price * selling_quantity
                self.wealth += income
                self.model.economy.wealth -= income
                self.personal_food_supply -= selling_quantity

    def step(self):
        super().step()
        if not self.alive:
            return

        self.update_agent_config()
        is_moving = self.move()

        if not is_moving:
            if self.pos == self.home_location:
                self.produce()
            elif self.pos == self.model.city_network.points_of_interest["market"]:
                self.sell()

