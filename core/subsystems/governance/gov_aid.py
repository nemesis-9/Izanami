class GovAid:
    def __init__(self, gov):
        self.gov = gov

    def fund_aid(self):
        for resource, amount in self.gov.aid_amount.items():
            current_price = self.gov.model.economy.current_price(resource)
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
            max_per_agent = self.gov.aid_max_per_agent.get(resource, float('inf'))

            eligible_recipients = []
            for agent in agents_in_need:
                current_inv = agent.inventory.get(resource, 0)
                if current_inv < resource_threshold:
                    needed = resource_threshold - current_inv
                    eligible_recipients.append((agent, needed))

            if not eligible_recipients:
                continue

            eligible_recipients.sort(key=lambda x: x[1], reverse=True)

            for agent, amount_needed in eligible_recipients:
                if available_aid <= 0:
                    break

                allowed_amount = min(amount_needed, max_per_agent, available_aid)

                agent.inventory[resource] = agent.inventory.get(resource, 0) + allowed_amount
                self.gov.aid_fund[resource] -= allowed_amount
                available_aid -= allowed_amount
