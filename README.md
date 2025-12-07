# 🏙️ Agent-Based City Economy Simulation

## 🌟 Project Purpose

This project is an **Agent-Based Model (ABM)** simulating a simple city economy. The goal is to observe the dynamic emergence of market behavior, resource distribution, and agent survival based on the interactions between different specialized agents (Farmers, Traders, Craftsmen) and a central **Economy** subsystem.

The simulation focuses on:
* **Dynamic Pricing:** How resource prices fluctuate based on supply and demand forces.
* **Survival Mechanics:** How agents manage their resources (wealth and food) to stay alive.
* **Trade Cycles:** The cyclical movement of agents (buying, selling, producing) to sustain the economy.
* **Environmental Impact:** How global parameters change based on a **Seasonal Cycle**.

---

## 🚀 How to Start the Simulation

The project is built using the **Mesa framework**. The following is the way to run and interact with the model.

### 1. Backend Run (Terminal/CLI)

First run the simulation for collecting large datasets.

1.  **Install Dependencies:** Ensure all required libraries (Mesa, pandas, etc.) are installed.
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Model:** Execute the main Python file that initializes and run. `/runs/interactive_run.py`
    ```bash
    python interactive_run.py
    ```

### 2. Jupyter Notebook (Interactive Analysis)

Next notebooks for interactive execution, visualization, and immediate data analysis.

1.  **Start Jupyter:** Launch the Jupyter Notebook server.
    ```bash
    jupyter notebook
    ```
2.  **Open the Notebook:** Navigate to `analyze` and open the notebook (e.g., `testbook_p5.ipynb`).
3.  **Execute Cells:** Run the cells sequentially to initialize the model, run the steps, and analyze the resulting data.

---

## 🛠️ Key Components

| Component | Description |
| :--- | :--- |
| **`CityModel`** | The environment manager; handles the grid, scheduler, **seasonal cycles**, and data collection. |
| **`Economy`** | The central market mechanism; manages **resource pools**, the system's wealth, and **dynamic price calculation** (elasticity). |
| **`BaseAgent`** | The blueprint for all agents; contains core logic for survival (`consume`), aging, and pathfinding movement. |
| **`Farmer`** | **Producer** agent; generates food at home and sells **surplus** at the market. |
| **`Trader`** | **Arbitrage** agent; cycles between buying low and selling high to maximize wealth. |
| **`Crafter`** | **Manufacturer** agent; buys raw materials, performs **crafting** at home, and sells finished goods. |

---

## 🗂️ Documentation

The detailed logic for each agent and subsystem is documented in the dedicated Markdown files located in the `explanation` directory.
