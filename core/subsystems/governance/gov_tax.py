class GovTax:
    def collect_taxes(self, gov):
        tax_collected_in_step = 0

        for agent in gov.model.schedule.agents:
            if agent.wealth > gov.tax_threshold / (1 - gov.tax_rate):
                tax_amount = agent.wealth * gov.tax_rate
                agent.wealth -= tax_amount
                gov.treasury += tax_amount
                tax_collected_in_step += tax_amount

        gov.total_tax_collected += tax_collected_in_step

    def adjust_tax_rate(self, gov):
        min_tax_rate = gov.tax_min_rate
        max_tax_rate = gov.tax_max_rate
        adj_tax_rate = gov.tax_adj_rate

        if gov.treasury < gov.treasury_min:
            gov.tax_rate = min(max_tax_rate, gov.tax_rate + adj_tax_rate)

        elif gov.treasury > gov.treasury_max:
            gov.tax_rate = max(min_tax_rate, gov.tax_rate - adj_tax_rate)
