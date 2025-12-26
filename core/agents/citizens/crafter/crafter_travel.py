from core.agents.base.agent_travel import AgentTravel


class CrafterTravel(AgentTravel):
    def __init__(self, crafter):
        super().__init__(crafter)
        self.crafter = crafter

    def move(self):
        current_pos = self.crafter.pos

        city_center = self.crafter.model.city_network.points_of_interest["city_center"]
        market = self.crafter.model.city_network.points_of_interest["market"]

        if self.crafter.destination is None:
            if self.crafter.action == "buy":
                self.crafter.destination = market
            elif self.crafter.action == "sell":
                self.crafter.destination = city_center
            elif self.crafter.action == "craft":
                self.crafter.destination = self.crafter.home_location

        if self.crafter.destination and self.crafter.destination != current_pos:
            return self.crafter.execute_pathfinding_move(
                current_pos, self.crafter.destination
            )

        return False
