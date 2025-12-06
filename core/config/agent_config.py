agent_config = {
    "food_consumption_rate": 1,     # food consumption per time
    "personal_food_supply": 20,     # initial food supply
    "travel_food_cost": 0.1,

    "replenishment_buffer": 5,      # Amount of additional food to buy
}

farmer_config = {
    "surplus_threshold": 5,         # Food amount needed for market trip
    "survival_buffer": 15,          # Minimum food to keep after selling
}

trader_config = {
    "max_inventory": 30,
    "buying_power": 10,             # Max units of goods they can try to buy
    "buying_aggression": 0.95       # Buy if the current price is 95% or less of base price
}
