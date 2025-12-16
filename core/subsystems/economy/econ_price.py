class EconomyPrice:
    def __init__(self, econ):
        self.econ = econ

    @staticmethod
    def new_price_formula(base_price, resource_pool, price_elasticity):
        # simple inverse relationship formula
        new_price = round(base_price - (resource_pool * price_elasticity), 3)
        return new_price

    def calculate_price(self, resource):
        if resource not in self.econ.resource_pools:
            return 0

        resource_pool = self.econ.resource_pools.get(resource, 0)
        base_price = self.econ.base_prices.get(resource, 0)
        price_elasticity = self.econ.price_elasticities.get(resource, 0)
        minimum_threshold = self.econ.minimum_threshold.get(resource, 0)

        new_price = self.new_price_formula(base_price, resource_pool, price_elasticity)

        # minimum threshold
        final_price = max(minimum_threshold, new_price)

        return final_price
