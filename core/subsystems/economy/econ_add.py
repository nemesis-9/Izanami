class EconomyAdd:
    def __init__(self, econ):
        self.econ = econ

    def affordance(self):
        affordable_cost = self.econ.wealth * self.econ.wealth_margin
        return max(0, affordable_cost)

    def add_resource(self, resource_name, amount):
        if amount <= 0:
            return 0

        current_price = self.econ.price_logic.calculate_price(resource_name)
        total_cost = current_price * amount
        affordable_cost = self.affordance()

        if total_cost > affordable_cost:
            affordable_amount = max(0, int(affordable_cost / current_price))
        else:
            affordable_amount = amount

        final_cost = affordable_amount * current_price
        self.econ.wealth -= final_cost

        if resource_name in self.econ.resource_pools:
            self.econ.resource_pools[resource_name] += affordable_amount
        else:
            self.econ.resource_pools[resource_name] = affordable_amount

        return affordable_amount
