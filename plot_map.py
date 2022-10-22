import pandas as pd
import numpy as np

from shapely.geometry import LineString, Point
from shapely import affinity
import geopandas

import matplotlib as mpl
from matplotlib import pyplot as plt
# import matplotlib.patheffects as PathEffects


def add_arrow(rendered_label, pt_tgt, pt_caption):
    x, y, dx, dy = pt_caption.x, pt_caption.y, pt_tgt.x - pt_caption.x, pt_tgt.y - pt_caption.y

    # decreases overlap of arrow over label of this arrow
    x += dx * 0.1
    y += dy * 0.1
    dx *= 0.9
    dy *= 0.9

    # bbox = rendered_label.get_window_extent()
    plt.arrow(x, y, dx, dy, head_width=0.5, head_length=1, linewidth=0.5)


def plot_arrows_from_captions(fig, df, arrow_preps):
    # to clip arrows under transparent bboxes, nessesary to draw and save bboxes first
    fig.canvas.draw()

    for prep in arrow_preps:
        i = prep[0]
        lbl = prep[1]
        add_arrow(lbl, df.centers_xy[i], df.captions_xy[i])


def add_caption(txt, pt_caption):
    lbl = plt.text(pt_caption.x, pt_caption.y, txt, size=7, color='black', ha='center', va='center')
    lbl.set_bbox(dict(facecolor='white', alpha=0.8, linewidth=0.5, pad=1))
    return lbl


def format_l(year):
    if np.isnan(year):
        return 'L-'
    else:
        return 'L' + str(int(year))


def has_overlaps(pt_moved, spaced_pts, crit_overlap):
    for pt_taken in spaced_pts:
        cur_overlap = pt_moved.distance(pt_taken)
        if cur_overlap < crit_overlap:
            return pt_taken
    return None


def lens(pt_src, pt_lens_center, lens_force, pos_limit_y):
    cnt_dist = pt_src.distance(pt_lens_center)

    # lens styled positions adjust
    ratio = cnt_dist / lens_force
    if 0 < ratio < 1.0:
        # mul = 1 - ratio**0.2
        mul = 1 / (ratio + 0.05)
        dx, dy = -pt_lens_center.x + pt_src.x, -pt_lens_center.y + pt_src.y

        pt_moved = affinity.translate(pt_src, dx * mul, dy * mul, 0)
        return Point(pt_moved.x, np.fmin(pos_limit_y, pt_moved.y))
    else:
        return pt_src


def try_avoid_overlaps(pt_src, pt_moved, adjusted_pts, lens_force):
    # disabled now

    crit_overlap = lens_force * 0.2
    for _ in range(0):
        pt_taken = has_overlaps(pt_moved, adjusted_pts, crit_overlap)
        if pt_taken is None:
            break

        # pt_taken

        pt_moved = affinity.rotate(pt_moved, 10, pt_src)
        print('Rotate attempt')

    return pt_moved


def space_caption_positions(src_pts, pt_lens_center, lens_force, pos_limit_y):
    # must operate under geo coodrinates, not plane xy
    # spr_dist = 0 means no caption position adjusting

    adjusted_pts = []
    for pt_src in src_pts:
        pt_moved = lens(pt_src, pt_lens_center, lens_force, pos_limit_y)
        pt_moved = try_avoid_overlaps(pt_src, pt_moved, adjusted_pts, lens_force)

        adjusted_pts += [pt_moved]
    return adjusted_pts


def get_caption_pos_adjust_params(df):
    # point for magnifying is selected between l1 and l2
    # matplotlib.pyplot.arrow(x, y, dx, dy, **kwargs)
    l1_pos = df[df.iso_a3 == 'POL'].centers_xy.values[0]
    l2_pos = df[df.iso_a3 == 'DEU'].centers_xy.values[0]

    spr_force_source = LineString([l1_pos, l2_pos]).interpolate(0.8, normalized=True)
    spa_pos = df[df.iso_a3 == 'ISR'].centers_xy.values[0]
    spr_dist = spr_force_source.distance(spa_pos) + 1

    # used to limit labels from being positioned above map
    pos_limit_y = df[df.iso_a3 == 'NOR'].centers_xy.values[0].y

    return spr_force_source, spr_dist, pos_limit_y


def plot_captions(fig, df, try_space=True):
    df['centers_xy'] = df.centroid

    # simple approach without magnifying
    # will overlap all over EU
    if try_space:
        spr_force_source, spr_dist, pos_limit_y = get_caption_pos_adjust_params(df)
        df['captions_xy'] = space_caption_positions(df.centers_xy, spr_force_source, spr_dist, pos_limit_y)
    else:
        df['captions_xy'] = df.centers_xy

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
        lbl = add_caption(txt, df.captions_xy[i])
        arrow_preps += [[i, lbl]]

    plot_arrows_from_captions(fig, df, arrow_preps)


def clean_unicode_text(cl):
    return [r.encode('ascii', 'ignore').decode('ascii') for r in cl]


def get_ru_map():
    ru_shape = geopandas.GeoDataFrame.from_file("Data/Ru/_Simplified\\geoBoundaries-RUS-ADM1_simplified.shp")
    ru_shape.shapeName = clean_unicode_text(ru_shape.shapeName)
    return ru_shape


def get_geopandas_world_map():
    # 'naturalearth_lowres' is internal geopandas dataset
    world = geopandas.GeoDataFrame.from_file(geopandas.datasets.get_path('naturalearth_lowres'))

    # geopandas bugfix wtf
    assert (world[world.name == 'France'].iso_a3.values[0] == '-99')
    world.loc[world.name == 'France', 'iso_a3'] = 'FRA'
    world.loc[world.name == 'Norway', 'iso_a3'] = 'NOR'
    world.loc[world.name == 'N. Cyprus', 'iso_a3'] = 'CYP'
    world.loc[world.name == 'Somaliland', 'iso_a3'] = 'SOM'
    world.loc[world.name == 'Kosovo', 'iso_a3'] = 'RKS'

    # no Arctica here
    world = world[(world.name != "Antarctica") & (world.name != "Fr. S. Antarctic Lands")]

    return world


def decrease_marigins(fig):
    # default geopandas marigins are enourmously huge

    fig.tight_layout(pad=0)
    fig.subplots_adjust(top=0.98, bottom=0, left=0, right=1, hspace=0, wspace=0)


def set_mercurial_projection(areas):
    areas.to_crs("EPSG:3395", inplace=True)


def add_df_columns_to_map_data(df_world, df_ru):
    # uses internal world preset and external ru map

    df_world_areas = get_geopandas_world_map()
    df_ru_areas = get_ru_map()

    assert (df_world_areas.crs == df_ru_areas.crs)
    set_mercurial_projection(df_world_areas)
    set_mercurial_projection(df_ru_areas)

    # merge geo shape data with provided data
    df_world.rename(columns={'Code': 'iso_a3'}, inplace=True)
    df_world_merged = pd.merge(df_world_areas, df_world, on='iso_a3', how='left')  # CYP 2x , validate='1:1')

    df_ru_areas.rename(columns={'shapeName': 'iso_name'}, inplace=True)
    df_ru_merged = pd.merge(df_ru_areas, df_ru, on='iso_name', how='left', validate='1:1')

    return df_world_merged, df_ru_merged


def plot_map(df_world, df_ru, col_range, show_info, title, fix_aspect, wait):
    df_world_merged, df_ru_merged = add_df_columns_to_map_data(df_world, df_ru)

    col_norm = mpl.colors.Normalize(vmin=col_range[0], vmax=col_range[1])
    skipped_areas_desc = {"color": "lightgrey", "edgecolor": "black", "label": ""}

    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots(figsize=(20, 16))
    decrease_marigins(fig)

    df_world_merged.plot(column='Growth', ax=ax,
                         norm=col_norm, cmap='jet',
                         legend=True, legend_kwds={'shrink': 0.3, 'orientation': "horizontal", 'format': "%d%%"},
                         edgecolor='black',
                         missing_kwds=skipped_areas_desc)

    df_ru_merged.plot(column='Growth', ax=ax,
                      norm=col_norm, cmap='jet',
                      legend=False,
                      missing_kwds=skipped_areas_desc)

    # aspect became adjusted indirectly
    # on 2nd .plot call with limited area
    if ~fix_aspect:
        ax.set_aspect('equal')

    # add country names and numbers
    plt.title(title, fontsize=12, y=-0.20)
    if show_info:
        plot_captions(fig, df_world_merged)

    plt.plot()
    if wait:
        plt.show()
