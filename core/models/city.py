from mesa import Model, DataCollector
from mesa.space import MultiGrid
from core.subsystems.economy import Economy
from core.agents.citizens.farmer import Farmer
from core.agents.citizens.trader import Trader
from core.spaces.city_network import CityNetwork
from core.data_collectors.reporter_model import reporter_model
from core.data_collectors.reporter_agent import reporter_agent


class CityModel(Model):
    def __init__(
            self, unique_id,
            parent_world, width=100, height=100,
            farmers=5, traders=5,
            resource_pools=None, price_pools=None,
            model_reporters=None, agent_reporters=None
    ):
        super().__init__()
        self.unique_id = unique_id
        self.parent_world = parent_world

        self.grid = MultiGrid(width, height, torus=False)
        self.city_network = CityNetwork(self, width, height)

        self.economy = Economy(self, resource_pools, price_pools)

        if model_reporters is None:
            model_reporters = reporter_model
        if agent_reporters is None:
            agent_reporters = reporter_agent

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
            agent.home_location = (x, y)

    def step(self):
        self.economy.step()
        self.agents.shuffle_do("step")

        dead_agents = [a for a in self.agents if not a.alive]
        for agent in dead_agents:
            self.agents.remove(agent)

        self.datacollector.collect(self)
        print(f"  City Step {self.steps}: Food Pool = {self.economy.resource_pools.get('food')}")
