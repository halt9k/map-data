import typing
import pandas as pd
import numpy as np

from shapely.geometry import LineString
from shapely import affinity
import geopandas

import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.patheffects as PathEffects

import translations

def add_caption(plt, txt, place, spr_center, pos_min_y, spr_dist):
    cur_dist = place.distance(spr_center)
    pos = place
    ratio = cur_dist / spr_dist
    if ratio < 1.0:
        # mul = 1 - ratio**0.2
        mul = 2 / (ratio + 0.1) # + ratio ** 0.2 / 4.0
        dx, dy = -spr_center.x + place.x, -spr_center.y + place.y
        max_mul = (pos_min_y - spr_center.y) / dy
        mul = np.fmin(abs(max_mul), mul)
        pt_throw = affinity.translate(spr_center, dx * mul, dy * 2 * mul, 0)
        x,y,dx,dy = pt_throw.x, pt_throw.y, -pt_throw.x + place.x, -pt_throw.y + place.y
        plt.arrow(x,y,dx,dy, head_width=0.5, head_length=1, linewidth=0.5)
        pos = pt_throw
            
    plt_txt = plt.text(pos.x, pos.y, txt, size=7, color='black')
    plt_txt.set_bbox(dict(facecolor='white', alpha=0.8, linewidth=0.5, pad = 1))


# with magnifying over EU
def plot_ovelapping_captions(plt, df):
    df['centers_xy'] = df.centroid

    # matplotlib.pyplot.arrow(x, y, dx, dy, **kwargs)
    ger_pos = df[df.iso_a3 == 'BEL'].centers_xy.values[0]
    fra_pos = df[df.iso_a3 == 'DEU'].centers_xy.values[0]
    pos_min_y = df[df.iso_a3 == 'NOR'].centers_xy.values[0].y

    cen_pos = LineString([ger_pos, fra_pos]).interpolate(0.8, normalized=True)
    spa_pos = df[df.iso_a3 == 'ISR'].centers_xy.values[0]
    spr_dist = cen_pos.distance(spa_pos) + 1

    for i in range(0, df.shape[0]):
        if np.isnan(df.Growth[i]):
            continue
        txt = "{}\n{}%\n{}y".format(df.iso_a3[i],
                                round(df.Growth[i]),
                                round(df.Expectancy[i]))
        add_caption(plt, txt, df.centers_xy[i], cen_pos, pos_min_y, spr_dist)


def get_geopandas_fixed_world_map_data():
    # 'naturalearth_lowres' is internal geopandas dataset
    world = geopandas.GeoDataFrame.from_file(geopandas.datasets.get_path('naturalearth_lowres'))

    # geopandas bugfix wtf
    assert(world[world.name == 'France'].iso_a3.values[0] == '-99')
    world.loc[world.name == 'France', 'iso_a3'] = 'FRA'
    world.loc[world.name == 'Norway', 'iso_a3'] = 'NOR'
    world.loc[world.name == 'N. Cyprus', 'iso_a3'] = 'CYP'
    world.loc[world.name == 'Somaliland', 'iso_a3'] = 'SOM'
    world.loc[world.name == 'Kosovo', 'iso_a3'] = 'RKS'
    return world


def remove_geopandas_marigins(fig):
    fig.tight_layout(pad=0)
    fig.subplots_adjust(top=0.9, bottom=0, left=0, right=1, hspace=0, wspace=0)


def plot_map(df, col_min, col_max, show_info, caption_text, wait, figN):    
    df_world = get_geopandas_fixed_world_map_data()

    # merge geopandas data with provided data
    df.rename(columns = {'Code':'iso_a3'}, inplace = True)
    df_merge = pd.merge(df_world, df, on='iso_a3')

    # plot world map
    col_norm = mpl.colors.Normalize(vmin=col_min, vmax=col_max)
    skipped_areas_desc = {"color": "lightgrey", "edgecolor": "black", "label": "",}

    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots()
    remove_geopandas_marigins(fig)
    df_merge.plot(column='Growth', ax=ax,
                       norm=col_norm, cmap='plasma',
                       figsize=(40, 30),
                       legend=True, legend_kwds={'shrink': 0.3, 'orientation': "horizontal", 'format':"%d%%"},
                       # legend=True, legend_kwds={'shrink': 0.2},
                       missing_kwds=skipped_areas_desc)
    
    # add countries names and numbers
    plt.title(caption_text, fontsize=8)
    if show_info:
        plot_ovelapping_captions(plt, df_merge)

    plt.plot()
    if wait:
        plt.show()

