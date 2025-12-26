class FarmerProduce:
    def __init__(self, farmer):
        self.farmer = farmer

    def produce(self):
        self.farmer.harvest_progress += 1

        if self.farmer.harvest_progress >= self.farmer.max_harvest_progress:
            production_amount = self.farmer.food_production_rate
            current_food = self.farmer.inventory.get("food", 0)

            self.farmer.inventory["food"] = round(current_food + production_amount, 3)
            self.farmer.harvest_progress = 0
