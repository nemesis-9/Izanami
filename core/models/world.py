from mesa import Model
from core.models.city import CityModel


class WorldModel(Model):
    def __init__(self, cities, seasons=["Spring", "Summer", "Autumn", "Winter"], **city_kwargs):
        super().__init__()
        self.cities_count = cities
        self.city_models = []
        self.village_models = []
        self.running = True

        for i in range(cities):
            print(f"World: initiating City {i+1}")
            city = CityModel(
                unique_id=i+1,
                parent_world=self,
                seasons=seasons,
                **city_kwargs
            )
            self.city_models.append(city)

    def step(self):
        for city in self.city_models:
            city.step()

        if self.steps % 100 == 0 and self.steps > 0:
            print(f"--- World Year {self.steps // 100} Checkpoint ---")

    def run_model(self, step_count=1000):
        for i in range(step_count):
            self.step()
