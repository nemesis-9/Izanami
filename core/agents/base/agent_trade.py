class AgentTrade:
    def buy_goods(self, agent, buying_resources):
        for resource, amount in buying_resources:
            if amount > 0:
                current_price = agent.model.economy.calculate_price(resource)
                buying_quantity = agent.model.economy.request_resource(resource, amount)
                if buying_quantity > 0:
                    cost = current_price * buying_quantity
                    agent.wealth -= cost
                    agent.model.economy.wealth += cost
                    agent.inventory[resource] = agent.inventory.get(resource, 0) + buying_quantity

    def sell_goods(self, agent, selling_resources):
        for resource, amount in selling_resources:
            if amount > 0:
                current_price = agent.model.economy.calculate_price(resource)
                selling_quantity = agent.model.economy.allocate_resource(resource, amount)
                if selling_quantity > 0:
                    income = current_price * selling_quantity
                    agent.wealth += income
                    agent.model.economy.wealth -= income
                    agent.inventory[resource] = agent.inventory.get(resource, 0) - selling_quantity
