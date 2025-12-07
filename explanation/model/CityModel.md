## 🏙️ CityModel.md: Simulation and Environmental Management

The `CityModel` is the **core container** that defines the environment, initializes all agents and subsystems, manages the simulation time, and enforces the **seasonal cycle**.

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Initialization** | Sets up the entire simulation environment. | Creates a **`MultiGrid`** for agent placement and a **`CityNetwork`** for movement. Initializes the **`Economy`** subsystem and defines initial global parameters (variables). |
| **Agent Spawning** | Places initial agents (e.g., `Farmer`, `Trader`) randomly on the grid. | Sets initial `wealth` and assigns the appropriate configuration variables based on the current `season`. |
| **Seasonal Cycle** | Updates the global environment every `season_length` steps. | Increments the **`current_season_index`** and retrieves new configuration parameters (`base_variables`, `farmer_variables`, etc.) from the global configuration system based on the new season. |
| **Step Execution** | Defines the sequence of events that occur in every simulation time step. | 1. **Update Season**. 2. **Economy Step** (updates prices, etc.). 3. All agents execute their **`step`** logic in a random order. |
| **Agent Cleanup** | Removes agents that have died (e.g., from starvation) from the simulation. | Identifies agents where `alive == False` and removes them from the model's schedule. |
| **Data Collection** | Records the state of the model and agents for analysis. | The **`DataCollector`** gathers defined metrics every step. |

---

### ⚙️ Parameter Explanation (Core Components)

| Component | Type | Purpose |
| :--- | :--- | :--- |
| **`grid`** | `MultiGrid` | The 2D space where agents reside. It allows multiple agents to occupy the same location. |
| **`city_network`** | `CityNetwork` | A spatial layer that manages paths, points of interest (market, city center), and handles movement logic for agents. |
| **`economy`** | `Economy` Subsystem | Manages all resource pools (supply), tracks wealth flow, and calculates dynamic prices based on supply and demand forces. |
| **`seasons` / `season_length`** | list / int | Define the sequence of environmental states (e.g., ['Spring', 'Winter']) and how long each state lasts before parameters change. |
| **`base_variables`** | dict | Global parameters (like `food_consumption_rate`) that apply to all agents and are updated each season. |
| **`datacollector`** | `DataCollector` | The Mesa tool used to log simulation data, essential for analyzing the model's long-term behavior. |