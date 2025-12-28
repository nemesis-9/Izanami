import streamlit as st
import ast

from ui.components.agentCard import agent_card


def agent_tab(agent_data, model_data):
    header_cols = st.columns([9, 2])

    with header_cols[0]:
        st.markdown("""
        <div class="flex flex-col border-l-4 border-purple-600 pl-6 py-2">
            <h1 class="text-6xl font-black text-white tracking-tighter flex items-center gap-4">
                <span class="shining-title" style="font-size: 4rem; font-weight: 900; letter-spacing: -2px; font-style: italic;">
                    IZANAMI
                </span>
                <span class="bg-purple-600 text-xs font-mono tracking-normal px-2 py-1 rounded italic text-purple-100">
                    AGENTS
                </span>
            </h1>
            <p class="text-purple-400/60 font-mono text-sm mt-1 uppercase tracking-widest">
                Strategic Oversight & Biomass Recovery Logistics
            </p>
        </div>
        """, unsafe_allow_html=True)

    with header_cols[1]:
        spc = st.columns(3)
        with spc[1]:
            st.metric("Step", st.session_state.step)

    left_col, right_col = st.columns([9, 2])

    with left_col:
        st.divider()

        step_data = agent_data[agent_data['Step'] == st.session_state.step].copy()
        available_types = sorted(step_data['AgentType'].unique().tolist())

        filter_cols = st.columns([0.1, 8, 1])
        with filter_cols[1]:
            selected_types = st.multiselect(
                "Agent Type",
                options=available_types,
                default=available_types,
                format_func=lambda x: x.capitalize(),
                label_visibility="hidden"
            )

        if selected_types:
            current_agents = step_data[step_data['AgentType'].isin(selected_types)]
        else:
            current_agents = step_data.iloc[0:0]

        st.subheader(f"Population Status")

        cols_per_row = 5
        for i in range(0, len(current_agents), cols_per_row):
            row_agents = current_agents.iloc[i:i + cols_per_row]
            grid_cols = st.columns(cols_per_row)

            for idx, (index, agent) in enumerate(row_agents.iterrows()):
                with grid_cols[idx]:
                    agent_card(agent)

    with right_col:
        spc = st.columns([1, 8, 1])

        with spc[1]:
            city_rows = model_data[model_data['Step'] == st.session_state.step].reset_index(drop=True)

            prev_step = st.session_state.step - 1
            prev_city_rows = model_data[model_data['Step'] == prev_step].reset_index(drop=True)

            if not city_rows.empty:
                current_city = city_rows.iloc[0]

                def parse_counts(row):
                    if 'LivingAgents' in row and isinstance(row['LivingAgents'], str):
                        try:
                            return ast.literal_eval(row['LivingAgents'])
                        except:
                            return {}
                    return {}

                current_counts = parse_counts(current_city)
                prev_counts = parse_counts(prev_city_rows.iloc[0]) if not prev_city_rows.empty else {}

                def get_delta(column_name):
                    if not prev_counts:
                        return None
                    curr_val = current_counts.get(agent_type.lower(), 0)
                    prev_val = prev_counts.get(agent_type.lower(), 0)
                    return int(curr_val - prev_val)

                st.subheader("Demographic")

                st.metric(
                    "Total Agents",
                    int(current_city['TotalAgents']),
                    delta=int(current_city['TotalAgents'] - prev_city_rows.iloc[0]['TotalAgents']) if not prev_city_rows.empty else None
                )

                if selected_types:
                    agent_type_cols = st.columns(3)

                    for i, agent_type in enumerate(selected_types):
                        type_key = agent_type.lower()

                        with agent_type_cols[i % 3]:
                            st.metric(
                                label=agent_type.capitalize(),
                                value=int(current_counts.get(type_key, 0)),
                                delta=get_delta(type_key)
                            )
