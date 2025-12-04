import os
import shutil
import pandas as pd

from core.models.world import WorldModel
from core.models.city import CityModel

MODEL_REPORTERS = {
    "TotalAgents": lambda m: len(m.agents),
    "FoodPool": lambda m: m.economy.resource_pools.get("food", 0),
    "TotalWealth": lambda m: sum(a.wealth for a in m.agents),
}

AGENT_REPORTERS = {
    "AgentID": lambda a: a.unique_id,
    "AgentLocation": lambda a: a.location,
    "AgentType": lambda a: getattr(a, 'agent_type', 'Unknown'),
    "Age": lambda a: a.age,
    "Wealth": lambda a: a.wealth,
}


if __name__ == '__main__':
    print("--- Starting City Simulation Test ---")

    world = WorldModel(cities=1)

    city_instance = CityModel(
        unique_id=1,
        parent_world=world,
        width=100,
        height=100,
        agents=10,
        farmers=15,
        agent_reporters=AGENT_REPORTERS
    )
    world.city_models.append(city_instance)

    for i in range(10):
        print(f"\nWorld Step {world.steps + 1}:")
        world.step()

    print("\n--- Simulation Test Complete ---")

    output_dir = "../data/output/phase2"
    if os.path.exists(output_dir):
        print(f"Directory {output_dir} exists. Deleting and recreating for clean run.")
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    model_data = city_instance.datacollector.get_model_vars_dataframe()
    # agent_data = city_instance.datacollector.get_agent_vars_dataframe()

    # agent data manual creation
    # agent_table = city_instance.datacollector._agent_records
    # records = []
    # for step, agents_at_step in agent_table.items():
    #     for agent_row in agents_at_step:
    #         row = {"Step": step}
    #         if isinstance(agent_row, dict):
    #             row.update(agent_row)
    #         elif hasattr(agent_row, "to_dict"):
    #             row.update(agent_row.to_dict())
    #         elif isinstance(agent_row, (list, tuple)):
    #             row["AgentID"] = agent_row[0]
    #         else:
    #             raise TypeError(f"Unsupported agent_row type: {type(agent_row)}")
    #         records.append(row)
    # agent_data = pd.DataFrame.from_records(records)
    # if not agent_data.empty:
    #     agent_data = agent_data.set_index(['Step', 'AgentID'])

    AGENT_COLUMNS = list(AGENT_REPORTERS.keys())
    records = []
    for step, agents_at_step in city_instance.datacollector._agent_records.items():
        for agent_data_tuple in agents_at_step:
            row = dict(zip(AGENT_COLUMNS, agent_data_tuple[2:]))
            row["Step"] = step
            records.append(row)
    agent_data = pd.DataFrame.from_records(records)

    model_filename = os.path.join(output_dir, "model_data_test.csv")
    agent_filename = os.path.join(output_dir, "agent_data_test.csv")

    model_data.to_csv(model_filename)
    agent_data.to_csv(agent_filename)

    print(f"Model data saved to: {model_filename}")
    print(f"Agent data saved to: {agent_filename}")
    print("---------------------------------------------")
