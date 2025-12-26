class CrafterTravel:
    def __init__(self, crafter):
        self.crafter = crafter

    def move(self):
        current_pos = self.crafter.pos

        city_center = self.crafter.model.city_network.points_of_interest["city_center"]
        market = self.crafter.model.city_network.points_of_interest["market"]

        if self.crafter.action == "buy":
            destination = market
        elif self.crafter.action == "sell":
            destination = city_center
        elif self.crafter.action == "craft":
            destination = self.crafter.home_location
        else:
            return False

        if destination != current_pos:
            return self.crafter.execute_pathfinding_move(current_pos, destination)

        return False
