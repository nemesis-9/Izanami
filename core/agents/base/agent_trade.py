class AgentTrade:
    def __init__(self, agent):
        self.agent = agent

    def buy_goods(self, buying_resources):
        for resource, amount in buying_resources:
            if amount > 0:
                current_price = self.agent.model.economy.calculate_price(resource)
                buying_quantity = self.agent.model.economy.request_resource(resource, amount)
                if buying_quantity > 0:
                    cost = current_price * buying_quantity
                    self.agent.wealth -= cost
                    self.agent.model.economy.wealth += cost
                    self.agent.inventory[resource] = self.agent.inventory.get(resource, 0) + buying_quantity

    def sell_goods(self, selling_resources):
        for resource, amount in selling_resources:
            if amount > 0:
                current_price = self.agent.model.economy.calculate_price(resource)
                selling_quantity = self.agent.model.economy.allocate_resource(resource, amount)
                if selling_quantity > 0:
                    income = current_price * selling_quantity
                    self.agent.wealth += income
                    self.agent.model.economy.wealth -= income
                    self.agent.inventory[resource] = self.agent.inventory.get(resource, 0) - selling_quantity
