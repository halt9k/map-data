import pandas as pd
import numpy as np
import geopandas
import matplotlib as mpl
from matplotlib import pyplot as plt

plt.tight_layout()

def sy(val):
    return str(val) + 'y'

def plot_growth_hist_split_life_expectancy(df, bins, caption, stop, figN, s1=70, s2=75):
    df_modern = df[s2 <= df.Expectancy]
    df_transfer = df[(s1 <= df.Expectancy) & (df.Expectancy < s2)]
    df_medieval = df[df.Expectancy < s1]

    # bins = np.concatenate(([0], np.arange(90, 120+1, 2), [1000]))

    plt.figure(figN)

    plt.style.use('seaborn-deep')
    growths = [df_modern.Growth, df_transfer.Growth, df_medieval.Growth]
    labels = [sy(s2) + ' <= life expectancy', sy(s1) + ' <= life expectancy < ' + sy(s2), 'life expectancy < ' + sy(s1)]
     
    plt.hist(growths, bins, label=labels)
    plt.xlabel(caption)
    plt.ylabel("Amount of countries")

    plt.legend(loc='upper right')
    plt.plot()
    if stop:
        plt.show()

def plot_map(df, names, caption, stop, figN):
    # geopandas default have 

    # merge geopandas data with our data
    # 'naturalearth_lowres' is internal geopandas dataset
    # rename the columns so that we can merge with our data
    # TODO 1 fix to unpacked zip
    world = geopandas.GeoDataFrame.from_file(geopandas.datasets.get_path('naturalearth_lowres'))

    # bugfix wtf
    assert(world[world.name=='France'].iso_a3.values[0] == '-99')
    world.loc[world.name == 'France', 'iso_a3'] = 'FRA'
    world.loc[world.name == 'Norway', 'iso_a3'] = 'NOR'
    world.loc[world.name == 'N. Cyprus', 'iso_a3'] = 'CYP'
    world.loc[world.name == 'Somaliland', 'iso_a3'] = 'SOM'
    world.loc[world.name == 'Kosovo', 'iso_a3'] = 'RKS'

    df.rename(columns = {'Code':'iso_a3'}, inplace = True)
    df_merge = pd.merge(world, df, on='iso_a3')

    # plot world map
    # plt.figure(figN)
    col_norm = mpl.colors.Normalize(vmin=80, vmax=150)
    skipped_areas_desc = {"color": "lightgrey", "edgecolor": "red", "hatch": "///", "label": "",}
    df_merge.plot(column='Growth',  norm=col_norm,
               figsize=(40, 20),
               legend=True, cmap='plasma')
               #missing_kwds=skipped_areas_desc)

    # add countries names and numbers
    
    plt.title(caption, fontsize=8)
    if names:
        centers_xy = df_merge.centroid

        for i in range(0, df_merge.shape[0]):
            txt = "{}\n{}% {}y".format(df_merge.iso_a3[i],
                                   round(df_merge.Growth[i], 0),
                                   round(df_merge.Expectancy[i], 0))
            plt.text(centers_xy[i].x,
                centers_xy[i].y,
                txt,
                size=8)

    plt.plot()
    if stop:
        plt.show()

