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
        economy_growth = self.gov.model.economy_metrics.get_metric("growth")
        inflation_rate = self.gov.model.economy_metrics.get_metric("inflation")
        target_inflation = self.gov.target_inflation

        # 1. EMERGENCY: Treasury is dangerously low
        if self.gov.treasury < self.gov.treasury_min:
            self.gov.tax_rate = min(self.gov.tax_max_rate, self.gov.tax_rate + self.gov.tax_adj_rate)

        # 2. RECESSION: Growth is negative (e.g., -1%)
        elif economy_growth < 0:
            self.gov.tax_rate = max(self.gov.tax_min_rate, self.gov.tax_rate - self.gov.tax_adj_rate)

        # 3. OVERHEATING: Inflation is too high
        elif inflation_rate > target_inflation:
            self.gov.tax_rate = min(self.gov.tax_max_rate, self.gov.tax_rate + self.gov.tax_adj_rate)

        # 4. SURPLUS: Treasury is too high and economy is stable
        elif self.gov.treasury > self.gov.treasury_max:
            self.gov.tax_rate = max(self.gov.tax_min_rate, self.gov.tax_rate - self.gov.tax_adj_rate)
