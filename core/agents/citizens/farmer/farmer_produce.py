class FarmerProduce:
    def produce(self, farmer):
        production_amount = farmer.food_production_rate
        farmer.personal_food_supply += production_amount
