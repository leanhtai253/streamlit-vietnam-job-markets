import pandas as pd
import numpy as np
import os
import json 

def map_yoe_range(x):
        if x < 1:
            return "0 - 1 year"
        elif x < 3:
            return "1 - 3 years"
        elif x < 5:
            return "3 - 5 years"
        elif x < 10:
            return "5 - 10 years"
        return "10+ years"

class dfs_provider:
    data = pd.read_csv("./data/txl_data.csv")
    city_code = pd.read_csv('./data/provinces.csv')
    vietnam_geo = json.load(open("./data/vietnam_state.geojson","r"))
    def get_job_levels(self):
        return self.data['level'].unique()
    
    def get_industry_counts(self):
        industry_counts = pd.DataFrame(self.data['mapped_industry'].str.split(', ')
                                       .explode().value_counts()).reset_index()
        industry_counts.columns = ['industry', 'count']
        return industry_counts
    
    def search_mean_salaries_by_level(self, level):
        temp_data = self.data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()[['mapped_industry_ls', 'level', 'min_salary', 'max_salary']]
        mean_slr_by_level = temp_data.groupby(['mapped_industry_ls', 'level']).mean()[['min_salary', 'max_salary']].reset_index()
        mean_slr_by_level['min_salary_rd'] = mean_slr_by_level['min_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        mean_slr_by_level['max_salary_rd'] = mean_slr_by_level['max_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        return mean_slr_by_level[mean_slr_by_level['level'] == level].reset_index(drop=True)
    
    def get_mean_salaries(self):
        temp_data = self.data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()[['mapped_industry_ls', 'min_salary', 'max_salary']]
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
        temp_data = self.data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()
        return temp_data['mapped_industry_ls'].unique()
    
    def get_mean_salaries_by_industry_group_by_yoe(self, industry):
        temp_data = self.data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()[['mapped_industry_ls', 'min_year', 'min_salary', 'max_salary']]
        mean_slr_yoe = temp_data.groupby(['mapped_industry_ls','min_year']).mean()[['min_salary', 'max_salary']]
        mean_slr_yoe['min_salary_rd'] = mean_slr_yoe['min_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        mean_slr_yoe['max_salary_rd'] = mean_slr_yoe['max_salary'].apply(lambda x: np.round(x / 1000000, decimals=2))
        mean_slr_yoe_of_ind = mean_slr_yoe.loc[industry].reset_index()
        mean_slr_yoe_of_ind.min_year = mean_slr_yoe_of_ind.min_year.apply(map_yoe_range)
        df = mean_slr_yoe_of_ind.groupby('min_year').mean()[['min_salary_rd', 'max_salary_rd']].reset_index()
        return df
    
    def get_mean_min_years_for_each_level(self, industry):
        temp_data = self.data.copy()
        temp_data['mapped_industry_ls'] = temp_data['mapped_industry'].str.split(', ')
        temp_data = temp_data.explode('mapped_industry_ls').copy()[['mapped_industry_ls', 'level', 'min_year']]
        mean_min_year_by_level = temp_data[temp_data['mapped_industry_ls'] == industry].drop('mapped_industry_ls', axis=1)
        mean_min_year_by_level = mean_min_year_by_level.groupby('level').mean()[['min_year']].reset_index()
        mean_min_year_by_level = mean_min_year_by_level[mean_min_year_by_level['level'].apply(lambda x: 'Quản lý' in x)].copy()
        mean_min_year_by_level['min_year_rd'] = mean_min_year_by_level.min_year.apply(lambda x: np.round(x, 2))
        return mean_min_year_by_level.sort_values('min_year_rd').reset_index(drop=True)
    
    def get_mean_salary_by_province(self):
        map = pd.DataFrame()
        map['industry_list'] = [x.split(', ') for x in self.data['mapped_industry']]
        map['average'] = [(x+y)/2 for x, y in zip(self.data['min_salary'],self.data['max_salary'])]
        map['city'] = [x.split(', ') for x in self.data['city']]
        map = map.explode('industry_list').explode('city').groupby(['industry_list','city']).mean().reset_index()
        map['average'] = [round(x,-5) for x in map['average']]

        lst = list(set(map['industry_list']))
        output = self.city_code.copy()
        for x in lst:
            filter = map.loc[map['industry_list'] == x]
            filter.drop(columns = ['industry_list'], inplace=True)
            filter.columns = ['Provinces', x]
            
            output = output.merge(filter, on='Provinces', how='outer', indicator=True)\
                .query('_merge!="right_only"').drop(columns=['_merge'])
        output = output.fillna(-1)

        return output