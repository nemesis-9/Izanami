class FarmerSell:
    def __init__(self, farmer):
        self.farmer = farmer

    def sell_goods(self):
        resource = 'food'

        surplus = self.farmer.inventory.get(resource, 0) - self.farmer.survival_buffer

        if surplus > 0:
            self.farmer.inventory[resource] -= surplus
            return [(resource, surplus)]

        return None
