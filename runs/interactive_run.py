from core.models.world import WorldModel
from core.models.city import CityModel

if __name__ == '__main__':
    print("--- Starting City Simulation Test ---")

    world = WorldModel(cities=1)

    city_instance = CityModel(
        1,
        world,
        100,
        100,
        5
    )
    world.city_models.append(city_instance)

    for i in range(10):
        print(f"\nWorld Step {world.steps + 1}:")
        world.step()

    print("\n--- Simulation Test Complete ---")