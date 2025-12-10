class CrafterTravel:
    def move(self, crafter):
        current_pos = crafter.pos

        city_center = crafter.model.city_network.points_of_interest["city_center"]
        market = crafter.model.city_network.points_of_interest["market"]

        if crafter.mode == 'selling':
            selling_resources = crafter.selling_logic.need_to_sell(crafter)
            if not selling_resources:
                crafter.toggle_mode()
            else:
                crafter.destination = city_center

        elif crafter.mode == 'buying':
            buying_resources = crafter.buying_logic.need_to_buy(crafter)
            if not buying_resources:
                crafter.toggle_mode()
            else:
                crafter.destination = market

        else:
            crafter.destination = crafter.home_location

        if crafter.destination and crafter.destination != crafter.pos:
            return crafter.execute_pathfinding_move(current_pos, crafter.destination)
        return False
