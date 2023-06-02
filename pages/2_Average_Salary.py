import streamlit as st
from plots.visualizations import visualizations

my_plots = visualizations()

# Title
st.title("Mức lương trung bình theo ngành nghề và cấp bậc")
# Average salaries of each industry based on job level
my_plots.plot_mean_salary_industry_by_level()