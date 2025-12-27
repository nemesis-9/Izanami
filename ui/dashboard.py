import pandas as pd
import streamlit as st

from tabs.sidebar import sidebar
from tabs.overview import overview
from tabs.agents import agents

st.set_page_config(layout="wide", page_title="Izanami Dashboard")

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
        font-size: 0.5rem;
        padding: 2px 4px;
        border-radius: 3px;
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

    max_steps = int(model_data['Step'].max())
    with st.sidebar:
        sidebar(max_steps)

    tabs = st.tabs(["Overview", "Economy", "Agents"])

    with tabs[0]:
        overview(agent_data, model_data, st.session_state.step)
    with tabs[2]:
        agents(agent_data, model_data)


except Exception as e:
    st.error(f"Error loading data: {e}")
