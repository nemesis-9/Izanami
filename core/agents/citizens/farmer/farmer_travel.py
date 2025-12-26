from core.agents.base.agent_travel import AgentTravel


class FarmerTravel(AgentTravel):
    def __init__(self, farmer):
        super().__init__(farmer)
        self.farmer = farmer

    def move(self):
        current_pos = self.farmer.pos
        if self.farmer.destination and self.farmer.destination != current_pos:
            return self.farmer.execute_pathfinding_move(current_pos, self.farmer.destination)
        return False
