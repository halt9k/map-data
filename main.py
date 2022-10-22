from Data.df_preprocess_world import *
from Data.df_preprocess_ru import get_df_population_change_ru
from Data.df_process import merge_geo_tables, filter_geo_table
from consts import *
from plot_hist import plot_growth_hist
from plot_map import plot_map

from translations import fill_translations
import i18n

fill_translations()
i18n.set('locale', 'en')

df_pc, info_pc = get_df_population_change(C_FROM_Y, C_TO_Y)
df_pc_info = info_pc.format(where=t('ALL_COUNTRIES'))

df_pc_ru, info_pc_ru = get_df_population_change_ru(C_FROM_Y, C_TO_Y)
df_pc_info += info_pc_ru

df_merged, info_merged = merge_geo_tables(df_pc)
df_filtered, info_filtered = filter_geo_table(df_merged)

df_filtered_info = info_pc.format(where=t('ONLY'))
df_filtered_info += t('POPULATION') + ", 2020; "
df_filtered_info += info_merged
df_filtered_info += info_filtered

bins = np.arange(50, 200 + 1, 5)
e1, e2 = CT_LE_DELEVOPED, CT_LE_MODERN

plot_growth_hist(df_merged, bins, df_pc_info, stop=False, th1=e1, th2=e2)

bins = np.arange(50, 200 + 1, 5)
e1, e2 = CT_LE_DELEVOPED, CT_LE_MODERN
plot_growth_hist(df_filtered, bins, df_filtered_info, stop=False, th1=e1, th2=e2)

plot_map(df_merged, df_pc_ru, col_range=(80, 150), show_info=False, title=df_pc_info, asp=True, wait=False)
plot_map(df_filtered, df_pc_ru, col_range=(80, 130), show_info=True, title=df_filtered_info, asp=False,
         wait=True)
