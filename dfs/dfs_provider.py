import pandas as pd
import numpy as np
import os

data = pd.read_csv("./data/txl_data.csv")

class dfs_provider:
    def get_job_levels(self):
        return data['level'].unique()
    
    def get_industry_counts(self):
        industry_counts = pd.DataFrame(data['mapped_industry'].str.split(', ')
                                       .explode().value_counts()).reset_index()
        industry_counts.columns = ['industry', 'count']
        return industry_counts
    
    def search_mean_salaries_by_level(self, level):
        temp_data = data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()
        mean_slr_by_level = temp_data.groupby(['mapped_industry_ls', 'level']).mean()[['min_salary', 'max_salary']].reset_index()
        mean_slr_by_level['min_salary_rd'] = mean_slr_by_level['min_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        mean_slr_by_level['max_salary_rd'] = mean_slr_by_level['max_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        return mean_slr_by_level[mean_slr_by_level['level'] == level].reset_index(drop=True)
    
    def get_mean_salaries(self):
        temp_data = data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()
        mean_salaries = temp_data.groupby('mapped_industry_ls').mean()[['min_salary', 'max_salary']].reset_index()
        mean_salaries['min_salary_rd'] = mean_salaries['min_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        mean_salaries['max_salary_rd'] = mean_salaries['max_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        return mean_salaries
    
    def search_mean_salaries_by_industry(self, industry):
        full_df = self.get_mean_salaries()
        return full_df[full_df['mapped_industry_ls'] == industry]
    
    def search_mean_salaries_by_industry_level(self, industry, level):
        full_df = self.search_mean_salaries_by_level(level)
        return full_df[full_df['mapped_industry_ls'] == industry]
    
    def get_industries(self):
        temp_data = data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()
        return temp_data['mapped_industry_ls'].unique()