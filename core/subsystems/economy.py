class Economy:
    def __init__(self, model):
        self.model = model

        self.resource_pools = {
            "food": 50,
            "materials": 100,
            "gold": 0,
        }

        self.prices = {
            "food": 2.0,
            "material": 5.0,
            "labour": 1.0,
        }

        self.base_food_price = 2.0
        self.price_elasticity = 0.005

    def calculate_price(self, resource):
        if resource == "food":
            food_pool = self.resource_pools["food"]

            # simple inverse relationship formula
            new_price = self.base_food_price - (food_pool * self.price_elasticity)
            # minimum threshold
            self.prices["food"] = max(0.5, new_price)

        return self.prices[resource]

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
        self.calculate_price("food")
        pass
