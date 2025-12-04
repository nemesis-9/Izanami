from mesa import Model


class WorldModel(Model):
    def __init__(self, cities):
        super().__init__()
        self.city_models = []
        self.village_models = []
        self.running = True

        for i in range(cities):
            print(f"World: initiating City {i+1}")

    def step(self):
        for city in self.city_models:
            city.step()

        if self.steps % 100 == 0 and self.steps > 0:
            print(f"--- World Year {self.steps // 100} Checkpoint ---")
