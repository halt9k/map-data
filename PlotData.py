import pandas as pd
import numpy as np
import geopandas
import matplotlib
from matplotlib import pyplot as plt

plt.tight_layout()

def sy(val):
    return str(val) + 'y'

def plot_growth_hist_split_life_expectancy(df, bins, caption, figureN, stop):
    # split into two categories: developed (life > 70) and developing (life <
    # 70)
    s1 = 70
    s2 = 75

    df_modern = df[s2 <= df.Expectancy]
    df_transfer = df[(s1 <= df.Expectancy) & (df.Expectancy < s2)]
    df_medieval = df[df.Expectancy < s1]

    # bins = np.concatenate(([0], np.arange(90, 120+1, 2), [1000]))

    plt.figure(figureN)

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

def plot_map(df, stop, names, caption):
    # merge geopandas data with our data
    # 'naturalearth_lowres' is internal geopandas dataset
    # rename the columns so that we can merge with our data
    world = geopandas.GeoDataFrame.from_file(geopandas.datasets.get_path('naturalearth_lowres'))

    # merge again with our location data which
    # contains each country’s latitude and longitude
    df.rename(columns = {'Code':'iso_a3'}, inplace = True)
    merge = pd.merge(world, df, on='iso_a3')

    location = pd.read_csv('Data\countries_latitude_longitude.csv')
    merge = merge.merge(location,on='name').sort_values(by='Growth',ascending=False).reset_index()

    # plot confirmed cases world map
    merge.plot(column='Growth', scheme="quantiles",
               figsize=(25, 20),
               legend=True,cmap='coolwarm')

    # add countries names and numbers
    plt.title(caption, fontsize=20)
    if names:
        for i in range(0, merge.shape[0]):
            txt = "{}\n{}%".format(merge.name[i],
                                   round(merge.Growth[i]))
            plt.text(float(merge.longitude[i]),
                float(merge.latitude[i]),
                txt,
                size=10)

    plt.plot()
    if stop:
        plt.show()

