import pycountry
import pandas as pd
import numpy as np
import geopandas
import matplotlib
from matplotlib import pyplot as plt
from TransformCsvData import *
from PlotData import *

# thresholds: life expectancy, total_population
th_expect_developed = 72.0
th_expect_modern = 76.0
th_total_ppl_M = 5


df_pc = get_population_change_2000_to_2020()
df_le = get_life_expectancy_2019()
#TODO 1 add info for LE year
df = pd.merge(df_pc, df_le, on='Code')
df_desc = "2000 -> 2020 Growth%, all countries"

df_sample = df[(df._2020 > th_total_ppl_M * 10**6) & (df.Expectancy > th_expect_developed)]
df_sample_desc = "2000 -> 2020 Growth%, P > {}M, LE > {}y".format(th_total_ppl_M, th_expect_developed)

bins = np.arange(50, 200 + 1, 5)
e1, e2 = th_expect_developed, th_expect_modern
plot_growth_hist_split_life_expectancy(df, bins, df_desc, stop=False, figN=0, s1=e1, s2=e2)

bins = np.arange(50, 200 + 1, 5)
e1, e2 = th_expect_developed, th_expect_modern
plot_growth_hist_split_life_expectancy(df_sample, bins, df_sample_desc, stop=False, figN=1, s1=e1, s2=e2)

# = 90% ...  140%
plot_map(df, names = False, caption=df_desc, stop=False, figN=2)
plot_map(df_sample,  names = True, caption=df_sample_desc, stop=True, figN=3)