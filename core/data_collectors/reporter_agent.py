reporter_agent = {
    "AgentID": lambda a: a.unique_id,
    "AgentType": lambda a: getattr(a, 'agent_type', 'Unknown'),
    "Age": lambda a: a.age,
    "IsAlive": lambda a: a.alive,
    "AgentLocation": lambda a: str(a.pos),

    "Wealth": lambda a: round(a.wealth, 2),
    "HealthPoints": lambda a: a.hp,

    "Mode": lambda a: getattr(a, 'mode', 'N/A'),
    "PersonalFoodSupply": lambda a: getattr(a, 'personal_food_supply', 0),

    "Inventory_ItemCount": lambda a: len(getattr(a, 'inventory', {})),
    "Inventory_TotalVolume": lambda a: sum(
        v for v in getattr(a, 'inventory', {}).values()
        if isinstance(v, (int, float))
    )
}
