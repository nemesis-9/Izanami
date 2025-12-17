from core.agents.base.agent import BaseAgent

from core.agents.base.agent_trade import AgentTrade

from core.agents.citizens.crafter.crafter_buy import CrafterBuy
from core.agents.citizens.crafter.crafter_sell import CrafterSell
from core.agents.citizens.crafter.crafter_travel import CrafterTravel
from core.agents.citizens.crafter.crafter_craft import CrafterCraft


class Crafter(BaseAgent):
    def __init__(self, model, wealth, initial_crafter_config):
        super().__init__(model, wealth, "crafter")

        self.inventory = {"iron": 20, "copper": 15}
        self.crafting_rate = self.random.randrange(4, 10)

        self.has_craft_plot = True
        self.path = None
        self.home_location = None
        self.destination = None
        self.mode = 'crafting'

        self.trade = AgentTrade(self)
        self.buying_logic = CrafterBuy(self)
        self.selling_logic = CrafterSell(self)
        self.travel_logic = CrafterTravel(self)
        self.crafting_logic = CrafterCraft(self)

        self.max_inventory = initial_crafter_config.get("max_inventory", 0)
        self.buying_power = initial_crafter_config.get("buying_power", {})
        self.selling_power = initial_crafter_config.get("selling_power", {})
        self.inventory_margin = initial_crafter_config.get("inventory_margin", 0)
        self.wealth_margin = initial_crafter_config.get("wealth_margin", 0)

    def update_agent_config(self):
        super().update_agent_config()
        crafter_vars = self.model.crafter_variables
        self.max_inventory = crafter_vars.get("max_inventory", 0)
        self.buying_power = crafter_vars.get("buying_power", {})
        self.selling_power = crafter_vars.get("selling_power", {})
        self.inventory_margin = crafter_vars.get("inventory_margin", 0)
        self.wealth_margin = crafter_vars.get("wealth_margin", 0)

    def toggle_mode(self):
        if self.mode == 'buying':
            self.mode = 'crafting'
        elif self.mode == 'crafting':
            self.mode = 'selling'
        elif self.mode == 'selling':
            self.mode = 'buying'
        else:
            self.mode = 'crafting'

    def move(self):
        return self.travel_logic.move()

    def buy_materials(self):
        buying_resources = self.buying_logic.buy_materials()
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

    # Craft function
    def craft(self):
        return self.crafting_logic.craft()

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
                self.buy_materials()
            elif self.pos == city_center:
                self.sell_goods()
            elif self.pos == self.home_location:
                self.craft()
