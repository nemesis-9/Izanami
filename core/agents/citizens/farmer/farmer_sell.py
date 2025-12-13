class FarmerSell:
    def __init__(self, farmer):
        self.farmer = farmer

    def sell_goods(self):
        current_price = self.farmer.model.economy.calculate_price("food")
        surplus = self.farmer.personal_food_supply - self.farmer.survival_buffer
        if surplus > 0:
            selling_quantity = self.farmer.model.economy.add_resource("food", surplus)
            if selling_quantity > 0:
                return [("food", selling_quantity)]
