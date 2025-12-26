class CrafterUtility:
    def __init__(self, crafter):
        self.crafter = crafter

    @staticmethod
    def clamp01(x: float) -> float:
        return max(0.0, min(1.0, x))

    def inventory_ratio(self) -> float:
        max_inv = max(1, self.crafter.max_inventory)
        return self.clamp01(
            sum(self.crafter.inventory.values()) / max_inv
        )

    def wealth_ratio(self) -> float:
        margin = max(1, self.crafter.wealth_margin)
        return self.clamp01(
            self.crafter.wealth / margin
        )

    def high_inventory_pressure(self) -> float:
        return self.clamp01(
            self.clamp01(
                self.inventory_ratio() / max(0.01, self.crafter.inventory_margin)
            )
        )

    def craft_utility(self) -> float:
        if not self.crafter.crafting_logic.can_craft_anything():
            return 0.0

        return (
            (1.0 - self.inventory_ratio())
            * (0.5 + 0.5 * self.wealth_ratio())
        )

    def sell_utility(self) -> float:
        if not self.crafter.selling_logic.need_to_sell():
            return 0.0

        return (
            self.high_inventory_pressure()
            * (1.0 - self.wealth_ratio())
        )

    def buy_utility(self) -> float:
        if self.crafter.wealth <= 0:
            return 0.0

        return (
            self.wealth_ratio()
            * (1.0 - self.inventory_ratio())
        )

    def travel_utility(self) -> float:
        poi = self.crafter.model.city_network.points_of_interest.values()
        return 0.3 if self.crafter.pos not in poi else 0.0

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self) -> str:
        utilities = {
            "craft": self.craft_utility(),
            "sell": self.sell_utility(),
            "buy": self.buy_utility(),
            "travel": self.travel_utility(),
            "idle": self.idle_utility(),
        }

        return max(utilities, key=utilities.get)
