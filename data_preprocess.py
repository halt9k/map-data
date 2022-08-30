import pycountry
import pandas as pd
import numpy as np
import geopandas

# Remove combined world regions (Whole world, Africa, etc)
def filter_code(df):
    df_filtered = df[~df.Code.isnull() & (df.Code != 'OWID_WRL')]
    return df_filtered

def get_population_change_2000_to_2020():
    df = pd.read_csv("Data\\population-since-1800.csv",dtype={'Code': np.str})
    # print(df)
    df.rename(columns = {'Population (historical estimates)':'Population'}, inplace = True)

    df = df[df.Year.isin([2000, 2020])]
    df = filter_code(df)

    df = pd.pivot_table(df, values='Population', index=['Entity', 'Code'], columns='Year')
    df.reset_index(inplace=True)
    df.rename(columns = {2000:'_2000',2020:'_2020'}, inplace = True)
    df['Growth'] = df._2020.div(df._2000).mul(100)

    return df

def get_life_expectancy(at_year):
    df = pd.read_csv("Data\\life-expectancy.csv",dtype={'Code': np.str})
    # print(df)
    df.rename(columns = {'Life expectancy':'Expectancy'}, inplace = True)

    df = df[df.Year == at_year]    
    df = filter_code(df)

    return df

# Country names from codes
def alpha3code(column):
    Codes = []
    for country_name in column:
        # .alpha_3 means 3-letter country code
        # .alpha_2 means 2-letter country code
        country = pycountry.countries.get(name=country_name)

        if country is None:
            try:
                match_list = pycountry.countries.search_fuzzy(country_name)
                if len(match_list) > 0:
                    country = match_list[0]
            except:
                country = None

        if country is None:
            Codes.append('UNK')
        else:
            Codes.append(country.alpha_3)

    return Codes

def get_nobel_winners_amount_2022():
    df = pd.read_csv("Data\\nobel-prizes.csv")
    df['Code'] = alpha3code(df.country)
    df.rename(columns = {'count':'Nobels'}, inplace = True)

    return df
