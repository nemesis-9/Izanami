class AgentTravel:
    def __init__(self, agent):
        self.agent = agent

    def pathfinding_move(self, current_pos, destination_pos):
        if current_pos == destination_pos:
            self.agent.path = None
            return False

        if self.agent.path is None or len(self.agent.path) < 2:
            self.agent.path = self.agent.model.city_network.get_path(current_pos, destination_pos)
            if self.agent.path is None or len(self.agent.path) < 2:
                return False

        next_pos = self.agent.path[1]

        if self.agent.personal_food_supply > self.agent.travel_food_cost:
            self.agent.personal_food_supply -= self.agent.travel_food_cost
            self.agent.model.grid.move_agent(self.agent, next_pos)
            self.agent.location = next_pos
            self.agent.path = self.agent.path[1:]
            return True

        else:
            return False
