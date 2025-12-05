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

        self.food_consumption_rate = 2
        self.personal_food_supply = 10

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
        if self.personal_food_supply >= food_needed:
            self.personal_food_supply -= food_needed
            return True
        else:
            food_to_request = food_needed - self.personal_food_supply
            food_gained = self.model.economy.request_resource("food", food_to_request)

            if food_gained < food_to_request:
                self.alive = False
                print(f"{self.agent_type} {self.unique_id} starved to death.")
                return False

            self.personal_food_supply = 0
            return True

    def step(self):
        self.age += 1
        if not self.consume():
            return
        pass
