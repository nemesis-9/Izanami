import os
import shutil
import pandas as pd

from core.models.world import WorldModel

from core.data_collectors.reporter_agent import reporter_agent
from core.data_collectors.reporter_model import reporter_model

CURRENT_PHASE = 8.5

if __name__ == '__main__':
    print("--- Starting City Simulation Test ---")

    NUM_AGRO = 5
    NUM_CRAFTERS = 5
    NUM_FARMERS = 10
    NUM_TRADERS = 5
    NUM_STEPS = 100

    world = WorldModel(
        cities=1,
        seasons=['spring', 'summer', 'autumn', 'winter'],
        width=20,
        height=20,
        agro=NUM_AGRO,
        crafters=NUM_CRAFTERS,
        farmers=NUM_FARMERS,
        traders=NUM_TRADERS,
        model_reporters=reporter_model,
        agent_reporters=reporter_agent
    )

    city_instance = world.city_models[0]

    # --- Run Simulation ---
    for i in range(NUM_STEPS):
        print(f"\nWorld Step {world.steps + 1}:")
        world.step()

    print("\n--- Simulation Test Complete ---")

    # --- Output Management ---
    output_dir = f"../data/output/phase{CURRENT_PHASE}"
    if os.path.exists(output_dir):
        print(f"Directory {output_dir} exists. Deleting and recreating for clean run.")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # --- Data Extraction ---
    model_data = city_instance.datacollector.get_model_vars_dataframe()

    try:
        agent_data = city_instance.datacollector.get_agent_vars_dataframe()

    except Exception as e:
        print(f"Warning: Mesa's get_agent_vars_dataframe failed ({e}). Falling back to custom logic.")

        agent_columns = list(reporter_agent.keys())
        records = []
        for step, agents_at_step in city_instance.datacollector._agent_records.items():
            for agent_data_tuple in agents_at_step:
                row = dict(zip(agent_columns, agent_data_tuple[2:]))
                row["Step"] = step
                records.append(row)
        agent_data = pd.DataFrame.from_records(records)

    memorial_entries = city_instance.governance.memorial_log
    memorial_df = pd.DataFrame(memorial_entries)

    model_filename = os.path.join(output_dir, "model_data.csv")
    agent_filename = os.path.join(output_dir, "agent_data.csv")
    memorial_filename = os.path.join(output_dir, "memorial_log.csv")

    model_data.to_csv(model_filename)
    agent_data.to_csv(agent_filename)
    memorial_df.to_csv(memorial_filename, index=False)

    print(f"Model data saved to: {model_filename}")
    print(f"Agent data saved to: {agent_filename}")
    print("---------------------------------------------")
