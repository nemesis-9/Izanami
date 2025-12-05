from core.agents.agent import BaseAgent


class Trader(BaseAgent):
    def __init__(self, model, wealth):
        self.agent_type = 'Trader'
        super().__init__(model, wealth)

        self.buying_power = 10
        self.inventory = {"food": 0}
        self.path = None


    def move(self):
        current_pos = self.pos
        destination_pos = self.model.city_network.points_of_interest["city_center"]

        return self.execute_pathfinding_move(current_pos, destination_pos)

    def trade(self):
        if self.pos == self.model.city_network.points_of_interest["city_center"]:
            resource_to_buy = "food"
            amount_to_buy = 5
            price_per_unit = self.model.economy.calculate_price(resource_to_buy)
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
