from gov_aid import GovAid
from gov_tax import GovTax


class Governance:
    def __init__(self, model, governance_variables):
        self.model = model

        self.total_tax_collected = 0
        self.total_public_spending = 0

        self.aid_logic = GovAid()
        self.tax_logic = GovTax()

        self.treasury = governance_variables.get('initial_budget', 0)
        self.treasury_min = governance_variables.get('treasury_min', 0)
        self.treasury_max = governance_variables.get('treasury_max', 0)

        self.tax_rate = governance_variables.get('tax_rate', 0)
        self.tax_min_rate = governance_variables.get('tax_min_rate', 0)
        self.tax_max_rate = governance_variables.get('tax_max_rate', 1)
        self.tax_inc_rate = governance_variables.get('tax_inc_rate', 0.01)
        self.tax_threshold = governance_variables.get('tax_threshold', 0)

        self.aid_fund = governance_variables.get('aid_fund', {})
        self.aid_amount = governance_variables.get('aid_amount', {})
        self.aid_price_margin = governance_variables.get('aid_price_margin', {})
        self.aid_threshold = governance_variables.get('aid_threshold', {})

    def collect_taxes(self):
        self.tax_logic.adjust_tax_rate(self)
        self.tax_logic.collect_taxes(self)

    def fund_public_services(self):
        self.aid_logic.fund_aid(self)

    def distribute_aid(self):
        self.aid_logic.distribute_aid(self)
