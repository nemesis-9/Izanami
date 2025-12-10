class FarmerSell:
    def sell_goods(self, farmer):
        current_price = farmer.model.economy.calculate_price("food")
        surplus = farmer.personal_food_supply - farmer.survival_buffer
        if surplus > 0:
            selling_quantity = farmer.model.economy.add_resource("food", surplus)
            if selling_quantity > 0:
                return [("food", selling_quantity)]
