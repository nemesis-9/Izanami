## 💰 Trader.md: Mercantile and Inventory Management Agent

The `Trader` agent specializes in **arbitrage**—buying goods cheaply and selling them at a higher price to generate profit. It manages a dynamic **inventory** and switches between **buying** and **selling** modes based on its strategy and current market conditions.

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Mode Toggle** | Switches the agent's primary state between **'selling'** and **'buying'**. | Toggled when the agent runs out of resources to sell (in 'selling' mode) or runs out of money/hits max inventory (in 'buying' mode). |
| **Movement Strategy** | Directs the trader to the appropriate location based on its current `mode`. | In **'selling'** mode, the destination is the **market**. In **'buying'** mode, the destination is the **city center**. |
| **Determine Buy Need** | Checks if the trader should buy goods. | Returns a list of resources the trader is configured to buy, provided their **current price** is less than or equal to the agent's price limit (derived from `buying_aggression` and the base price). Also checks **wealth** and **max inventory**. |
| **Determine Sell Need** | Checks if the trader should sell goods. | Returns a list of resources the trader holds, provided their **current price** is greater than or equal to the agent's price limit (derived from `selling_aggression` and the base price). |
| **Buy Goods** | Executes purchase transactions upon reaching the designated location (e.g., city center). | Prioritizes buying the cheapest suitable resources. The **quantity** is limited by the agent's **wealth**, **max inventory**, and resource-specific **`buying_power`**. Updates `wealth` and `inventory`. |
| **Sell Goods** | Executes sales transactions upon reaching the designated location (e.g., market). | Prioritizes selling the most profitable suitable resources. The **quantity** is limited by the agent's inventory and resource-specific **`selling_power`**. Updates `wealth` and `inventory`. |
| **Step Order** | The agent first ensures **survival** (consumes food). Then, it **updates configuration** and attempts to **move**. If it is stationary at an exchange point (market or city center), it attempts to **sell** and then **buy** goods. |

---

### ⚙️ Parameter Explanation (Specific to Trader)

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| **`inventory`** | dict | A dictionary tracking the quantity of each resource currently held by the trader. |
| **`max_inventory`** | int | The maximum total quantity of goods the trader can hold at any time. |
| **`mode`** | string | Determines the agent's primary activity: 'buying' or 'selling'. |
| **`buying_power`** | dict | The maximum monetary amount the agent is willing to spend on a specific resource per transaction. |
| **`buying_aggression`** | float | A factor that scales the base price to set the maximum price the trader is willing to pay (e.g., 1.0 means buying at or below the base price). |
| **`selling_power`** | dict | The maximum quantity of a specific resource the agent is willing to sell per transaction. |
| **`selling_aggression`** | float | A factor that scales the base price to set the minimum price the trader is willing to accept (e.g., 1.0 means selling at or above the base price). |
| **`inventory_margin`** | float | A threshold (as a fraction of `max_inventory`) used to trigger a mode switch to 'selling' once inventory reaches this level. |
| **`wealth_margin`** | float | A minimum wealth level used to trigger a mode switch to 'selling' if the agent's wealth drops below this amount. |