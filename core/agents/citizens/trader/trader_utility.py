class TraderUtility:
    def __init__(self, trader):
        self.trader = trader

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def inventory_ratio(self) -> float:
        max_inv = max(1, self.trader.max_inventory)
        return self.clamp01(
            sum(self.trader.inventory.values()) / max_inv
        )

    def wealth_ratio(self) -> float:
        margin = max(1, self.trader.wealth_margin)
        return self.clamp01(
            self.trader.wealth / margin
        )

    def inventory_pressure(self) -> float:
        inv = self.inventory_ratio()
        margin = self.trader.inventory_margin
        if inv <= margin:
            return 0.0
        return self.clamp01((inv - margin) / max(0.01, 1.0 - margin))

    def buy_utility(self) -> float:
        return (
            self.trader.buying_aggression
            * self.wealth_ratio()
            * (1.0 - self.inventory_ratio())
        )

    def sell_utility(self) -> float:
        return (
            self.trader.selling_aggression
            * max(self.inventory_ratio(), self.inventory_pressure())
        )

    def travel_utility(self) -> float:
        poi = self.trader.model.city_network.points_of_interest.values()
        return 0.4 if self.trader.pos not in poi else 0.0

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self) -> str:
        utilities = {
            "buy": self.buy_utility(),
            "sell": self.sell_utility(),
            "travel": self.travel_utility(),
            "idle": self.idle_utility(),
        }

        return max(utilities, key=utilities.get)
