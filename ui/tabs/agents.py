import streamlit as st


def agents(agent_data, model_data):
    if 'step' not in st.session_state:
        st.session_state.step = 1

    title_col, state_col = st.columns([4, 1], vertical_alignment="center")
    with title_col:
        st.title('Izanami - Agent View')
    with state_col:
        semi_cols = st.columns(3, vertical_alignment="center")
        with semi_cols[1]:
            st.metric("Step", st.session_state.step)

    left_col, right_col = st.columns([4, 1])

    with left_col:

        # st.subheader(f"Agent Population Status")

        step_data = agent_data[agent_data['Step'] == st.session_state.step].copy()
        available_types = sorted(step_data['AgentType'].unique().tolist())

        filter_cols = st.columns([0.1, 8, 1])
        with filter_cols[1]:
            selected_types = st.multiselect(
                "",
                options=available_types,
                default=available_types,
                format_func=lambda x: x.capitalize()
            )

        if selected_types:
            current_agents = step_data[agent_data['AgentType'].isin(selected_types)]
        else:
            current_agents = step_data.iloc[0:0]

        cols_per_row = 5
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
        city_rows = model_data[model_data['Step'] == st.session_state.step].reset_index(drop=True)

        prev_step = st.session_state.step - 1
        prev_city_rows = model_data[model_data['Step'] == prev_step].reset_index(drop=True)

        if not city_rows.empty:
            current_city = city_rows.iloc[0]

            def get_delta(column_name):
                if prev_city_rows.empty:
                    return None
                return int(current_city[column_name]) - int(prev_city_rows.iloc[0][column_name])

            st.subheader("Demographics")

            st.metric("Total Agents", int(current_city['TotalAgents']), delta=get_delta('TotalAgents'))

            if selected_types:
                agent_type_cols = st.columns(3)

                for i, agent_type in enumerate(selected_types):
                    agent_type = agent_type.capitalize()
                    column_key = f'Count_{agent_type}'

                    with agent_type_cols[i % 3]:
                        st.metric(
                            label=agent_type,
                            value=int(current_city.get(column_key, 0)),
                            delta=get_delta(column_key)
                        )
