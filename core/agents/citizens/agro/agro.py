from core.agents.base.agent import BaseAgent
from core.agents.base.agent_trade import AgentTrade

from core.agents.citizens.agro.agro_travel import AgroTravel
from core.agents.citizens.agro.agro_produce import AgroProduce
from core.agents.citizens.agro.agro_sell import AgroSell
from core.agents.citizens.agro.agro_utility import AgroUtility


class Agro(BaseAgent):
    def __init__(self, model, wealth, initial_agro_config):
        super().__init__(model, wealth, "agro")

        self.food_production_rate = self.random.randrange(250, 500)
        self.harvest_progress = 0
        self.inventory = {"food": 10}
        self.has_farm_plot = True
        self.is_emergency = False
        self.action = 'idle'

        self.max_harvest_progress = initial_agro_config.get("max_harvest_progress", 0)
        self.max_inventory = initial_agro_config.get("max_inventory", 0)

        self.personal_minimum = initial_agro_config.get("personal_ratio", 0)
        self.selling_margin = initial_agro_config.get("selling_margin", 0)
        self.selling_cap = initial_agro_config.get("selling_cap", 0)
        self.emergency_margin = initial_agro_config.get("emergency_margin", 0)
        self.spoilage_rate = initial_agro_config.get("spoilage_rate", 0)
        self.selling_power = initial_agro_config.get("selling_power", {})

        self.home_location = None
        self.destination = None
        self.path = None

        self.trade = AgentTrade(self)
        self.travel_logic = AgroTravel(self)
        self.producing_logic = AgroProduce(self)
        self.selling_logic = AgroSell(self)
        self.utility_logic = AgroUtility(self)

    def update_agent_config(self):
        super().update_agent_config()
        agro_vars = self.model.agro_variables
        self.personal_minimum = agro_vars.get("personal_minimum", 0)
        self.selling_margin = agro_vars.get("selling_margin", 0)
        self.selling_cap = agro_vars.get("selling_cap", 0)
        self.emergency_margin = agro_vars.get("emergency_margin", 0)
        self.spoilage_rate = agro_vars.get("spoilage_rate", 0)
        self.selling_power = agro_vars.get("selling_power", {})

    def move(self):
        return self.travel_logic.move()

    def produce(self):
        return self.producing_logic.produce()

    def sell_goods(self):
        selling_resources = self.selling_logic.sell_goods()
        if selling_resources:
            print(f"Agro [{self.unique_id}] selling foods: {selling_resources}")
            self.trade.sell_goods(selling_resources)

    def apply_spoilage(self):
        if self.inventory.get("food", 0) > 0:
            spoilage = round(self.inventory["food"] * self.spoilage_rate)
            self.inventory["food"] -= spoilage

    def emergency(self):
        market_supply = self.model.economy.resource_pools.get('food', 0)
        if market_supply < self.emergency_margin:
            self.is_emergency = True
        else:
            self.is_emergency = False

    def step(self):
        super().step()
        if not self.alive: return

        self.update_agent_config()
        self.emergency()
        self.apply_spoilage()

        self.action = self.utility_logic.decide_action()
        market = self.model.city_network.points_of_interest["market"]

        if self.action == "travel":
            if self.utility_logic.sell_utility() > self.utility_logic.produce_utility():
                self.destination = market
            else:
                self.destination = self.home_location
            self.move()

        elif self.action == "produce":
            if self.pos == self.home_location:
                self.produce()
            else:
                self.move()

        elif self.action == "sell":
            if self.pos == market:
                self.sell_goods()
            else:
                self.move()
