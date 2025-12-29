from collections import Counter


def get_agent_counts(model):
    counts = Counter(a.agent_type for a in model.agents if a.alive)
    return str(dict(counts))


reporter_model = {
    "Step": lambda m: m.steps,
    "CurrentSeason": lambda m: m.current_season,

    # Agent
    "TotalAgents": lambda m: len([a for a in m.agents if a.alive]),
    "LivingAgents": lambda m: get_agent_counts(m),

    "TotalAgentWealth": lambda m: round(sum(a.wealth for a in m.agents), 2),

    # Economy
    "EconomyWealth": lambda m: round(m.economy.wealth, 2),

    "ResourcePool": lambda m: str(getattr(m.economy, 'resource_pools', {})),
    "PricePool": lambda m: str(getattr(m.economy, 'price_pools', {})),

    "BasePrices": lambda m: str(getattr(m.economy, 'base_prices', {})),
    "TargetSupply": lambda m: str(getattr(m.economy, 'target_supply', {})),

    "EconomyMetrics": lambda m: str(getattr(m.economy_metrics, 'current_metrics', {})),

    # Government
    "TotalTaxCollected": lambda m: round(m.governance.total_tax_collected, 2),
    "TotalPublicSpending": lambda m: round(m.governance.total_public_spending, 2),
    "GovInventory": lambda m: str(getattr(m.governance, 'inventory', {})),

    "Treasury": lambda m: round(m.governance.treasury, 2),
    "TaxRate": lambda m: round(m.governance.tax_rate, 4),

    "AidFund": lambda m: str(getattr(m.governance, "aid_fund", {})),
}
