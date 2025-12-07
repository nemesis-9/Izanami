## 🔨 Crafter.md: Production and Trade Cycle Agent

The `Crafter` agent is specialized for **manufacturing**. Its logic follows a three-stage cycle: **buying raw materials**, **crafting** the final product at home, and **selling** the output at a central location.

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Mode Toggle** | Cycles the agent's primary state through three modes: **'buying'** $\to$ **'crafting'** $\to$ **'selling'**. | Switches based on resource needs (buying), material availability (crafting), and inventory levels (selling). |
| **Movement Strategy** | Directs the agent based on its current `mode`. | Moves to the **market** for **'buying'** materials. Moves to the **city center** for **'selling'** finished goods. Moves to the **`home_location`** for **'crafting'**. |
| **Determine Buy Need** | Checks if the agent needs to purchase raw materials. | Looks at the resources configured for buying in `crafter_global_var['buy']`. Only returns resources if the agent has **wealth**, has not hit **`max_inventory`**, and its current inventory for that specific material is below its allocated **`buying_power`** threshold. |
| **Determine Sell Need** | Checks if the agent needs to sell finished goods. | Looks at resources configured for selling in `crafter_global_var['sell']`. Only returns resources if the agent has a **surplus** (inventory amount exceeds the specified **`selling_power`** threshold). |
| **Buy Materials** | Executes purchases at the market or city center. | Buys the needed resources (cheapest first) up to limits set by **wealth**, **`max_inventory`**, and **`buying_power`**. Triggers a mode toggle if materials are acquired or if wealth/inventory limits are hit. |
| **Sell Goods** | Executes sales at the city center. | Sells surplus resources (highest price first) up to the limit set by **`selling_power`**. Triggers a mode toggle when the sellable surplus is exhausted. |
| **Craft** | **(TODO: Logic Pending)** This function, executed at the `home_location`, is where the raw materials in the `inventory` will be converted into finished goods. Currently, it just returns `True`. | The core production function, executed when the agent is stationary at home. |
| **Step Order** | The agent follows the sequence: **Survival** (consume food) $\to$ **Config Update** $\to$ **Move**. If stationary, the agent executes the action matching its location (Buy at Market, Sell at City Center, Craft at Home). |

---

### ⚙️ Parameter Explanation (Specific to Craftsman)

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| **`inventory`** | dict | Tracks the quantity of both **raw materials** and **finished products**. |
| **`crafting_rate`** | int | The speed or efficiency at which the craftsman can convert materials into products (used in the `craft()` function). |
| **`mode`** | string | Defines the agent's current focus: 'buying', 'crafting', or 'selling'. |
| **`max_inventory`** | int | The total capacity for holding all materials and goods. |
| **`buying_power`** | dict | The maximum quantity of a raw material the agent attempts to stock or purchase at once. |
| **`selling_power`** | dict | The minimum quantity of a finished good the agent retains before selling any surplus, and the maximum quantity to sell per transaction. |
| **`inventory_margin`** | float | A threshold (fraction of `max_inventory`) used to trigger a mode switch to 'selling' or 'crafting' once inventory levels are high. |
| **`wealth_margin`** | float | A minimum wealth level used to trigger a mode switch to 'selling' to replenish funds. |