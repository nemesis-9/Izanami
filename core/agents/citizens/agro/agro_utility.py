class AgroUtility:
    def __init__(self, agro):
        self.agro = agro

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def inventory_ratio(self) -> float:
        max_inv = max(1.0, self.agro.max_inventory)
        current_inv = sum(self.agro.inventory.values())
        return self.clamp01(current_inv / max_inv)

    def produce_utility(self) -> float:
        if not self.agro.has_farm_plot or self.inventory_ratio() >= 1.0:
            return 0.0

        return self.clamp01((1.0 - self.inventory_ratio()) * 0.8 + 0.1)

    def sell_utility(self) -> float:
        food_amount = self.agro.inventory.get("food", 0)
        if food_amount <= self.agro.personal_minimum and not self.agro.is_emergency:
            return 0.0

        surplus = max(0, food_amount - self.agro.personal_minimum)
        surplus_ratio = surplus / max(1, self.agro.selling_margin)
        emergency_boost = 0.5 if self.agro.is_emergency else 0.0

        return self.clamp01(surplus_ratio + emergency_boost)

    def travel_utility(self) -> float:
        market_pos = self.agro.model.city_network.points_of_interest.get("market")
        produce_needed = self.produce_utility()
        sell_needed = self.sell_utility()

        if sell_needed > 0.7 and self.agro.pos != market_pos:
            return 0.8
        if produce_needed > 0.6 and self.agro.pos != self.agro.home_location:
            return 0.7
        return 0.1

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self) -> str:
        utilities = {
            "produce": self.produce_utility(),
            "sell": self.sell_utility(),
            "travel": self.travel_utility(),
            "idle": self.idle_utility(),
        }
        return max(utilities, key=utilities.get)
