class EconomyRemove:
    def __init__(self, econ):
        self.econ = econ

    def request_resource(self, resource_name, amount):
        if amount <= 0:
            return 0

        if resource_name not in self.econ.resource_pools or self.econ.resource_pools[resource_name] <= 0:
            return 0

        actual_gained = min(amount, self.econ.resource_pools[resource_name])
        self.econ.resource_pools[resource_name] -= actual_gained
        return actual_gained
