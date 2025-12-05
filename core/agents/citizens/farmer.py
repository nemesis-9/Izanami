from core.agents.agent import BaseAgent


class Farmer(BaseAgent):
    def __init__(self, model, wealth):
        self.agent_type = "Farmer"
        super().__init__(model, wealth)

        self.food_production_rate = self.random.randrange(3,7)
        self.food_consumption_rate = 2
        self.has_farm_plot = True
        self.path = None

    def produce(self):
        production_amount = self.food_production_rate
        current_price = self.model.economy.calculate_price("food")
        self.model.economy.add_resource("food", production_amount)
        income = production_amount * current_price
        self.wealth += income

    def consume(self):
        food_needed = self.food_consumption_rate
        food_gained = self.model.economy.request_resource("food", food_needed)

        if food_gained < food_needed:
            self.alive = False
            self.model.grid.remove_agent(self)
            print(f"Farmer {self.unique_id} starved to death")
            return False
        return True

    def move(self):
        current_pos = self.pos
        destination_pos = self.model.city_network.points_of_interest["market"]
        return self.execute_pathfinding_move(current_pos, destination_pos)

    def step(self):
        if not self.alive:
            return

        self.move()

        if self.path is None or len(self.path) <= 1:
            self.produce()
            self.consume()

        super().step()
