class TraderTravel:
    def move(self, trader):
        current_pos = trader.pos

        market = trader.model.city_network.points_of_interest["market"]
        city_center = trader.model.city_network.points_of_interest["city_center"]

        if trader.mode == 'selling':
            selling_resources = trader.selling_logic.need_to_sell(trader)
            if not selling_resources:
                trader.toggle_mode()
            else:
                trader.destination = market

        elif trader.mode == 'buying':
            buying_resources = trader.buying_logic.need_to_buy(trader)
            if not buying_resources:
                trader.toggle_mode()
            else:
                trader.destination = city_center

        else:
            trader.destination = trader.home_location

        if trader.destination and trader.destination != trader.pos:
            return trader.execute_pathfinding_move(current_pos, trader.destination)
        return False
