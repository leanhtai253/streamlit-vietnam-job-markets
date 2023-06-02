from plots.plot_functions import plot_functions
from dfs.dfs_provider import dfs_provider
from utils.colors import colors
from utils.save_tools import save_html
import streamlit as st

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
        save_html(plot, "phan_bo_nganh_nghe.html")
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
        save_html(plot, 'luong_tb_theo_cap_bac.html')
        return mean_slr_by_level_c