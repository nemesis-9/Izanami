import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Izanami - ABM Model Dashboard 01")

st.markdown("""
<style>
    .agent-card {
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        height: 100%;
    }
    .alive-card {
        border: 2px solid #28a745;
        background-color: #f8fff9;
    }
    .dead-card {
        border: 2px solid #dc3545;
        background-color: #fff8f8;
    }
    .status-label {
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.8rem;
        padding: 2px 6px;
        border-radius: 4px;
        color: white;
    }
    .status-alive { background-color: #28a745; }
    .status-dead { background-color: #dc3545; }
    .card-title { font-weight: bold; font-size: 1.1rem; margin-bottom: 5px; }
    .card-detail { font-size: 0.9rem; color: #555; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    agent_df = pd.read_csv('../data/output/phase7/agent_data_test.csv')
    model_df = pd.read_csv('../data/output/phase7/model_data_test.csv')
    return agent_df, model_df


try:
    agent_data, model_data = load_data()

    st.title('Izanami - ABM Model Dashboard 01')
    st.markdown("A real-time visualization of agent states and city-level metrics across simulation steps.")

    max_steps = int(model_data['Step'].max())
    selected_step = st.slider('Select a step', min_value=1, max_value=max_steps, value=1)

    current_agents = agent_data[agent_data['Step'] == selected_step].copy()

    city_rows = model_data[model_data['Step'] == selected_step].reset_index(drop=True)
    if city_rows.empty:
        st.warning(f"Step {selected_step} has no data.")
        st.stop()
    current_city = city_rows.iloc[0]

    left_col, right_col = st.columns([4, 1])

    with left_col:
        st.subheader(f"Agent Status - Step {selected_step}")

        cols_per_row = 4
        for i in range(0, len(current_agents), cols_per_row):
            row_agents = current_agents.iloc[i:i+cols_per_row]
            grid_cols = st.columns(cols_per_row)

            for idx, (index, agent) in enumerate(row_agents.iterrows()):
                is_alive = agent['IsAlive']
                status_class = "alive-card" if is_alive else "dead-card"
                status_text = 'ALIVE' if is_alive else 'DEAD'
                status_label_class = "status-alive" if is_alive else "status-dead"

                with grid_cols[idx]:
                    st.markdown(f"""
                        <div class="agent-card {status_text}">
                            <span class="status-label {status_label_class}">{status_text}</span>
                            <div class="card-title">Agent ID: {agent['AgentID']}</div>
                            <div class="card-detail"><b>Type:</b> {agent['AgentType']}</div>
                            <div class="card-detail"><b>Health:</b> {agent['HealthPoints']:.1f}</div>
                            <div class="card-detail"><b>Wealth:</b> ${agent['Wealth']:.2f}</div>
                            <div class="card-detail"><b>Food:</b> {agent['PersonalFoodSupply']}</div>
                            <div class="card-detail"><b>Loc:</b> {agent['AgentLocation']}</div>
                        </div>
                    """, unsafe_allow_html=True)

    with right_col:
        st.subheader("City Overview")
        st.info(f"**Season:** {current_city['CurrentSeason'].capitalize()}")

        st.write("**Demographics**")
        st.metric("Total Agents", int(current_city['TotalAgents']))
        st.caption(f"Agro: {current_city['Count_Agro']} | Farmer: {current_city['Count_Farmer']}")
        st.caption(f"Crafter: {current_city['Count_Crafter']} | Trader: {current_city['Count_Trader']}")

        st.divider()

        st.write("**Resource Pools**")
        res_cols = st.columns(2)
        res_cols[0].metric("Food", f"{current_city['FoodPool']:.0f}")
        res_cols[1].metric("Gold", f"{current_city['GoldPool']:.0f}")
        res_cols[0].metric("Iron", f"{current_city['IronPool']:.0f}")
        res_cols[1].metric("Copper", f"{current_city['CopperPool']:.0f}")

        st.divider()

        st.write("**Market Prices**")
        st.metric("Food Price", f"${current_city['FoodPrice']:.2f}")
        st.metric("Iron Price", f"${current_city['IronPrice']:.2f}")

        st.divider()

        st.write("**Economy**")
        st.metric("Treasury", f"${current_city['Treasury']:.2f}")
        st.metric("Tax Rate", f"{current_city['TaxRate'] * 100:.1f}%")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Ensure 'agent_data_test.csv' and 'model_data_test.csv' exists!")
