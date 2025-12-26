class FarmerUtility:
    def __init__(self, farmer):
        self.farmer = farmer

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def inventory_ratio(self) -> float:
        max_inv = max(1, self.farmer.max_inventory)
        current = sum(self.farmer.inventory.values())
        return self.clamp01(current / max_inv)

    def food_surplus_ratio(self) -> float:
        food = self.farmer.inventory.get("food", 0)
        surplus = max(0, food - self.farmer.personal_minimum)
        return self.clamp01(surplus / max(1, self.farmer.selling_margin))

    def produce_utility(self) -> float:
        if not self.farmer.has_farm_plot:
            return 0.0

        inv_ratio = self.inventory_ratio()
        base = (1.0 - inv_ratio)

        if self.farmer.pos != self.farmer.home_location:
            base += 0.3

        return self.clamp01(base)

    def sell_utility(self) -> float:
        surplus_ratio = self.food_surplus_ratio()
        if surplus_ratio <= 0:
            return 0.0

        market = self.farmer.model.city_network.points_of_interest["market"]
        base = surplus_ratio

        if self.farmer.pos == market:
            base *= 0.2

        return self.clamp01(base)

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
