import streamlit as st
from plots.visualizations import visualizations

my_plots = visualizations()

# Title
st.title("Tương quan giữa tiền lương và khu vực")

my_plots.plot_mean_salary_by_province()