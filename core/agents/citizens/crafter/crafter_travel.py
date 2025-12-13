class CrafterTravel:
    def __init__(self, crafter):
        self.crafter = crafter

    def move(self):
        current_pos = self.crafter.pos

        city_center = self.crafter.model.city_network.points_of_interest["city_center"]
        market = self.crafter.model.city_network.points_of_interest["market"]

        if self.crafter.mode == 'selling':
            selling_resources = self.crafter.selling_logic.need_to_sell()
            if not selling_resources:
                self.crafter.toggle_mode()
            else:
                self.crafter.destination = city_center

        elif self.crafter.mode == 'buying':
            buying_resources = self.crafter.buying_logic.need_to_buy()
            if not buying_resources:
                self.crafter.toggle_mode()
            else:
                self.crafter.destination = market

        else:
            self.crafter.destination = self.crafter.home_location

        if self.crafter.destination and self.crafter.destination != self.crafter.pos:
            return self.crafter.execute_pathfinding_move(current_pos, self.crafter.destination)
        return False
