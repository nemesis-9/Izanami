class FarmerUtility:
    def __init__(self, farmer):
        self.farmer = farmer

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def produce_utility(self) -> float:
        ratio = self.farmer.personal_food_supply / max(1, self.farmer.surplus_threshold)
        return self.clamp01(1.0 - ratio)

    def sell_utility(self) -> float:
        food_amount = self.farmer.inventory.get("food", 0)
        return self.clamp01(
            food_amount / self.farmer.survival_buffer
        )

    def travel_utility(self) -> float:
        market_pos = self.farmer.model.city_network.points_of_interest.get("market")
        produce_needed = self.produce_utility()
        sell_needed = self.sell_utility()

        if sell_needed > 0.5 and self.farmer.pos != market_pos:
            return 0.7
        if produce_needed > 0.5 and self.farmer.pos != self.farmer.home_location:
            return 0.6
        return 0.1

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self) -> str:
        utilities = {
            "produce": self.produce_utility(),
            "sell": self.sell_utility(),
            "travel": self.travel_utility(),
            "idle": self.idle_utility()
        }
        return max(utilities, key=utilities.get)
