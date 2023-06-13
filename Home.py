import streamlit as st
import streamlit.components.v1 as components
from plots.visualizations import visualizations

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to DS103 Capstone Project 👋")

st.markdown(
    """
    DS103 Course from the University of Information Technology (UIT)
    focuses on fundamental concepts of data collection, data cleaning, 
    and data evaluation.

    **👈 Select a page from the sidebar** to view key visualizations
    that are based on Vietnam's job markets data.
    ### Professors & Authors
    - Instructor: Mr. Tran Quoc Khanh
    - Author 1: Mr. Tai Le (20522216)
    - Author 2: Mr. Cuong Le (20520146)
    ### Visit our university website
    - Visit [UIT's Homepage](https://www.uit.edu.vn/)
"""
)
# My classes

# bootstrap 4 collapse example
