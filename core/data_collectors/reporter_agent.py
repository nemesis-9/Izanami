reporter_agent = {
    "AgentID": lambda a: a.unique_id,
    "AgentLocation": lambda a: a.location,
    "AgentType": lambda a: getattr(a, 'agent_type', 'Unknown'),
    "Age": lambda a: a.age,
    "Wealth": lambda a: a.wealth,
}
