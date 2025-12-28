import streamlit as st


def sidebar(max_steps):
    if 'step' not in st.session_state:
        st.session_state.step = 1

    st.slider('Timeline', 1, max_steps, key='step')

