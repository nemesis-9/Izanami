class AgentTravel:
    def pathfinding_move(self, agent, current_pos, destination_pos):
        if current_pos == destination_pos:
            agent.path = None
            return False

        if agent.path is None or len(agent.path) < 2:
            agent.path = agent.model.city_network.get_path(current_pos, destination_pos)
            if agent.path is None or len(agent.path) < 2:
                return False

        next_pos = agent.path[1]

        if agent.personal_food_supply > agent.travel_food_cost:
            agent.personal_food_supply -= agent.travel_food_cost
            agent.model.grid.move_agent(agent, next_pos)
            agent.location = next_pos
            agent.path = agent.path[1:]
            return True

        else:
            return False
