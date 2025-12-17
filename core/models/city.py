from mesa import Model, DataCollector
from mesa.space import MultiGrid

from core.subsystems.economy.economy import Economy
from core.subsystems.governance.governance import Governance

from core.agents.citizens.farmer.farmer import Farmer
from core.agents.citizens.trader.trader import Trader
from core.agents.citizens.crafter.crafter import Crafter

from core.spaces.city_network import CityNetwork

from core.data_collectors.reporter_model import reporter_model
from core.data_collectors.reporter_agent import reporter_agent

from core.config.agent_config import AgentConfig
from core.config.subsystem_config import SubsystemConfig

agent_config = AgentConfig().get()
subsystem_config = SubsystemConfig().get()


class CityModel(Model):
    def __init__(
            self, unique_id, parent_world,
            seasons, season_length=25,
            width=100, height=100,
            farmers=5, traders=5, crafters=5,
            model_reporters=None, agent_reporters=None
    ):
        super().__init__()
        self.unique_id = unique_id
        self.parent_world = parent_world

        self.grid = MultiGrid(width, height, torus=False)
        self.city_network = CityNetwork(self, width, height)

        self.seasons = seasons
        self.season_length = season_length
        self.current_season_index = 0
        self.current_season = seasons[0]
        self.running = True

        self.base_variables = agent_config.agent_var("base", self.current_season)
        self.farmer_variables = agent_config.agent_var("farmer", self.current_season)
        self.trader_variables = agent_config.agent_var("trader", self.current_season)
        self.crafter_variables = agent_config.agent_var("crafter", self.current_season)

        economy_variables = subsystem_config.subsystem_var('economy', self.current_season)
        governance_variables = subsystem_config.subsystem_var('governance', self.current_season)

        self.economy = Economy(self, economy_variables)
        self.governance = Governance(self, governance_variables)

        if model_reporters is None:
            model_reporters = reporter_model
        if agent_reporters is None:
            agent_reporters = reporter_agent

        self.datacollector = DataCollector(
            model_reporters=model_reporters,
            agent_reporters=agent_reporters,
        )

        #  --- Agent Initialization ---

        for i in range(farmers):
            agent = Farmer(
                self,
                wealth=self.random.randrange(50, 200),
                initial_farmer_config=self.farmer_variables
            )
            self._register_agent(agent)

        for i in range(traders):
            agent = Trader(
                self,
                wealth=self.random.randrange(100, 500),
                initial_trader_config=self.trader_variables
            )
            self._register_agent(agent)
            agent.home_location = agent.pos

        for i in range(crafters):
            agent = Crafter(
                self,
                wealth=self.random.randrange(100, 500),
                initial_crafter_config=self.crafter_variables
            )
            self._register_agent(agent)
            agent.home_location = agent.pos

    def update_season(self):
        if self.steps % self.season_length == 0 and self.steps > 0:
            self.current_season_index = (self.current_season_index + 1) % len(self.seasons)
            self.current_season = self.seasons[self.current_season_index]

            self.base_variables = agent_config.agent_var("base", self.current_season)
            self.farmer_variables = agent_config.agent_var("farmer", self.current_season)
            self.trader_variables = agent_config.agent_var("trader", self.current_season)
            self.crafter_variables = agent_config.agent_var("crafter", self.current_season)

            print(f"\n--- Season Change! It is now {self.current_season} ---")

    def _place_agent(self, agent):
        if agent.agent_type == 'farmer':
            poi_key = self.random.choice([k for k in self.city_network.points_of_interest if 'farm_plot' in k])
            pos = self.city_network.points_of_interest[poi_key]

        elif agent.agent_type == 'crafter':
            pos = self.city_network.points_of_interest["city_center"]

        else:
            pos = (self.random.randrange(self.grid.width), self.random.randrange(self.grid.height))

        self.grid.place_agent(agent, pos)
        agent.location = pos
        agent.pos = pos

    def _register_agent(self, agent):
        self._place_agent(agent)
        self.agents.add(agent)

    def step(self):
        self.update_season()

        self.economy.step()

        self.governance.collect_taxes()
        self.governance.fund_public_services()

        if hasattr(self.city_network, 'adjust_cost_for_step'):
            self.city_network.adjust_cost_for_step()

        for agent in self.agents:
            if agent.alive:
                agent.step()

        self.governance.distribute_aid()

        dead_agents = [a for a in self.agents if not a.alive]
        for agent in dead_agents:
            self.grid.remove_agent(agent)
            self.agents.remove(agent)

        self.datacollector.collect(self)

        self.steps += 1
        print(f"  City Step {self.steps}: Food Pool = {self.economy.resource_pools.get('food')}")
