## 🧑‍🌾 Farmer.md: Production and Trading Agent Logic

The `Farmer` agent inherits all survival and movement capabilities from the `BaseAgent`. Its specialized role is **producing food** and bringing its **surplus** to the market to **trade for wealth**.

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Produce** | Generates food when the farmer is at their `home_location`. | Adds a fixed **`food_production_rate`** to the agent's **`personal_food_supply`**. |
| **Sell** | Sells surplus food to the central `economy` when at the market. | Calculates food **surplus** above a **`survival_buffer`**. The farmer is paid based on the current market price, increasing their **`wealth`** and decreasing the `economy`'s wealth. |
| **Movement Strategy** | Determines the agent's destination based on its current food stock. | If **`personal_food_supply`** exceeds the **`surplus_threshold`**, the destination is the **market**. Otherwise, the destination is the **`home_location`** (to produce food). |
| **Step Order** | Defines the action sequence each turn. | The farmer first attempts to **survive (consume)**. Then, it attempts to **move**. If movement fails (i.e., the agent is at its destination), it either **produces** (if at home) or **sells** (if at the market). |

---

### ⚙️ Parameter Explanation (Specific to Farmer)

| Parameter | Type | Purpose | Inherited from BaseAgent |
| :--- | :--- | :--- | :--- |
| **`food_production_rate`** | int | The amount of food produced by the farmer when working at home. | No |
| **`has_farm_plot`** | bool | Simple flag indicating if the agent owns a farm (currently always `True`). | No |
| **`surplus_threshold`** | float | The amount of food supply an agent must exceed before deciding to travel to the market to sell. | No |
| **`survival_buffer`** | float | The minimum amount of food the farmer attempts to retain in their personal supply and avoid selling. | No |
| **`home_location`** | tuple | The fixed location where the farmer lives and produces food. | Yes |
| **`destination`** | tuple | The current target coordinates for the movement logic (either market or home). | Yes |