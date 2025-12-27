from mesa import Agent

from core.agents.base.agent_consume import AgentConsumeLogic
from core.agents.base.agent_travel import AgentTravel
from core.agents.base.agent_hp import AgentHP


class BaseAgent(Agent):
    def __init__(self, model, wealth, agent_type):
        super().__init__(model)
        self.age = 0
        self.wealth = wealth
        self.agent_type = agent_type
        self.alive = True
        self.memorial = False

        self.location = None
        self.path = None

        base_vars = model.base_variables

        self.hp = base_vars.get("initial_hp", 100)
        self.hp_min_margin = base_vars.get("hp_min_margin", 20)
        self.hp_starve_penalty = base_vars.get("hp_starve_penalty", 5)
        self.hp_move_penalty = base_vars.get("hp_move_penalty", 2)

        self.food_consumption_rate = base_vars.get("food_consumption_rate", 1)
        self.travel_food_cost = base_vars.get("travel_food_cost", 0.0)
        self.replenishment_buffer = base_vars.get("replenishment_buffer", 0)

        self.consume_logic = AgentConsumeLogic(self)
        self.travel_logic = AgentTravel(self)
        self.hp_logic = AgentHP(self)

    def update_agent_config(self):
        base_vars = self.model.base_variables
        self.food_consumption_rate = base_vars.get("food_consumption_rate", 1)
        self.travel_food_cost = base_vars.get("travel_food_cost", 0.0)
        self.replenishment_buffer = base_vars.get("replenishment_buffer", 0)

    def execute_pathfinding_move(self, current_pos, destination_pos):
        return self.travel_logic.pathfinding_move(current_pos, destination_pos)

    def step(self):
        if self.hp_logic.death_check():
            return

        self.update_agent_config()
        self.age += 1
        self.consume_logic.consume()

        if self.hp_logic.death_check():
            return

        if hasattr(self, 'destination') and self.destination:
            self.travel_logic.pathfinding_move(self.location, self.destination)
