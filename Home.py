import streamlit as st
import streamlit.components.v1 as components
from plots.visualizations import visualizations
import base64

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

@st.cache_data()
def set_background(file):
    with open(file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('images/background.jpg')


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
