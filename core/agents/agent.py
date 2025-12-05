from mesa import Agent


class BaseAgent(Agent):
    def __init__(self, model, wealth, agent_type):
        super().__init__(model)
        self.age = 0
        self.wealth = wealth
        self.agent_type = agent_type
        self.alive = True

        self.location = None
        self.path = None

        self.food_consumption_rate = 1
        self.personal_food_supply = 20

    def execute_pathfinding_move(self, current_pos, destination_pos):
        if current_pos == destination_pos:
            self.path = None
            return False

        if self.path is None or len(self.path) < 2:
            self.path = self.model.city_network.get_path(current_pos, destination_pos)
            if self.path is None or len(self.path) < 2:
                return False

        next_pos = self.path[1]
        self.model.grid.move_agent(self, next_pos)
        self.location = next_pos
        self.path = self.path[1:]
        return True

    def consume(self):
        food_needed = self.food_consumption_rate
        replenishment_buffer = 5  # Amount of food the agent tries to buy

        if self.personal_food_supply >= food_needed:
            self.personal_food_supply -= food_needed
            return True

        else:
            food_to_request = food_needed - self.personal_food_supply
            amount_to_acquire = food_to_request + replenishment_buffer
            current_price = self.model.economy.calculate_price("food")
            total_cost = amount_to_acquire * current_price      # for amount_to_acquire
            minimum_cost = food_to_request * current_price      # for food_to_request

            if self.wealth >= minimum_cost:

                if self.wealth >= total_cost:
                    amount_to_buy = amount_to_acquire
                else:
                    amount_to_buy = food_to_request

                food_gained = self.model.economy.request_resource("food", amount_to_buy)
                if food_gained > 0:
                    actual_cost = food_gained * current_price
                    self.wealth -= actual_cost
                    self.personal_food_supply += food_gained - food_needed
                    return True

                else:
                    self.alive = False
                    print(f"[{self.unique_id}] {self.agent_type} starved to death - market empty")
                    return False

            # Agent doesn't have enough money
            else:
                self.alive = False
                print(f"[{self.unique_id}] {self.agent_type} starved to death - no enough money")
                return False

    def step(self):
        self.age += 1
        if not self.consume():
            return
        pass
