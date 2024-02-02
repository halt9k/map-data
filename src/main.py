from os import chdir
from pathlib import Path

from data.df_preprocess_world import get_df_population_change
from data.df_preprocess_ru import get_df_population_change_ru
from data.df_process import merge_geo_tables, filter_geo_table
from consts import *
from plot_hist import plot_growth_hist
from plot_map import plot_map


from translations import fill_translations, loc_set, t


class Dataframes:
    def __init__(self):
        self.pc = None
        self.pc_summary = None
        self.pc_ru = None
        self.merged = None
        self.filtered = None
        self.filtered_summary = None


def set_consistent_root_parth():
    app_root_path = Path(__file__).parent.parent
    chdir(app_root_path)
    assert(Path.exists(app_root_path / 'data'))
    print(f'Root path is set to {app_root_path}')


def init_app():
    set_consistent_root_parth()
    fill_translations()
    loc_set('locale', 'en')


def prep_dataframes():
    df = Dataframes()
    df.pc = None
    df.pc, info_pc = get_df_population_change(C_FROM_Y, C_TO_Y)
    df.pc_summary = info_pc.format(where=t('ALL_COUNTRIES'))

    df.pc_ru, info_pc_ru = get_df_population_change_ru(C_FROM_Y, C_TO_Y)

    df.merged = merge_geo_tables(df.pc)
    df.filtered, info_filtered = filter_geo_table(df.merged)

    df.filtered_summary = info_pc.format(where=t('ONLY'))
    df.filtered_summary += info_filtered
    df.filtered_summary += info_pc_ru

    return df


def plot(dataframes):
    dfs = dataframes
    plot_growth_hist(dfs.merged, dfs.pc_summary, C_HIST_BINS, C_HIST_THRESHOLDS)
    plot_growth_hist(dfs.filtered, dfs.filtered_summary, C_HIST_BINS, C_HIST_THRESHOLDS)

    plot_map(dfs.merged, dfs.pc_ru, col_range=(80, 150), show_info=False, title=dfs.pc_summary, fix_aspect=True, wait=False)
    plot_map(dfs.filtered, dfs.pc_ru, col_range=(80, 130), show_info=True, title=dfs.filtered_summary, fix_aspect=False, wait=True)


def main():
    init_app()

    dataframes = prep_dataframes()
    plot(dataframes)


if __name__ == '__main__':
    main()