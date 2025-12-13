class FarmerTravel:
    def __init__(self, farmer):
        self.farmer = farmer

    def move(self):
        current_pos = self.farmer.pos
        market = self.farmer.model.city_network.points_of_interest["market"]

        if self.farmer.personal_food_supply > self.farmer.surplus_threshold:
            self.farmer.destination = market
        elif self.farmer.pos == market:
            self.farmer.destination = self.farmer.home_location
        else:
            self.farmer.destination = self.farmer.home_location

        if self.farmer.destination and self.farmer.destination != current_pos:
            return self.farmer.execute_pathfinding_move(current_pos, self.farmer.destination)
        return False
