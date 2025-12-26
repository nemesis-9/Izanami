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
        current_edge = (current_pos, next_pos)

        food_stock = self.agent.inventory.get("food", 0)
        cost = self.agent.travel_food_cost

        if food_stock >= cost:
            self.agent.inventory["food"] = round(food_stock - cost, 3)
        else:
            self.agent.hp -= self.agent.hp_move_penalty

        if hasattr(self.agent.model.city_network, 'record_usage'):
            self.agent.model.city_network.record_usage(current_edge[0], current_edge[1])

        self.agent.model.grid.move_agent(self.agent, next_pos)
        self.agent.location = next_pos
        self.agent.path = self.agent.path[1:]
        return True

