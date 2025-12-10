from mesa import Agent
from agent_consume import AgentConsumeLogic
from agent_travel import AgentTravel


class BaseAgent(Agent):
    def __init__(self, model, wealth, agent_type):
        super().__init__(model)
        self.age = 0
        self.wealth = wealth
        self.agent_type = agent_type
        self.alive = True

        self.location = None
        self.path = None

        base_vars = model.base_variables

        self.personal_food_supply = base_vars.get("personal_food_supply", 0)
        self.food_consumption_rate = base_vars.get("food_consumption_rate", 1)
        self.travel_food_cost = base_vars.get("travel_food_cost", 0.0)
        self.replenishment_buffer = base_vars.get("replenishment_buffer", 0)

        self.consume_logic = AgentConsumeLogic()
        self.travel_logic = AgentTravel()

    def update_agent_config(self):
        base_vars = self.model.base_variables
        self.food_consumption_rate = base_vars.get("food_consumption_rate", 1)
        self.travel_food_cost = base_vars.get("travel_food_cost", 0.0)
        self.replenishment_buffer = base_vars.get("replenishment_buffer", 0)

    def execute_pathfinding_move(self, current_pos, destination_pos):
        return self.travel_logic.pathfinding_move(self, current_pos, destination_pos)

    def step(self):
        self.update_agent_config()
        self.age += 1
        if not self.consume_logic.consume(self):
            return
        pass
