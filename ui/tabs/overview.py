import streamlit as st

def overview_tab(agent_data, model_data):
    st.header('agent_data')
    st.write(agent_data)
    st.write('---')
    st.header('model_data')
    st.write(model_data)
