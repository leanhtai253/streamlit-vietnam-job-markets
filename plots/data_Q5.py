import pandas as pd
import numpy as np

#df là file csv dữ liệu đã tiền xử lý-dữ liệu chính
#df_code là csv chứa mã code của các tỉnh
def get_data_Q5(df,df_code):
    map = pd.DataFrame()
    map['industry_list'] = [x.split(', ') for x in df['mapped_industry']]
    map['average'] = [(x+y)/2 for x, y in zip(df['min_salary'],df['max_salary'])]
    map['city'] = [x.split(', ') for x in df['city']]
    map = map.explode('industry_list').explode('city').groupby(['industry_list','city']).mean().reset_index()
    map['average'] = [round(x,-5) for x in map['average']]

    lst = list(set(map['industry_list']))
    output = df_code.copy()
    for x in lst:
        filter = map.loc[map['industry_list'] == x]
        filter.drop(columns = ['industry_list'], inplace=True)
        filter.columns = ['Provinces', x]
        
        output = output.merge(filter, on='Provinces', how='outer', suffixes=None, indicator=True)\
            .query('_merge!="right_only"').drop(columns=['_merge'])
    output = output.fillna(-1)

    return output

