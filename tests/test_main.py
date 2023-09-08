from main import prep_dataframes, init_app
from plot_map import plot_map


def test_plot():
    init_app()
    dfs = prep_dataframes()
    plot_map(dfs.merged, dfs.pc_ru, col_range=(80, 150), show_info=True, title=dfs.pc_summary, fix_aspect=True, wait=True)
    assert True
