import math

class EconomyPrice:
    def __init__(self, econ):
        self.econ = econ

    @staticmethod
    def new_price_formula(base_price, resource_pool, price_elasticity, target_supply):
        q_current = max(1.0, resource_pool)
        q_target = max(1.0, target_supply)
        elasticity = max(1.0, price_elasticity)

        supply_ratio = q_target / q_current
        new_price = base_price * (supply_ratio ** elasticity)

        return round(new_price, 3)

    def calculate_price(self, resource):
        if resource not in self.econ.resource_pools:
            return 0

        resource_pool = self.econ.resource_pools.get(resource, 0)
        base_price = self.econ.base_prices.get(resource, 0)
        price_elasticity = self.econ.price_elasticities.get(resource, 0)
        minimum_threshold = self.econ.minimum_threshold.get(resource, 0)
        target_supply = self.econ.target_supply.get(resource, 1000)

        new_price = self.new_price_formula(base_price, resource_pool, price_elasticity, target_supply)

        # minimum threshold
        final_price = max(minimum_threshold, new_price)

        return final_price

    # @staticmethod
    # def new_price_formula(base_price, resource_pool, price_elasticity):
    #     # simple inverse relationship formula
    #     new_price = round(base_price - (resource_pool * price_elasticity), 3)
    #     return new_price
