class FarmerProduce:
    def __init__(self, farmer):
        self.farmer = farmer

    def produce(self):
        production_amount = self.farmer.food_production_rate
        self.farmer.personal_food_supply += production_amount
