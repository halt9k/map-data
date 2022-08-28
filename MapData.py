import pycountry
import pandas as pd
import numpy as np
import geopandas
import matplotlib
from matplotlib import pyplot as plt
from TransformCsvData import *
from PlotData import *

df_pc = get_population_change_2000_to_2020()
df_le = get_life_expectancy_2019()
#TODO 1 add info for LE year

df = pd.merge(df_pc, df_le, on='Code')
df_desc = "2000 -> 2020 Growth%, all countries"

df_sample = df[ (df._2020 > 20 * 10**6) & (df.Expectancy > 70)]
df_sample_desc = "2000 -> 2020 Growth%, P > 20M, LE > 70y"

bins = np.arange(50, 200+1, 5)
plot_growth_hist_split_life_expectancy(df, bins, df_desc, 0, stop = False)

bins = np.arange(50, 200+1, 5)
plot_growth_hist_split_life_expectancy(df_sample, bins, df_sample_desc, 1, stop = False)

# = 90% ... 140%

plot_map(df, names = False, stop = False, caption = df_desc)
plot_map(df_sample,  names = True, stop = True, caption = df_sample_desc)