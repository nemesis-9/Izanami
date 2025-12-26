reporter_model = {
    "Step": lambda m: m.steps,
    "CurrentSeason": lambda m: m.current_season,
    "TotalAgents": lambda m: len(m.agents),

    "Count_Agro": lambda m: len([a for a in m.agents if a.agent_type == 'agro']),
    "Count_Crafter": lambda m: len([a for a in m.agents if a.agent_type == 'crafter']),
    "Count_Farmer": lambda m: len([a for a in m.agents if a.agent_type == 'farmer']),
    "Count_Trader": lambda m: len([a for a in m.agents if a.agent_type == 'trader']),

    "TotalWealth": lambda m: round(sum(a.wealth for a in m.agents), 2),
    "EconomyWealth": lambda m: round(m.economy.wealth, 2),

    "FoodPool": lambda m: m.economy.resource_pools.get("food", 0),
    "IronPool": lambda m: m.economy.resource_pools.get("food", 0),
    "CopperPool": lambda m: m.economy.resource_pools.get("food", 0),
    "GoldPool": lambda m: m.economy.resource_pools.get("food", 0),

    "FoodPrice": lambda m: round(m.economy.calculate_price("food"), 0),
    "IronPrice": lambda m: round(m.economy.calculate_price("food"), 0),
    "CopperPrice": lambda m: round(m.economy.calculate_price("food"), 0),
    "GoldPrice": lambda m: round(m.economy.calculate_price("food"), 0),

    "Treasury": lambda m: round(m.governance.treasury, 2),
    "TotalTaxCollected": lambda m: round(m.governance.total_tax_collected, 2),
    "TotalPublicSpending": lambda m: round(m.governance.total_public_spending, 2),
    "TaxRate": lambda m: round(m.governance.tax_rate, 4),

    "AidFund_Food": lambda m: m.governance.aid_fund.get("food", 0),
}
