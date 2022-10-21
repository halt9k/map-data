from i18n import t

from data_preprocess import *
from plot_hist import plot_growth_hist
from plot_map import plot_map

from translations import fill_translations
import i18n

fill_translations()
i18n.set('locale', 'en')

# diff years
C_FROM_Y = 2000
C_TO_Y = 2020

# country threshold: total_population
CT_POPULATION_M = 5
# CT_POPULATION_AT_Y = last year

# country threshold:  amount of nobel prize winners (= modern country)
CT_NOBELS = 2
CT_NOBELS_AT_Y = 2022

# country threshold: life expectancy
CT_LE_DELEVOPED = 65.0
CT_LE_MODERN = 76.0
CT_LE_AT_Y = 2019

df_pc_ru, info_pc_ru = get_df_population_change_ru_2002_to_2022(C_FROM_Y, C_TO_Y)

df_pc, info_pc = get_df_population_change(C_FROM_Y, C_TO_Y)
df_le, info_le = get_df_life_expectancy(CT_LE_AT_Y)
df_nb, info_nb = get_df_nobels_amount(CT_NOBELS_AT_Y)
df_l = get_df_l_religions()

# adding info to population table
df_desc = info_pc + t('ALL_COUNTRIES')
df = pd.merge(df_pc, df_le, on='Code', how='left', validate='1:1')
df = pd.merge(df, df_nb, on='Code', how='left', validate='1:1')
df = pd.merge(df, df_l, on='Code', how='left', validate='1:1')

df_sample = df.copy()

df_sample.Growth[df_sample._2020 <= CT_POPULATION_M * 10 ** 6] = np.nan


df_sample.Growth[(df_sample.Expectancy <= CT_LE_DELEVOPED) | df_sample.Expectancy.isnull()] = np.nan
df_sample.Growth[(df_sample.Nobels <= CT_NOBELS) | df_sample.Nobels.isnull()] = np.nan

df_sample_desc = info_pc + t('ONLY')
df_sample_desc += " P > {}M, LE > {}y, NB > {}\n".format(CT_POPULATION_M, CT_LE_DELEVOPED, CT_NOBELS)
df_sample_desc += t('POPULATION') + ", 2020; "
df_sample_desc += info_le
df_sample_desc += info_nb
df_sample_desc += info_pc_ru

bins = np.arange(50, 200 + 1, 5)
e1, e2 = CT_LE_DELEVOPED, CT_LE_MODERN
plot_growth_hist(df, bins, df_desc, stop=False, th1=e1, th2=e2)

bins = np.arange(50, 200 + 1, 5)
e1, e2 = CT_LE_DELEVOPED, CT_LE_MODERN
plot_growth_hist(df_sample, bins, df_sample_desc, stop=False, th1=e1, th2=e2)

plot_map(df, df_pc_ru, col_range=(80, 150), show_info=False, title=df_desc, asp=True, wait=False)
plot_map(df_sample, df_pc_ru, col_range=(80, 130), show_info=True, title=df_sample_desc, asp=False,
         wait=True)
