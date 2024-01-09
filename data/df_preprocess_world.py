import pandas as pd
import numpy as np
from i18n import t


from data.geo_helpers import code_to_alpha_3_iso, filter_irregular_codes


def get_df_population_change(year_from, year_to):
    df = pd.read_csv("data\\world\\population-since-1800.csv", dtype={'Code': str})
    # print(df)
    df.rename(columns={'Population (historical estimates)': 'Population'}, inplace=True)

    df = df[df.Year.isin([year_from, year_to])]
    df = filter_irregular_codes(df)

    df = pd.pivot_table(df, values='Population', index=['Entity', 'Code'], columns='Year')
    df.reset_index(inplace=True)
    df.rename(columns={2000: 'at_2000', 2020: 'at_2020'}, inplace=True)
    df['Growth'] = df.at_2020.div(df.at_2000).mul(100)

    desc = t('GROWTH')
    assert (str(year_from) in desc)
    assert (str(year_to) in desc)

    return df, desc


def get_df_life_expectancy(year_at):
    df = pd.read_csv("data\\world\\life-expectancy.csv", dtype={'Code': str})
    # print(df)
    df.rename(columns={'Life expectancy': 'Expectancy'}, inplace=True)

    df = df[df.Year == year_at]
    df = filter_irregular_codes(df)

    return df


def get_df_nobels_amount(year_at):
    df = pd.read_csv("data\\world\\nobel-prizes.csv")
    df['Code'] = code_to_alpha_3_iso(df.country)
    df.rename(columns={'count': 'Nobels'}, inplace=True)

    assert(str(year_at) in str(df.columns))

    return df


def get_df_l_religions():
    df = pd.read_csv("data\\world\\l-religions.csv")
    df['Code'] = code_to_alpha_3_iso(df.country)

    return df
