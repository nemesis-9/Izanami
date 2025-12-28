import streamlit as st

from ui.components.memorialCard import memorial_card


def generate_agent_cards(death_records):
    cols = st.columns(3)
    for idx, (_, agent) in enumerate(death_records.iterrows()):
        with cols[idx % 3]:
            memorial_card(agent)


def memorial_tab(memorial_data):

    header_cols = st.columns([9, 2])

    with header_cols[0]:
        st.markdown("""
        <div class="flex flex-col border-l-4 border-purple-600 pl-6 py-2">
            <h1 class="text-6xl font-black text-white tracking-tighter flex items-center gap-4">
                <span class="shining-title" style="font-size: 4rem; font-weight: 900; letter-spacing: -2px; font-style: italic;">
                    IZANAMI
                </span>
                <span class="bg-purple-600 text-xs font-mono tracking-normal px-2 py-1 rounded italic text-purple-100">
                    DEATH LOG
                </span>
            </h1>
            <p class="text-purple-400/60 font-mono text-sm mt-1 uppercase tracking-widest">
                Biological Archive & Resource Reclamation Center
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

        available_types = sorted(memorial_data['AgentType'].unique().tolist())
        selected_types = st.multiselect(
            "Filter Simulation Layers",
            options=available_types,
            default=available_types,
            label_visibility="hidden"
        )

        current_deaths = memorial_data[
            (memorial_data['Step'] == st.session_state.step) &
            (memorial_data['AgentType'].isin(selected_types))
            ]

        recent_archive = memorial_data[
            (memorial_data['Step'] < st.session_state.step) &
            (memorial_data['AgentType'].isin(selected_types))
            ].sort_values(by=['Step', 'AgentID'], ascending=False).head(9)  # Recent 9 Deaths

        st.subheader("Current Memorials")
        if current_deaths.empty:
            st.info("No agents passed away during current step.")
        else:
            generate_agent_cards(current_deaths)

        st.subheader("Recent Memorials")
        if recent_archive.empty:
            st.info("No previous deaths recorded.")
        else:
            generate_agent_cards(recent_archive)

    with right_col:

        space_cols = st.columns([1, 8, 1])

        with space_cols[1]:
            st.subheader("Death Analytics")
            historical_deaths = memorial_data[memorial_data['Step'] <= st.session_state.step]

            if not historical_deaths.empty:
                st.metric("Total Deceased", len(historical_deaths))
                st.metric("Avg Life Expectancy", f"{historical_deaths['DyingAge'].mean():.1f} Steps")
                st.metric("Total Legacy Wealth", f"${historical_deaths['DyingWealth'].sum():.2f}")

                st.write("---")

                st.write("**Mortality by Type**")
                st.write("")
                type_counts = historical_deaths['AgentType'].value_counts()
                type_cols = st.columns(3)

                for i, (agent_type, count) in enumerate(type_counts.items()):
                    with type_cols[i % 2]:
                        st.metric(label=agent_type.capitalize(), value=int(count))
