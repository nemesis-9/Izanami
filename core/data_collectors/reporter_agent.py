reporter_agent = {
    "AgentID": lambda a: a.unique_id,
    "AgentType": lambda a: getattr(a, 'agent_type', 'Unknown'),
    "Age": lambda a: a.age,
    "IsAlive": lambda a: a.alive,
    "AgentLocation": lambda a: str(a.pos),

    "Wealth": lambda a: round(a.wealth, 2),
    "HealthPoints": lambda a: a.hp,

    "Action": lambda a: getattr(a, 'action', 'N/A'),
    "Foods": lambda a: round(a.inventory.get("food", 0), 3),

    "Inventory_ItemCount": lambda a: len(getattr(a, 'inventory', {})),
    "Inventory_TotalVolume": lambda a: sum(
        v for v in getattr(a, 'inventory', {}).values()
        if isinstance(v, (int, float))
    )
}
