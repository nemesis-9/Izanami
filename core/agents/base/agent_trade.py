class AgentTrade:
    def __init__(self, agent):
        self.agent = agent

    def buy_goods(self, buying_resources):
        for resource, amount in buying_resources:
            if amount <= 0:
                continue

            current_price = self.agent.model.economy.calculate_price(resource)
            buying_quantity = self.agent.model.economy.request_resource(resource, amount)

            if buying_quantity > 0:
                cost = current_price * buying_quantity

                if self.agent.wealth >= cost:
                    self.agent.wealth -= cost
                    self.agent.model.economy.wealth += cost
                    self.agent.inventory[resource] = self.agent.inventory.get(resource, 0) + buying_quantity

                else:
                    self.agent.model.economy.add_resource(resource, buying_quantity)

    def sell_goods(self, selling_resources):
        for resource, amount in selling_resources:
            owned_qty = self.agent.inventory.get(resource, 0)
            actual_sell_qty = min(amount, owned_qty)
            if actual_sell_qty <= 0:
                continue

            current_price = self.agent.model.economy.calculate_price(resource)
            income = current_price * actual_sell_qty

            econ_wealth = self.agent.model.economy.wealth
            if econ_wealth < income:
                if econ_wealth <= 0:
                    continue

                actual_sell_qty = int(econ_wealth / current_price)
                income = actual_sell_qty * current_price

            if actual_sell_qty > 0:
                self.agent.model.economy.add_resource(resource, actual_sell_qty)

                self.agent.wealth += income
                self.agent.model.economy.wealth -= income

                self.agent.inventory[resource] = round(owned_qty - actual_sell_qty, 3)
