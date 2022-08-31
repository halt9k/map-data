import typing
import pandas as pd
import numpy as np

from shapely.geometry import LineString, Point
from shapely import affinity
import geopandas

import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.patheffects as PathEffects

import translations

def has_overlaps(pt_moved, spaced_pts, crit_overlap):
    for pt_taken in spaced_pts:
        cur_overlap = pt_moved.distance(pt_taken)
        if cur_overlap < crit_overlap:
            return pt_taken
    return None

# must operate under geo coodrinates, not plane xy
def space_captions(src_points, spr_repulse_center, spr_dist, pos_limit_y):
    taken_pts = []
    for pt_src in src_points:
        cur_dist = pt_src.distance(spr_repulse_center)        

        # lens styled positions adjust
        ratio = cur_dist / spr_dist
        if ratio < 1.0:
            # mul = 1 - ratio**0.2
            mul = 1 / (ratio + 0.05)
            dx, dy = -spr_repulse_center.x + pt_src.x, -spr_repulse_center.y + pt_src.y

            pt_moved = affinity.translate(pt_src, dx * mul, dy * mul, 0)
            pt_moved = Point(pt_moved.x, np.fmin(pos_limit_y, pt_moved.y))
        else:
            pt_moved = pt_src

        # preventing overlaps
        crit_overlap = spr_dist * 0.2
        for _ in range(0):
            pt_taken = has_overlaps(pt_moved, taken_pts, crit_overlap)
            if pt_taken is None:
                break

            # pt_taken

            pt_moved = affinity.rotate(pt_moved, 10, pt_src)
            print ('Rotate attempt')

        taken_pts += [pt_moved]
    return taken_pts


def add_arrow(rendered_label, pt_tgt, pt_caption):
    x,y,dx,dy = pt_caption.x, pt_caption.y, pt_tgt.x - pt_caption.x, pt_tgt.y - pt_caption.y

    # overlaps label itself
    x += dx*0.1
    y += dy*0.1
    dx*=0.9
    dy*=0.9


    #bbox = rendered_label.get_window_extent()
    plt.arrow(x,y,dx,dy, head_width=0.5, head_length=1, linewidth=0.5)


def add_caption(txt, pt_tgt, pt_caption):
    x,y,dx,dy = pt_caption.x, pt_caption.y, pt_tgt.x - pt_caption.x, pt_tgt.y - pt_caption.y    
            
    lbl = plt.text(pt_caption.x, pt_caption.y, txt, size=7, color='black', ha='center', va='center')
    lbl.set_bbox(dict(facecolor='white', alpha=0.8, linewidth=0.5, pad = 1))
    return lbl


def format_l(year):
    if np.isnan(year):
        return 'L-'        
    else:
        return 'L' + str(int(year))

# without magnifying tricks captions will overlap badly over EU
def plot_captions(fig, df):
    df['centers_xy'] = df.centroid

    # point for magnifying is selected between l1 and l2
    # matplotlib.pyplot.arrow(x, y, dx, dy, **kwargs)
    l1_pos = df[df.iso_a3 == 'POL'].centers_xy.values[0]
    l2_pos = df[df.iso_a3 == 'DEU'].centers_xy.values[0]    

    spr_force_source = LineString([l1_pos, l2_pos]).interpolate(0.8, normalized=True)
    spa_pos = df[df.iso_a3 == 'ISR'].centers_xy.values[0]
    spr_dist = spr_force_source.distance(spa_pos) + 1

    # used to limit labels from being positioned above map
    pos_limit_y = df[df.iso_a3 == 'NOR'].centers_xy.values[0].y

    df['captions_xy'] = space_captions(df.centers_xy, spr_force_source, spr_dist, pos_limit_y)

    # unused now, could be passed to library to try auto spacing
    arrow_preps = []
    for i in range(0, df.shape[0]):
        if np.isnan(df.Growth[i]):
            continue
        # txt = "{}\n{}%\n{}y\n{}" Include provokative labels
        txt = "{}\n{}%\n{}y".format(df.iso_a3[i],
                                round(df.Growth[i]),
                                round(df.Expectancy[i]),
                                format_l(df.legalizeYear[i]))
        lbl = add_caption(txt, df.centers_xy[i], df.captions_xy[i])
        arrow_preps += [[i, lbl]]

    # to clip arrows under transparent bboxes, nessesary to draw and save bboxes first
    fig.canvas.draw()
    for prep in arrow_preps:
        i = prep[0]
        lbl = prep[1]
        add_arrow(lbl, df.centers_xy[i], df.captions_xy[i])    


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
        plot_captions(fig, df_world_merged)

    plt.plot()
    if wait:
        plt.show()