class FarmerSell:
    def __init__(self, farmer):
        self.farmer = farmer

    def sell_goods(self):
        resource = 'food'
        surplus = self.farmer.personal_food_supply - self.farmer.survival_buffer

        if surplus > 0:
            self.farmer.personal_food_supply -= surplus
            self.farmer.inventory[resource] = self.farmer.inventory[resource] + surplus
            goods_to_sell = self.farmer.inventory[resource]
            return [(resource, goods_to_sell)]

        return None
