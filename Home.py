import streamlit as st
from plots.visualizations import visualizations

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to DS103 Capstone Project 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    DS103 Course from the University of Information Technology (UIT)
    focuses on fundamental concepts of data collection, data cleaning, 
    and data evaluation.

    **👈 Select a page from the sidebar** to view key visualizations
    that are based on Vietnam's job markets data.
    ### Professors & Authors
    - Instructor: Mr. Tran Quoc Khanh
    - Author 1: Mr. Tai Le
    - Author 2: Mr. Cuong Le
    ### Visit our university website
    - Visit [UIT's Homepage](https://www.uit.edu.vn/)
"""
)
# My classes


