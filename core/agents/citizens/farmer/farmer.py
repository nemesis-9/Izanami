from core.agents.base.agent import BaseAgent
from core.agents.base.agent_trade import AgentTrade

from core.agents.citizens.farmer.farmer_produce import FarmerProduce
from core.agents.citizens.farmer.farmer_sell import FarmerSell
from core.agents.citizens.farmer.farmer_travel import FarmerTravel


class Farmer(BaseAgent):
    def __init__(self, model, wealth, initial_farmer_config):
        super().__init__(model, wealth, "farmer")

        self.food_production_rate = self.random.randrange(3, 7)

        self.inventory = {}
        self.has_farm_plot = True
        self.path = None

        self.surplus_threshold = initial_farmer_config.get("surplus_threshold", 0)
        self.survival_buffer = initial_farmer_config.get("survival_buffer", 0)

        self.home_location = None
        self.destination = None

        self.trade = AgentTrade(self)
        self.producing_logic = FarmerProduce(self)
        self.selling_logic = FarmerSell(self)
        self.travel_logic = FarmerTravel(self)

    def update_agent_config(self):
        super().update_agent_config()
        farmer_vars = self.model.farmer_variables
        self.surplus_threshold = farmer_vars.get("surplus_threshold", 0)
        self.survival_buffer = farmer_vars.get("survival_buffer", 0)

    def move(self):
        return self.travel_logic.move()

    def produce(self):
        self.producing_logic.produce()

    def sell_goods(self):
        selling_resources = self.selling_logic.sell_goods()
        if selling_resources:
            self.trade.sell_goods(selling_resources)

    def step(self):
        super().step()
        if not self.alive:
            return

        market = self.model.city_network.points_of_interest["market"]

        self.update_agent_config()
        is_moving = self.move()

        if not is_moving:
            if self.pos == self.home_location:
                self.produce()
            elif self.pos == market:
                self.sell_goods()
