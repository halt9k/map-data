import pycountry
import pandas as pd
import numpy as np
import geopandas
import difflib
from data_preprocess_name_matching import get_match

def clean(cl):
    # NOT 'Oblast':'' due to moscow vs moscow oblast
    return cl.replace({'region':'r', 
                       'area':'a', 
                       'Oblast':'o',
                       'Republic':'r', 
                       'of':'', 
                       '  ':' ', 
                       'Krai':'k', 
                       'territory':'t'}, 
                      regex=True).str.strip()

def get_population_change_ru_2002_to_2022():
    df = pd.read_csv("Data\\Ru\\ru_2002_2022.csv")
    # print(df)

    # original region names messed, rename goals from this file
    correct_names = pd.read_csv("Data\\Ru\\ru_2022_correct_names.csv", encoding='utf-8')    

    df.Region = clean(df.Region)
    correct_names['cleaned_iso_names'] = clean(correct_names.iso_name)
    df['iso_name'] = df.Region.apply(lambda x: get_match(x, correct_names.cleaned_iso_names, correct_names.iso_name))

    print('Replaced: \n' + str(df.Region + ' -> ' + df.iso_name))

    df['Growth'] = df.p_2022.div(df.p_2002).mul(100)
    return df


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

def get_l_religions():
    df = pd.read_csv("Data\\l-religions.csv")
    df['Code'] = alpha3code(df.country)    

    return df
