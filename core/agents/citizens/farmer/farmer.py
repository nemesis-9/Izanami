from core.agents.base.agent import BaseAgent
from core.agents.base.agent_trade import AgentTrade

from core.agents.citizens.farmer.farmer_produce import FarmerProduce
from core.agents.citizens.farmer.farmer_sell import FarmerSell
from core.agents.citizens.farmer.farmer_travel import FarmerTravel
from core.agents.citizens.farmer.farmer_utility import FarmerUtility


class Farmer(BaseAgent):
    def __init__(self, model, wealth, initial_farmer_config):
        super().__init__(model, wealth, "farmer")

        self.food_production_rate = self.random.randrange(20, 50)
        self.harvest_progress = 0
        self.inventory = {"food": 6}
        self.has_farm_plot = True
        self.action = 'idle'

        self.max_harvest_progress = initial_farmer_config.get("max_harvest_progress", 0)
        self.max_inventory = initial_farmer_config.get("max_inventory", 0)

        self.personal_minimum = initial_farmer_config.get("personal_minimum", 0)
        self.selling_margin = initial_farmer_config.get("selling_margin", 0)
        self.selling_cap = initial_farmer_config.get("selling_cap", 0)
        self.spoilage_rate = initial_farmer_config.get("spoilage_rate", 0)
        self.selling_power = initial_farmer_config.get("selling_power", {})

        self.home_location = None
        self.destination = None
        self.path = None

        self.trade = AgentTrade(self)
        self.travel_logic = FarmerTravel(self)
        self.producing_logic = FarmerProduce(self)
        self.selling_logic = FarmerSell(self)
        self.utility_logic = FarmerUtility(self)

    def update_agent_config(self):
        super().update_agent_config()
        farmer_vars = self.model.farmer_variables
        self.personal_minimum = farmer_vars.get("personal_minimum", 0)
        self.selling_margin = farmer_vars.get("selling_margin", 0)
        self.selling_cap = farmer_vars.get("selling_cap", 0)
        self.spoilage_rate = farmer_vars.get("spoilage_rate", 0)
        self.selling_power = farmer_vars.get("selling_power", {})

    def move(self):
        return self.travel_logic.move()

    def produce(self):
        return self.producing_logic.produce()

    def sell_goods(self):
        selling_resources = self.selling_logic.sell_goods()
        if selling_resources:
            self.trade.sell_goods(selling_resources)

    def apply_spoilage(self):
        if self.inventory.get("food", 0) > 0:
            spoilage = round(self.inventory["food"] * self.spoilage_rate)
            self.inventory["food"] -= spoilage

    def step(self):
        super().step()
        if not self.alive:
            return

        self.update_agent_config()
        self.apply_spoilage()

        self.action = self.utility_logic.decide_action()
        market = self.model.city_network.points_of_interest["market"]

        is_moving = self.travel_logic.move()
        if is_moving:
            return

        if self.action == "produce" and self.pos == self.home_location:
            self.produce()
        elif self.action == "sell" and self.pos == market:
            self.sell_goods()
