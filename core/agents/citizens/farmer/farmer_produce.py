class FarmerProduce:
    def __init__(self, farmer):
        self.farmer = farmer

    def produce(self):
        production_amount = self.farmer.food_production_rate
        self.farmer.inventory["food"] = self.farmer.inventory.get("food", 0) + production_amount
