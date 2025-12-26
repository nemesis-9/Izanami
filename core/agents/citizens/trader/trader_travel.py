from core.agents.base.agent_travel import AgentTravel


class TraderTravel(AgentTravel):
    def __init__(self, trader):
        super().__init__(trader)
        self.trader = trader

    def get_nearest_destination(self, destinations):
        if not destinations:
            return None

        current_pos = self.trader.pos

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        return min(destinations, key=lambda d: manhattan(current_pos, d))

    def move(self):
        if not self.trader.destination:
            return False

        if self.trader.destination != self.trader.pos:
            return self.trader.execute_pathfinding_move(
                self.trader.pos,
                self.trader.destination
            )

        return False
