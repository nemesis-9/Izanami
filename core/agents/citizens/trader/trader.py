from core.agents.base.agent import BaseAgent

from core.agents.base.agent_trade import AgentTrade

from core.agents.citizens.trader.trader_buy import TraderBuy
from core.agents.citizens.trader.trader_sell import TraderSell
from core.agents.citizens.trader.trader_travel import TraderTravel
from core.agents.citizens.trader.trader_utility import TraderUtility


class Trader(BaseAgent):
    def __init__(self, model, wealth, initial_trader_config):
        super().__init__(model, wealth, "trader")

        self.inventory = {"food": 2}
        self.action = 'idle'

        self.home_location = None
        self.destination = None
        self.path = None

        self.trade = AgentTrade(self)
        self.buying_logic = TraderBuy(self)
        self.selling_logic = TraderSell(self)
        self.travel_logic = TraderTravel(self)
        self.utility = TraderUtility(self)

        self.max_inventory = initial_trader_config.get("max_inventory", 0)
        self.buying_power = initial_trader_config.get("buying_power", {})
        self.buying_aggression = initial_trader_config.get("buying_aggression", 1.0)
        self.selling_power = initial_trader_config.get("selling_power", {})
        self.selling_aggression = initial_trader_config.get("selling_aggression", 1.0)
        self.inventory_margin = initial_trader_config.get("inventory_margin", 0)
        self.wealth_margin = initial_trader_config.get("wealth_margin", 0)

    def update_agent_config(self):
        super().update_agent_config()
        trader_vars = self.model.trader_variables
        self.max_inventory = trader_vars.get("max_inventory", 0)
        self.buying_power = trader_vars.get("buying_power", {})
        self.buying_aggression = trader_vars.get("buying_aggression", 1.0)
        self.selling_power = trader_vars.get("selling_power", {})
        self.selling_aggression = trader_vars.get("selling_aggression", 1.0)
        self.inventory_margin = trader_vars.get("inventory_margin", 0)
        self.wealth_margin = trader_vars.get("wealth_margin", 0)

    def move(self):
        return self.travel_logic.move()

    def buy_goods(self):
        buying_resources = self.buying_logic.buy_goods()
        if buying_resources:
            self.trade.buy_goods(buying_resources)

    def sell_goods(self):
        selling_resources = self.selling_logic.sell_goods()
        if selling_resources:
            self.trade.sell_goods(selling_resources)

    def toggle_destination(self, market, city_center):
        self.destination = city_center if self.pos == market else market

    def step(self):
        super().step()
        if not self.alive:
            return

        self.update_agent_config()

        self.action = self.utility.decide_action()

        market = self.model.city_network.points_of_interest["market"]
        city_center = self.model.city_network.points_of_interest["city_center"]

        if self.action in ("buy", "sell"):
            self.destination = self.travel_logic.get_nearest_destination(
                [market, city_center]
            )
        else:
            self.destination = None

        if self.travel_logic.move():
            return

        if self.action == "buy":
            self.buy_goods()
        elif self.action == "sell":
            self.sell_goods()
