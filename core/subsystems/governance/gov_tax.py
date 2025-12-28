class GovTax:
    def __init__(self, gov):
        self.gov = gov

    def collect_taxes(self):
        tax_collected_in_step = 0

        for agent in self.gov.model.agents:
            if agent.wealth > self.gov.tax_threshold:
                taxable_wealth = agent.wealth - self.gov.tax_threshold
                tax_amount = taxable_wealth * self.gov.tax_rate
                agent.wealth -= tax_amount
                self.gov.treasury += tax_amount
                tax_collected_in_step += tax_amount

        self.gov.total_tax_collected += tax_collected_in_step

    def adjust_tax_rate(self):
        min_tax_rate = self.gov.tax_min_rate
        max_tax_rate = self.gov.tax_max_rate
        adj_tax_rate = self.gov.tax_adj_rate

        if self.gov.treasury < self.gov.treasury_min:
            self.gov.tax_rate = min(max_tax_rate, self.gov.tax_rate + adj_tax_rate)

        elif self.gov.treasury > self.gov.treasury_max:
            self.gov.tax_rate = max(min_tax_rate, self.gov.tax_rate - adj_tax_rate)
