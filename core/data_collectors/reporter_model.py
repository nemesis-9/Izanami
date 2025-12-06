reporter_model = {
    "TotalAgents": lambda m: len(m.agents),
    "FoodPool": lambda m: m.economy.resource_pools.get("food", 0),
    "TotalWealth": lambda m: sum(a.wealth for a in m.agents),
    "FoodPrice": lambda m: m.economy.price_pools.get("food", 0),
}
