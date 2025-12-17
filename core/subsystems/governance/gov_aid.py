class GovAid:
    def __init__(self, gov):
        self.gov = gov

    def fund_aid(self):
        for resource, amount in self.gov.aid_amount.items():
            current_price = self.gov.model.economy.calculate_price(resource)
            aid_price = round(current_price * self.gov.aid_price_margin.get(resource, 1.0), 3)

            received_amount = self.gov.model.economy.request_resource(resource, amount)
            cost = round(aid_price * received_amount, 3)

            self.gov.treasury -= cost
            self.gov.model.economy.wealth += cost
            self.gov.aid_fund[resource] = self.gov.aid_fund.get(resource, 0) + received_amount
            self.gov.total_public_spending += cost

    def distribute_aid(self):
        wealth_threshold = self.gov.aid_threshold.get('wealth', 0)
        agents_in_need = [
            agent for agent in self.gov.model.agents
            if agent.wealth <= wealth_threshold
        ]

        if not agents_in_need:
            return

        for resource in list(self.gov.aid_fund.keys()):
            available_aid = self.gov.aid_fund.get(resource, 0)
            if available_aid <= 0:
                continue

            resource_threshold = self.gov.aid_threshold.get(resource, 0)

            total_needed_list = []

            for agent in agents_in_need:
                amount_needed = resource_threshold - agent.inventory.get(resource, 0)
                if amount_needed > 0:
                    total_needed_list.append((agent, amount_needed))

            total_needed_list.sort(key=lambda x: x[1], reverse=True)

            for agent, required_amount in total_needed_list:
                if self.gov.aid_fund.get(resource, 0) <= 0:
                    break
                amount_to_give = min(required_amount, available_aid)
                agent.inventory[resource] = agent.inventory[resource] + amount_to_give
                self.gov.aid_fund[resource] -= amount_to_give
                available_aid -= amount_to_give
