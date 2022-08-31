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


# must operate under geo coodrinates, not plane xy
def space_captions(src_pos, spr_center, pos_min_y, spr_dist):
    spaced_pos = []
    for place in src_pos:
        cur_dist = place.distance(spr_center)
        pos = place

        # non-final manual adjust 
        ratio = cur_dist / spr_dist
        if 0.1 < ratio < 1.0:
            # mul = 1 - ratio**0.2
            mul = 2 / (ratio + 0.1) # + ratio ** 0.2 / 4.0
            dx, dy = -spr_center.x + place.x, -spr_center.y + place.y
            max_mul = (pos_min_y - spr_center.y) / dy
            mul_y = np.fmin(abs(max_mul), mul)
            pos = affinity.translate(spr_center, dx * mul, dy * mul_y, 0)
        spaced_pos += [pos]
    return spaced_pos


def add_caption(plt, txt, place, caption_place):
    x,y,dx,dy = place.x, place.y, -caption_place.x + place.x, -caption_place.y + place.y
    plt.arrow(x,y,dx,dy, head_width=0.5, head_length=1, linewidth=0.5)
            
    plt_txt = plt.text(caption_place.x, caption_place.y, txt, size=7, color='black')
    plt_txt.set_bbox(dict(facecolor='white', alpha=0.8, linewidth=0.5, pad = 1))
    return plt_txt


def format_l(year):
    if np.isnan(year):
        return 'L-'        
    else:
        return 'L' + str(int(year))

# with magnifying over EU
def plot_ovelapping_captions(plt, df):
    df['centers_xy'] = df.centroid

    # matplotlib.pyplot.arrow(x, y, dx, dy, **kwargs)
    ger_pos = df[df.iso_a3 == 'POL'].centers_xy.values[0]
    fra_pos = df[df.iso_a3 == 'DEU'].centers_xy.values[0]
    pos_min_y = df[df.iso_a3 == 'NOR'].centers_xy.values[0].y

    cen_pos = LineString([ger_pos, fra_pos]).interpolate(0.8, normalized=True)
    spa_pos = df[df.iso_a3 == 'ISR'].centers_xy.values[0]
    spr_dist = cen_pos.distance(spa_pos) + 1

    df['captions_xy'] = space_captions(df.centers_xy, cen_pos, pos_min_y, spr_dist)

    texts = []
    for i in range(0, df.shape[0]):
        if np.isnan(df.Growth[i]):
            continue
        txt = "{}\n{}%\n{}y\n{}".format(df.iso_a3[i],
                                round(df.Growth[i]),
                                round(df.Expectancy[i]),
                                format_l(df.legalizeYear[i]))
        texts += [add_caption(plt, txt, df.centers_xy[i], df.captions_xy[i])]


def clean_unicode_text(cl):
    return [r.encode('ascii', 'ignore').decode('ascii') for r in cl]


def get_ru_map():
    ru_shape = geopandas.GeoDataFrame.from_file("Data\\Ru\\Simplified\\geoBoundaries-RUS-ADM1_simplified.shp")
    ru_shape.shapeName = clean_unicode_text(ru_shape.shapeName)
    return ru_shape

def get_geopandas_world_map():
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
    fig.subplots_adjust(top=0.98, bottom=0, left=0, right=1, hspace=0, wspace=0)


def plot_map(df_world_info, df_ru_info, col_min, col_max, show_info, caption_text, asp, wait):
    df_world_areas = get_geopandas_world_map()
    df_ru_areas = get_ru_map()    


    # merge geo shape data with provided data
    df_world_info.rename(columns = {'Code':'iso_a3'}, inplace = True)
    df_world_merged = pd.merge(df_world_areas, df_world_info, on='iso_a3', how='left') # CYP 2x , validate='1:1') 

    df_ru_areas.rename(columns = {'shapeName':'iso_name'}, inplace = True)
    df_ru_merged = pd.merge(df_ru_areas, df_ru_info, on='iso_name', how='left', validate='1:1')


    # plot world map
    col_norm = mpl.colors.Normalize(vmin=col_min, vmax=col_max)
    skipped_areas_desc = {"color": "lightgrey", "edgecolor": "black", "label": ""}

    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots( figsize=(20, 16))
    remove_geopandas_marigins(fig)

    df_world_merged.plot(column='Growth', ax=ax,
                       norm=col_norm, cmap='plasma',
                       legend=True, legend_kwds={'shrink': 0.3, 'orientation': "horizontal", 'format':"%d%%"},
                       edgecolor='black',
                       missing_kwds=skipped_areas_desc)
    
    df_ru_merged.plot(column='Growth', ax=ax,
                       norm=col_norm, cmap='plasma',                       
                       legend=False,
                       missing_kwds=skipped_areas_desc)
    
    # became adjusted after 2nd .plot call with limited area
    if ~asp:
        ax.set_aspect('equal')
    
    # add countries names and numbers
    plt.title(caption_text, fontsize=8, y=-0.2)
    if show_info:
        plot_ovelapping_captions(plt, df_world_merged)

    plt.plot()
    if wait:
        plt.show()