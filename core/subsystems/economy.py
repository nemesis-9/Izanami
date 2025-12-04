class Economy:
    def __init__(self, model):
        self.model = model

        self.resource_pools = {
            "food": 50,
            "materials": 100,
            "gold": 0,
        }

        self.prices = {
            "food": 1.0,
            "material": 2.0
        }

    def add_resource(self, resource_name, amount):
        if resource_name in self.resource_pools:
            self.resource_pools[resource_name] += amount
        else:
            self.resource_pools[resource_name] = amount

    def request_resources(self, resource_name, amount):
        if resource_name not in self.resource_pools or self.resource_pools[resource_name] <= 0:
            return 0

        actual_gained = min(amount, self.resource_pools[resource_name])
        self.resource_pools[resource_name] -= actual_gained
        return actual_gained

    def step(self):
        pass
