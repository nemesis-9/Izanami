class Economy:
    def __init__(self, model, economy_variables):
        self.model = model

        self.resource_pools = economy_variables.get("resource_pools", {})

        self.price_pools = economy_variables.get("price_pools", {})

        self.base_prices = economy_variables.get("base_prices", {})
        self.price_elasticities = economy_variables.get("price_elasticities", {})
        self.minimum_threshold = economy_variables.get("minimum_threshold", {})

    def calculate_price(self, resource):
        if resource not in self.resource_pools:
            return 0

        resource_pool = self.resource_pools[resource]
        base_price = self.base_prices[resource]
        price_elasticity = self.price_elasticities[resource]
        minimum_threshold = self.minimum_threshold[resource]

        # simple inverse relationship formula
        new_price = base_price - (resource_pool * price_elasticity)

        # minimum threshold
        self.price_pools[resource] = max(minimum_threshold, new_price)

        return self.price_pools[resource]

    def add_resource(self, resource_name, amount):
        if resource_name in self.resource_pools:
            self.resource_pools[resource_name] += amount
        else:
            self.resource_pools[resource_name] = amount

    def request_resource(self, resource_name, amount):
        if resource_name not in self.resource_pools or self.resource_pools[resource_name] <= 0:
            return 0

        actual_gained = min(amount, self.resource_pools[resource_name])
        self.resource_pools[resource_name] -= actual_gained
        return actual_gained

    def step(self):
        for resource in self.resource_pools.keys():
            self.calculate_price(resource)
        pass
