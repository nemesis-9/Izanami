## 📝 BaseAgent.md: Core Agent Logic

The `BaseAgent` serves as the **blueprint for all entities** in the simulation. Its primary underlying logic revolves around **survival, resource management, and movement**.

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Survival Check** | Executed every step to ensure the agent is alive. | Calls `consume()`. If consumption fails due to lack of money or food, the agent's `alive` status is set to `False`. |
| **Consume (Eat/Buy)** | The critical loop for managing food supply. | Checks if **personal food supply** is sufficient. If not, the agent attempts to **buy food** from the model's `economy`. It prioritizes buying enough food to survive plus a **replenishment buffer**, using its **wealth**. |
| **Move** | Facilitates movement between locations using a pathfinding mechanism. | The agent consumes **`travel_food_cost`** and moves one step along a calculated **`path`** to its destination. |
| **Aging** | Increments the agent's `age` by one unit every step. | Simple counter tracking the agent's lifespan. |
| **Config Update** | Ensures the agent uses the latest global settings defined by the model. | Updates its local parameters (e.g., `food_consumption_rate`) from the model's global variables. |

---

### ⚙️ Parameter Explanation

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| **`wealth`** | float | Monetary resources used for transactions (e.g., buying food). |
| **`personal_food_supply`** | float | Current stock of food the agent possesses. |
| **`food_consumption_rate`** | float | Amount of food consumed per simulation step. |
| **`travel_food_cost`** | float | Food cost deducted for each step taken during movement. |
| **`replenishment_buffer`** | float | An extra amount of food the agent attempts to buy for reserves when its supply is low. |
| **`location`** | tuple | The (x, y) coordinates of the agent on the grid. |
| **`path`** | list | A sequence of coordinates defining the agent's current route. |