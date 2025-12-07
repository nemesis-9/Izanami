## 💲 Economy.md: Market and Resource Management Subsystem

The `Economy` is a **centralized subsystem** that controls all resource transactions, manages the overall wealth of the model, and calculates **dynamic prices** for goods based on supply (resource pools).

---

### 🧠 Underlying Logic (Actions)

| Action | Description | Key Mechanism |
| :--- | :--- | :--- |
| **Calculate Price** | Determines the current market price for a given resource. | Uses a **simple inverse relationship**: `New Price = Base Price - (Resource Pool * Price Elasticity)`. This ensures that **higher supply** leads to **lower prices**. The calculated price is always enforced to be above the **`minimum_threshold`**. |
| **Add Resource (Supply)** | Represents an agent (like a Farmer) selling a resource *to the economy*. | When an agent sells, the resource is added to the **`resource_pools`**. The economy determines how much it can *afford* to buy based on the **`wealth`** of the economy and the **`wealth_margin`** multiplier, preventing the economy from overspending. |
| **Request Resource (Demand)** | Represents an agent (like a Trader or Craftsman) buying a resource *from the economy*. | Checks if the requested `amount` is available in the **`resource_pools`**. The agent gains the minimum of the requested amount or the available stock. The resource is immediately **deducted** from the pool. |
| **Step Execution** | The mandatory action every step to ensure prices reflect current supply. | Iterates through all resources in the **`resource_pools`** and recalculates their prices using `calculate_price()`, immediately updating the **`price_pools`**. |

---

### ⚙️ Parameter Explanation (Core Components)

| Parameter | Type | Purpose |
| :--- | :--- | :--- |
| **`wealth`** | float | The current monetary holdings of the central economy itself. This pool is used to pay agents for resources they sell to the system. |
| **`wealth_margin`** | float | A factor (e.g., 0.8) that limits the economy's spending, defining the *affordable cost* it is willing to pay for resources in a single transaction. |
| **`resource_pools`** | dict | The current **supply** of all tradable goods available in the market. Keys are resource names, values are quantities. |
| **`price_pools`** | dict | The calculated, current market price for each resource. |
| **`base_prices`** | dict | The default or theoretical price for a resource when the supply pool is zero. |
| **`price_elasticities`** | dict | A factor that controls *how sensitive* the price is to changes in supply. Higher elasticity means a small change in `resource_pools` results in a large price change. |
| **`minimum_threshold`** | dict | The absolute lowest price a resource can fall to, even with excessive supply. |