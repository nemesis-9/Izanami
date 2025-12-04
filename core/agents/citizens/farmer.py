from core.agents.agent import BaseAgent


class Farmer(BaseAgent):
    def __init__(self, model, wealth):
        self.agent_type = "Farmer"
        super().__init__(model, wealth)

        self.food_production_rate = self.random.randrange(3,7)
        self.food_consumption_rate = 2
        self.has_farm_plot = True

    def produce(self):
        production_amount = self.food_production_rate
        self.model.economy.add_resource("food", production_amount)
        self.wealth += production_amount * 0.5

    def consume(self):
        food_needed = self.food_consumption_rate
        food_gained = self.model.economy.request_resources("food", food_needed)

        if food_gained < food_needed:
            self.alive = False
            self.model.grid.remove_agent(self)
            print(f"Farmer {self.unique_id} starved to death")
            return False

        return True

    def step(self):
        if not self.alive:
            return

        self.produce()
        self.consume()

        super().step()
