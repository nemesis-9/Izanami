class AgentConsumeLogic:
    def buy_foods(self, agent, food_needed, replenishment_buffer):
        food_to_request = food_needed - agent.personal_food_supply
        amount_to_acquire = food_to_request + replenishment_buffer
        current_price = agent.model.economy.calculate_price("food")
        total_cost = amount_to_acquire * current_price
        minimum_cost = food_to_request * current_price

        if agent.wealth >= minimum_cost:

            if agent.wealth >= total_cost:
                amount_to_buy = amount_to_acquire
            else:
                amount_to_buy = food_to_request

            food_gained = agent.model.economy.request_resource("food", amount_to_buy)
            if food_gained > 0:
                actual_cost = food_gained * current_price
                agent.wealth -= actual_cost
                agent.model.economy.wealth += actual_cost
                agent.personal_food_supply += food_gained - food_needed
                return True

            else:
                agent.alive = False
                print(f"[{agent.unique_id}] {agent.agent_type} starved to death - market empty")
                return False

    def consume(self, agent):
        food_needed = agent.food_consumption_rate
        replenishment_buffer = agent.replenishment_buffer

        if agent.personal_food_supply >= food_needed:
            agent.personal_food_supply -= food_needed
            return True

        else:
            buying_foods = self.buy_foods(agent, food_needed, replenishment_buffer)
            if buying_foods:
                return True

            else:
                agent.alive = False
                print(f"[{agent.unique_id}] {agent.agent_type} starved to death - no enough money")
                return False
