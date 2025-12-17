from core.agents.base.agent_travel import AgentTravel


class TraderTravel(AgentTravel):
    def __init__(self, trader):
        super().__init__(trader)
        self.trader = trader

    def move(self):
        current_pos = self.trader.pos

        market = self.trader.model.city_network.points_of_interest["market"]
        city_center = self.trader.model.city_network.points_of_interest["city_center"]

        if self.trader.mode == 'selling':
            selling_resources = self.trader.selling_logic.need_to_sell()
            if not selling_resources:
                self.trader.toggle_mode()
            else:
                self.trader.destination = market

        elif self.trader.mode == 'buying':
            buying_resources = self.trader.buying_logic.need_to_buy()
            if not buying_resources:
                self.trader.toggle_mode()
            else:
                self.trader.destination = city_center

        else:
            self.trader.destination = self.trader.home_location

        if self.trader.destination and self.trader.destination != self.trader.pos:
            return self.trader.execute_pathfinding_move(current_pos, self.trader.destination)
        return False
