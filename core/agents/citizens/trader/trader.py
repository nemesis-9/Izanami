from core.agents.base.agent import BaseAgent

from core.agents.base.agent_trade import AgentTrade
from trader_buy import TraderBuy
from trader_sell import TraderSell
from trader_travel import TraderTravel


class Trader(BaseAgent):
    def __init__(self, model, wealth, initial_trader_config):
        super().__init__(model, wealth, "trader")

        self.inventory = {"food": 2}

        self.path = None

        self.home_location = None
        self.destination = None
        self.mode = 'selling'

        self.trade = AgentTrade(self)
        self.buying_logic = TraderBuy(self)
        self.selling_logic = TraderSell(self)
        self.travel_logic = TraderTravel(self)

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

    def toggle_mode(self):
        if self.mode == 'selling':
            self.mode = 'buying'
        elif self.mode == 'buying':
            self.mode = 'selling'

    def move(self):
        return self.travel_logic.move()

    def buy_goods(self):
        buying_resources = self.buying_logic.buy_goods()
        if buying_resources:
            self.trade.buy_goods(buying_resources)

        if (
                sum(self.inventory.values()) >= self.max_inventory * self.inventory_margin
                or self.wealth < self.wealth_margin
        ):
            self.toggle_mode()

    def sell_goods(self):
        selling_resources = self.selling_logic.sell_goods()
        if selling_resources:
            self.trade.sell_goods(selling_resources)

    def step(self):
        super().step()
        if not self.alive:
            return

        market = self.model.city_network.points_of_interest["market"]
        city_center = self.model.city_network.points_of_interest["city_center"]

        self.update_agent_config()
        is_moving = self.move()

        if not is_moving:
            if self.pos == market:
                self.sell_goods()
                self.buy_goods()
            elif self.pos == city_center:
                self.sell_goods()
                self.buy_goods()
