import pycountry
import pandas as pd
import numpy as np
import geopandas
import matplotlib
from matplotlib import pyplot as plt
from data_preprocess import *
from plot_hist import plot_growth_hist
from plot_map import plot_map
import translations

# years of interest (= last 20)
# hardcoded: 2000 to 2020
desc_growth = translations.GROWTH + ", 2000 -> 2020\n"

# country filer: total_population
# at the last year of interest
th_total_ppl_M = 5

# country filer: amount of nobel prize winners (= modern country)
# hardcoded: nb_year = 2022
th_nobels = 2

# country filer: life expectancy
le_year = 2019
th_expect_developed = 65.0
th_expect_modern = 76.0

df_ru_pc = get_population_change_ru_2000_to_2020()

df_pc = get_population_change_2000_to_2020()
df_le = get_life_expectancy(le_year)
df_nb = get_nobel_winners_amount_2022()

# adding info to population table
df_desc = desc_growth + ", " + translations.ALL_COUNTRIES
df = pd.merge(df_pc, df_le, on='Code', how='left', validate='1:1')
df = pd.merge(df, df_nb, on='Code', how='left', validate='1:1')

df_sample = df.copy()
df_sample.Growth[df_sample._2020 <= th_total_ppl_M * 10**6] = np.nan
df_sample.Growth[(df_sample.Expectancy <= th_expect_developed) | df_sample.Expectancy.isnull()] = np.nan
df_sample.Growth[(df_sample.Nobels <= th_nobels) | df_sample.Nobels.isnull()] = np.nan

df_sample_desc = desc_growth + translations.ONLY
df_sample_desc += " P > {}M, LE > {}y, NB > {}\n".format(th_total_ppl_M, th_expect_developed, th_nobels)
df_sample_desc += translations.POPULATION + ", 2020; "
df_sample_desc += translations.EXPECTANCY  + ", {}; ".format(le_year)
df_sample_desc += translations.NOBELS + ", 2022;"

bins = np.arange(50, 200 + 1, 5)
e1, e2 = th_expect_developed, th_expect_modern
# plot_growth_hist(df, bins, df_desc, stop=False, th1=e1, th2=e2)

bins = np.arange(50, 200 + 1, 5)
e1, e2 = th_expect_developed, th_expect_modern
# plot_growth_hist(df_sample, bins, df_sample_desc, stop=False, th1=e1, th2=e2)

# = 90% ...  140%
# plot_map(df, col_min=80, col_max=150, show_info = False, caption_text=df_desc, wait=False)
# plot_map(df_sample, col_min=90, col_max=125, show_info = True, caption_text=df_sample_desc, wait=True)

plot_ru_map(df_ru_pc, col_min=90, col_max=125, caption_text="RU", wait=True)