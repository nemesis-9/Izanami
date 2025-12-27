import streamlit as st

def overview(agent_data, model_data, selected_step):

    if 'step' not in st.session_state:
        st.session_state.step = 1

    title_col1, title_col2 = st.columns([4, 1], vertical_alignment="center")
    with title_col1:
        st.title('Izanami - Overview')
    with title_col2:
        semi_cols = st.columns(3, vertical_alignment="center")
        with semi_cols[1]:
            st.metric("Step", st.session_state.step)


    left_col, right_col = st.columns([3, 2])

    with left_col:
        current_agents = agent_data[agent_data['Step'] == selected_step].copy()
        st.subheader(f"Agent Population Status")

        cols_per_row = 4
        for i in range(0, len(current_agents), cols_per_row):
            row_agents = current_agents.iloc[i:i + cols_per_row]
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
                                    <div class="card-detail"><b>Foods:</b> {agent['Foods']}</div>
                                    <div class="card-detail"><b>Loc:</b> {agent['AgentLocation']}</div>
                                    <div class="card-detail"><b>Action:</b> {agent['Action']}</div>
                                </div>
                            """, unsafe_allow_html=True)

    with right_col:
        city_rows = model_data[model_data['Step'] == selected_step].reset_index(drop=True)
        if not city_rows.empty:
            current_city = city_rows.iloc[0]

            st.subheader("City Overview")

            st.info(f"**Season:** {current_city['CurrentSeason'].capitalize()}")

            st.write("**Demographics**")

            st.metric("Total Agents", int(current_city['TotalAgents']))
            st.caption(f"Agro: {current_city['Count_Agro']} | Farmer: {current_city['Count_Farmer']}")
            st.caption(f"Crafter: {current_city['Count_Crafter']} | Trader: {current_city['Count_Trader']}")

            st.divider()

            st.write("**Resource Pools**")

            res_cols = st.columns(3)
            res_cols[0].metric("Food", f"{current_city['FoodPool']:.2f}")
            res_cols[1].metric("Gold", f"{current_city['GoldPool']:.2f}")
            res_cols[2].metric("Iron", f"{current_city['IronPool']:.2f}")
            res_cols[0].metric("Copper", f"{current_city['CopperPool']:.2f}")

            st.divider()

            st.write("**Market Prices**")

            price_cols = st.columns(3)
            price_cols[0].metric("Food Price", f"${current_city['FoodPrice']:.2f}")
            price_cols[1].metric("Iron Price", f"${current_city['IronPrice']:.2f}")
            price_cols[2].metric("Copper Price", f"${current_city['CopperPrice']:.2f}")
            price_cols[0].metric("Gold Price", f"${current_city['GoldPrice']:.2f}")

            st.divider()

            st.write("**Economy & Governance**")

            eco_cols = st.columns(2)
            eco_cols[0].metric("Total Wealth", f"${current_city['TotalWealth']:.2f}")
            eco_cols[1].metric("Treasury", f"${current_city['Treasury']:.2f}")

            tax_col, aid_col = st.columns(2)
            tax_col.metric("Tax Rate", f"{current_city['TaxRate'] * 100:.1f}%")
            aid_col.metric("Aid (Food)", f"{current_city['AidFund_Food']:.0f}")

            st.caption(f"Total Tax: ${current_city['TotalTaxCollected']:.2f}")
        else:
            st.warning("No data for this step.")
