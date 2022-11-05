from data.df_preprocess_world import get_df_population_change
from data.df_preprocess_ru import get_df_population_change_ru
from data.df_process import merge_geo_tables, filter_geo_table
from consts import *
from plot_hist import plot_growth_hist
from plot_map import plot_map

from translations import fill_translations, loc_set, t

fill_translations()
loc_set('locale', 'en')

df_pc, info_pc = get_df_population_change(C_FROM_Y, C_TO_Y)
df_pc_summary = info_pc.format(where=t('ALL_COUNTRIES'))

df_pc_ru, info_pc_ru = get_df_population_change_ru(C_FROM_Y, C_TO_Y)

df_merged = merge_geo_tables(df_pc)
df_filtered, info_filtered = filter_geo_table(df_merged)

df_filtered_summary = info_pc.format(where=t('ONLY'))
df_filtered_summary += info_filtered
df_filtered_summary += info_pc_ru

plot_growth_hist(df_merged, df_pc_summary, C_HIST_BINS, C_HIST_THRESHOLDS)
plot_growth_hist(df_filtered, df_filtered_summary, C_HIST_BINS, C_HIST_THRESHOLDS)

plot_map(df_merged, df_pc_ru, col_range=(80, 150), show_info=False, title=df_pc_summary, fix_aspect=True, wait=False)
plot_map(df_filtered, df_pc_ru, col_range=(80, 130), show_info=True, title=df_filtered_summary, fix_aspect=False, wait=True)
