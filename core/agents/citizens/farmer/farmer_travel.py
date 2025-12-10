class FarmerTravel:
    def move(self, farmer):
        current_pos = farmer.pos
        market = farmer.model.city_network.points_of_interest["market"]

        if farmer.personal_food_supply > farmer.surplus_threshold:
            farmer.destination = market
        elif farmer.pos == market:
            farmer.destination = farmer.home_location
        else:
            farmer.destination = farmer.home_location

        if farmer.destination and farmer.destination != current_pos:
            return farmer.execute_pathfinding_move(current_pos, farmer.destination)
        return False
