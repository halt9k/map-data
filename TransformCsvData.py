import pycountry
import pandas as pd
import numpy as np
import geopandas

# Without world regions (Whole world, Africa, etc)
def filter_code(df):
    df_filtered = df[~df.Code.isnull() & (df.Code != 'OWID_WRL')]
    return df_filtered

def get_population_change_2000_to_2020():
    df = pd.read_csv("Data\population-since-1800.csv",dtype={'Code': np.str})
    # print(df)
    df.rename(columns = {'Population (historical estimates)':'Population'}, inplace = True)

    df = df[df.Year.isin([2000, 2020])]
    df = filter_code(df)

    df = pd.pivot_table(df, values='Population', index=['Entity', 'Code'], columns='Year')
    df.reset_index(inplace=True)
    df.rename(columns = {2000:'_2000',2020:'_2020'}, inplace = True)
    df['Growth'] = df._2020.div(df._2000).mul(100)

    return df

def get_life_expectancy_2019():
    df = pd.read_csv("Data\life-expectancy.csv",dtype={'Code': np.str})
    # print(df)
    df.rename(columns = {'Life expectancy':'Expectancy'}, inplace = True)

    df = df[df.Year == 2019]    
    df = filter_code(df)

    return df

# country column to code column
#def alpha3code(column):
#    CODE = []
#    for country in column:
#        try:
#            code = pycountry.countries.get(name=country).alpha_3
#           # .alpha_3 means 3-letter country code
#           # .alpha_2 means 2-letter country code
#            CODE.append(code)
#        except:
#            CODE.append('None')
#    return CODE

#df['CODE'] = alpha3code(df.Entity)