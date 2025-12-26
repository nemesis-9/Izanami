from core.subsystems.economy.econ_price import EconomyPrice
from core.subsystems.economy.econ_add import EconomyAdd
from core.subsystems.economy.econ_remove import EconomyRemove


class Economy:
    def __init__(self, model, economy_variables):
        self.model = model

        self.wealth = economy_variables.get("wealth", 0)
        self.wealth_margin = economy_variables.get("wealth_margin", 0)

        self.resource_pools = economy_variables.get("resource_pools", {})
        self.price_pools = economy_variables.get("price_pools", {})

        self.base_prices = economy_variables.get("base_prices", {})
        self.price_elasticities = economy_variables.get("price_elasticities", {})
        self.minimum_threshold = economy_variables.get("minimum_threshold", {})
        self.maximum_threshold = economy_variables.get("maximum_threshold", {})
        self.target_supply = economy_variables.get("target_supply", {})

        self.price_logic = EconomyPrice(self)
        self.add_logic = EconomyAdd(self)
        self.remove_logic = EconomyRemove(self)

    def calculate_price(self, resource):
        new_price = self.price_logic.calculate_price(resource)
        self.price_pools[resource] = new_price
        return new_price

    def add_resource(self, resource_name, amount):
        affordable_amount = self.add_logic.add_resource(resource_name, amount)
        return affordable_amount

    def request_resource(self, resource_name, amount):
        actual_gained = self.remove_logic.request_resource(resource_name, amount)
        return actual_gained

    def step(self):
        for resource in self.resource_pools.keys():
            self.calculate_price(resource)
        pass
