from plots.plot_functions import plot_functions
from dfs.dfs_provider import dfs_provider
from utils.colors import colors
from utils.save_tools import save_html
import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

pf = plot_functions()
dfs = dfs_provider()
colors = colors()


all_levels_label = 'Tất cả cấp bậc'
all_industries_label = 'Tất cả ngành nghề'
class visualizations:
    def plot_industry_counts(self):
        industry_count_c = st.container()
        df = dfs.get_industry_counts()
        plot = pf.bar_plot(df=df, title='Phân bố ngành nghề', 
                               x='count', y='industry', orientation='h', color='count',
                               color_continuous_scale=colors.getSequentialPeach(), 
                               height=1200, ytitle='Ngành nghề', xtitle='Số lượng công việc')
        industry_count_c.plotly_chart(plot)
    
    def plot_mean_salary_industry_by_level(self):
        levels_arr = [all_levels_label] + list(dfs.get_job_levels())
        industries_arr = [all_industries_label] + list(dfs.get_industries())
        mean_slr_by_level_c = st.container()
        levels_col, industries_col = mean_slr_by_level_c.columns(2)
        level = levels_col.selectbox('Choose a job level',
                                    levels_arr)
        industry = industries_col.selectbox('Choose an industry',
                                    industries_arr)
        min_max = mean_slr_by_level_c.radio(label='Salary range', options=['Min','Max'])
        
        if (level == all_levels_label):
           if (industry == all_industries_label):
              df = dfs.get_mean_salaries()
           else:
              df = dfs.search_mean_salaries_by_industry(industry=industry)
        else:
           if (industry == all_industries_label):
              df = dfs.search_mean_salaries_by_level(level)
           else:
              df = dfs.search_mean_salaries_by_industry_level(industry=industry,
                                                              level=level)
        if min_max == 'Min':
          range_col = 'min_salary_rd'
          range_txt = 'tối thiểu'
        else:
          range_col = 'max_salary_rd'
          range_txt = 'tối đa'    
        plot = pf.bar_plot(df=df, x='mapped_industry_ls', y=range_col, barmode='group', orientation='v',
                                height=600, color_continuous_scale=colors.getSequentialPeach(), color='max_salary_rd', 
                                title=f'Lương {range_txt} trung bình Cấp bậc: {level} / Ngành nghề: {industry}',
                                xtitle='Ngành nghề', ytitle='Mức lương trung bình (Triệu VNĐ)')
        mean_slr_by_level_c.plotly_chart(plot)
        return mean_slr_by_level_c
    
    def plot_mean_salary_industry_by_yoe(self):
      industries_arr = list(dfs.get_industries())
      mean_slr_by_yoe_c = st.container()
      industries_col, min_max_col = mean_slr_by_yoe_c.columns(2)
      industry = industries_col.selectbox('Choose an industry',
                                 industries_arr)
      min_max = min_max_col.radio(label='Salary range', options=['Min','Max'])
      if min_max == 'Min':
          range_col = 'min_salary_rd'
          range_txt = 'tối thiểu'
      else:
         range_col = 'max_salary_rd'
         range_txt = 'tối đa'
      df = dfs.get_mean_salaries_by_industry_group_by_yoe(industry=industry)
      plot = pf.bar_plot(df=df, x='min_year', y=range_col, orientation='v',
                                height=600, color_continuous_scale=colors.getSequentialPeach(), color='max_salary_rd', 
                                title=f'Lương {range_txt} trung bình theo số năm kinh nghiệp Ngành nghề: {industry}',
                                xtitle='Ngành nghề', ytitle='Mức lương trung bình (Triệu VNĐ)')
      mean_slr_by_yoe_c.plotly_chart(plot)
      return mean_slr_by_yoe_c
    
    def plot_mean_min_years_by_level(self):
      mean_min_years_level_c = st.container()
      industries_arr = list(dfs.get_industries())
      industry = mean_min_years_level_c.selectbox('Choose an industry',
                              industries_arr)
      df = dfs.get_mean_min_years_for_each_level(industry=industry)
      mean_min_years_level_c.dataframe(df)
      return mean_min_years_level_c
   
    def plot_mean_salary_by_provinces(self):
      vietnam_geo = json.load(open("data/vietnam_state.geojson","r"))
      data = dfs.get_mean_salary_by_provinces()

      categories = sorted(data.columns[2:])
      cat_options = []
      for cat in categories:
         cat_options.append(cat)
      mean_salary_provinces = st.container()
      industry = mean_salary_provinces.selectbox('Choose an industry',cat_options)
      fig = px.choropleth_mapbox(data, geojson = vietnam_geo, locations = data.Code, color = data[industry],
                           featureidkey = 'properties.Code',
                           color_continuous_scale = "peach",
                           mapbox_style = "carto-positron",
                           zoom = 5, center = {"lat": 16, "lon": 106},
                           opacity = 0.5,        
                           hover_name = 'Provinces',
                           labels= {industry: 'Mean salary ','Code': 'Province code '}            
                          )
      fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0}, width = 800, height = 800)
      mean_salary_provinces.plotly_chart(fig)
      
      return mean_salary_provinces
