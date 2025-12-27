class AgentConsumeLogic:
    def __init__(self, agent):
        self.agent = agent

    def buy_foods(self, food_needed):
        replenishment = self.agent.replenishment_buffer
        total_to_request = food_needed + replenishment

        current_price = self.agent.model.economy.current_price("food")

        if self.agent.wealth < (food_needed * current_price):
            return False

        amount_to_buy = total_to_request if self.agent.wealth >= (total_to_request * current_price) else food_needed
        food_gained = self.agent.model.economy.request_resource("food", amount_to_buy)

        if food_gained > 0:
            actual_cost = food_gained * current_price
            self.agent.wealth -= actual_cost
            self.agent.model.economy.wealth += actual_cost
            self.agent.inventory["food"] = self.agent.inventory.get("food", 0) + food_gained
            return True

        return False

    def consume(self):
        food_needed = self.agent.food_consumption_rate

        if self.agent.inventory.get("food", 0) < food_needed:
            self.buy_foods(food_needed)

        if self.agent.inventory.get("food", 0) >= food_needed:
            self.agent.inventory["food"] = round(self.agent.inventory["food"] - food_needed, 3)
            return True

        else:
            self.agent.hp -= self.agent.hp_starve_penalty
            return False
