class AgentConsumeLogic:
    def __init__(self, agent):
        self.agent = agent
        self.food_needed = 0
        self.replenishment_buffer = 0

    def buy_foods(self):
        food_to_request = self.food_needed - self.agent.personal_food_supply
        amount_to_acquire = food_to_request + self.replenishment_buffer
        current_price = self.agent.model.economy.calculate_price("food")
        total_cost = amount_to_acquire * current_price
        minimum_cost = food_to_request * current_price

        if self.agent.wealth >= minimum_cost:

            if self.agent.wealth >= total_cost:
                amount_to_buy = amount_to_acquire
            else:
                amount_to_buy = food_to_request

            food_gained = self.agent.model.economy.request_resource("food", amount_to_buy)
            if food_gained > 0:
                actual_cost = food_gained * current_price
                self.agent.wealth -= actual_cost
                self.agent.model.economy.wealth += actual_cost
                self.agent.personal_food_supply += food_gained - self.food_needed
                return True

            else:
                self.agent.hp -= self.agent.hp_starve_penalty
                return False

    def consume(self):
        self.food_needed = self.agent.food_consumption_rate
        self.replenishment_buffer = self.agent.replenishment_buffer

        if self.agent.personal_food_supply >= self.food_needed:
            self.agent.personal_food_supply -= self.food_needed
            return True

        else:
            buying_foods = self.buy_foods()
            if buying_foods:
                return True

            else:
                self.agent.hp -= self.agent.hp_starve_penalty
                return False
