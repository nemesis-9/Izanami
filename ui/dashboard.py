import sys
import pandas as pd
import streamlit as st
from pathlib import Path

from ui.tabs.overview import overview_tab
from ui.tabs.agents import agent_tab
from ui.tabs.memorial import memorial_tab

from ui.components.sidebar import sidebar

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def local_css(file_name):
    css_path = Path(__file__).parent / "styles" / file_name
    with open(css_path, "r", encoding="utf-8") as f:
        return f.read()


st.set_page_config(layout="wide", page_title="Izanami Dashboard")

st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.1/flowbite.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.1/flowbite.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    </style>
""", unsafe_allow_html=True)

st.markdown(
    f"""<style>
        {local_css("main.css")}
        {local_css("agent_card.css")}
    </style>""",
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    agent_df = pd.read_csv('data/output/phase8/agent_data.csv')
    model_df = pd.read_csv('data/output/phase8/model_data.csv')
    memorial_df = pd.read_csv('data/output/phase8/memorial_log.csv')
    return agent_df, model_df, memorial_df


try:
    agent_data, model_data, memorial_data = load_data()

    max_steps = int(model_data['Step'].max())
    with st.sidebar:
        sidebar(max_steps)

    tabs = st.tabs(["Overview", "Economy", "Agents", "Memorial"])

    # with tabs[0]:
    #     overview_tab(agent_data, model_data, st.session_state.step)
    with tabs[2]:
        agent_tab(agent_data, model_data)
    with tabs[3]:
        memorial_tab(memorial_data)


except Exception as e:
    st.error(f"Error loading data: {e}")
