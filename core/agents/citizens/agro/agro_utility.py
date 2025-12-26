class AgroUtility:
    def __init__(self, agro):
        self.agro = agro

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def inventory_ratio(self) -> float:
        max_inv = max(1, self.agro.max_inventory)
        current = sum(self.agro.inventory.values())
        return self.clamp01(current / max_inv)

    def food_surplus_ratio(self) -> float:
        food = self.agro.inventory.get("food", 0)
        surplus = max(0, food - self.agro.personal_minimum)
        return self.clamp01(
            surplus / max(1, self.agro.selling_margin)
        )

    def produce_utility(self) -> float:
        if not self.agro.has_farm_plot:
            return 0.0

        inv_pressure = self.inventory_ratio()
        base = (1.0 - inv_pressure)

        if self.agro.is_emergency:
            base *= 0.6

        return self.clamp01(base * 0.9 + 0.1)

    def sell_utility(self) -> float:
        if self.agro.inventory.get("food", 0) <= self.agro.personal_minimum:
            return 0.0

        surplus_drive = self.food_surplus_ratio()

        emergency_boost = 0.6 if self.agro.is_emergency else 0.0

        market = self.agro.model.city_network.points_of_interest["market"]
        market_penalty = 0.3 if self.agro.pos == market else 0.0

        return self.clamp01(
            surplus_drive + emergency_boost - market_penalty
        )

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self) -> str:
        utilities = {
            "produce": self.produce_utility(),
            "sell": self.sell_utility(),
            "idle": self.idle_utility(),
        }
        return max(utilities, key=utilities.get)
