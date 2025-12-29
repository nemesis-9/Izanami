class CrafterUtility:
    def __init__(self, crafter):
        self.crafter = crafter

    @staticmethod
    def clamp01(x):
        return max(0.0, min(1.0, x))

    def inventory_ratio(self):
        return self.clamp01(
            sum(self.crafter.inventory.values()) / max(1, self.crafter.max_inventory)
        )

    def wealth_ratio(self):
        return self.clamp01(
            self.crafter.wealth / max(1, self.crafter.wealth_margin)
        )

    def inventory_margin_ratio(self):
        return self.clamp01(self.crafter.inventory_margin)

    def inventory_pressure(self):
        margin = self.inventory_margin_ratio()
        excess = self.inventory_ratio() - margin
        return self.clamp01(excess / max(0.01, 1.0 - margin))

    def craft_utility(self):
        if (
                not self.crafter.crafting_logic.can_craft_anything()
                or sum(self.crafter.inventory.values()) >= self.crafter.max_inventory
        ):
            return 0.0

        return (1.0 - self.inventory_ratio()) * (1.0 - self.inventory_pressure())

    def sell_utility(self):
        if (
                not self.crafter.selling_logic.need_to_sell()
        ):
            return 0.0
        return self.inventory_pressure()

    def buy_utility(self):
        if not self.crafter.buying_logic.need_to_buy():
            return 0.0
        return (1.0 - self.inventory_ratio()) * self.wealth_ratio() * 0.5

    @staticmethod
    def idle_utility() -> float:
        return 0.05

    def decide_action(self):
        utilities = {
            "craft": self.craft_utility(),
            "sell": self.sell_utility(),
            "buy": self.buy_utility(),
            "idle": self.idle_utility(),
        }
        return max(utilities, key=utilities.get)
