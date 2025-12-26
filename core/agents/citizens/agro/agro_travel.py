from core.agents.base.agent_travel import AgentTravel


class AgroTravel(AgentTravel):
    def __init__(self, agro):
        super().__init__(agro)
        self.agro = agro

    def move(self):
        current_pos = self.agro.pos

        market = self.agro.model.city_network.points_of_interest["market"]

        if self.agro.action == "sell":
            self.agro.destination = market

        elif self.agro.action == "produce":
            self.agro.destination = self.agro.home_location

        else:
            self.agro.destination = None

        if self.agro.destination and self.agro.destination != current_pos:
            return self.agro.execute_pathfinding_move(
                current_pos, self.agro.destination
            )

        return False
