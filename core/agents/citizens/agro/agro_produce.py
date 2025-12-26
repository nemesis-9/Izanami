class AgroProduce:
    def __init__(self, agro):
        self.agro = agro

    def produce(self):
        self.agro.harvest_progress += 1

        if self.agro.harvest_progress >= self.agro.max_harvest_progress:
            production_amount = self.agro.food_production_rate
            current_food = self.agro.inventory.get("food", 0)

            self.agro.inventory["food"] = round(current_food + production_amount, 3)
            self.agro.harvest_progress = 0
