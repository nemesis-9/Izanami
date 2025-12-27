memorial_template = {
    "AgentID": lambda a: a.unique_id,
    "AgentType": lambda a: getattr(a, 'agent_type', 'Unknown'),
    "DyingAge": lambda a: a.age,
    "DyingLocation": lambda a: str(a.pos),

    "DyingWealth": lambda a: round(a.wealth, 2),

    "DyingAction": lambda a: getattr(a, 'action', 'N/A'),
    "LeftFoods": lambda a: round(a.inventory.get("food", 0), 3),

    "DyingInv_ItemCount": lambda a: len(getattr(a, 'inventory', {})),
    "DyingInv_TotalVolume": lambda a: sum(
        v for v in getattr(a, 'inventory', {}).values()
        if isinstance(v, (int, float))
    )
}
