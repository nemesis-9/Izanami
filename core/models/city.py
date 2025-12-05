from mesa import Model, DataCollector
from mesa.space import MultiGrid
from core.models.world import WorldModel
from core.subsystems.economy import Economy
from core.agents.citizens.farmer import Farmer
from core.agents.citizens.trader import Trader
from core.spaces.city_network import CityNetwork


class CityModel(Model):
    def __init__(self, unique_id, parent_world, width=100, height=100, agents=10, farmers=5, traders=5, model_reporters=None, agent_reporters=None):
        super().__init__()
        self.unique_id = unique_id
        self.parent_world = parent_world

        self.grid = MultiGrid(width, height, torus=False)
        self.economy = Economy(self)
        self.city_network = CityNetwork(self, width, height)

        if model_reporters is None:
            model_reporters = {
                "TotalAgents": lambda m: len(m.agents),
                "FoodPool": lambda m: m.economy.resource_pools.get("food", 0),
                "TotalWealth": lambda m: sum(a.wealth for a in m.agents),
            }
        self.datacollector = DataCollector(
            model_reporters=model_reporters,
            agent_reporters=agent_reporters,
        )

        for i in range(farmers):
            agent = Farmer(self, wealth=self.random.randrange(10, 50))
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent.location = (x, y)

        for i in range(traders):
            agent = Trader(self, wealth=self.random.randrange(10, 50))
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            agent.location = (x, y)

    def step(self):
        self.economy.step()
        self.agents.shuffle_do("step")

        dead_agents = [a for a in self.agents if not a.alive]
        for agent in dead_agents:
            self.remove(agent)

        self.datacollector.collect(self)
        print(f"  City Step {self.steps}: Food Pool = {self.economy.resource_pools.get('food')}")
