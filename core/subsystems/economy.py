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

    def calculate_price(self, resource):
        if resource not in self.resource_pools:
            return 0

        resource_pool = self.resource_pools.get(resource, 0)
        base_price = self.base_prices.get(resource, 0)
        price_elasticity = self.price_elasticities.get(resource, 0)
        minimum_threshold = self.minimum_threshold.get(resource, 0)

        # simple inverse relationship formula
        new_price = round(base_price - (resource_pool * price_elasticity), 3)

        # minimum threshold
        self.price_pools[resource] = max(minimum_threshold, new_price)

        return self.price_pools[resource]

    def add_resource(self, resource_name, amount):
        if amount <= 0:
            return 0

        current_price = self.calculate_price(resource_name)
        total_cost = current_price * amount
        affordable_cost = self.wealth * self.wealth_margin

        if total_cost > affordable_cost:
            affordable_amount = int(affordable_cost / current_price) if not current_price == 0 else 0
        else:
            affordable_amount = amount

        if resource_name in self.resource_pools:
            self.resource_pools[resource_name] += affordable_amount
        else:
            self.resource_pools[resource_name] = affordable_amount

        return affordable_amount

    def request_resource(self, resource_name, amount):
        if amount <= 0:
            return 0

        if resource_name not in self.resource_pools or self.resource_pools[resource_name] <= 0:
            return 0

        actual_gained = min(amount, self.resource_pools[resource_name])
        self.resource_pools[resource_name] -= actual_gained
        return actual_gained

    def step(self):
        for resource in self.resource_pools.keys():
            self.calculate_price(resource)
        pass
