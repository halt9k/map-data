import typing
import numpy as np

from matplotlib import pyplot as plt

import translations


def sy(val):
    return str(val) + 'y'

# th1, th2 - thresholds to split countries to 3 categories by life expectancy
def plot_growth_hist(df, bins, caption, stop, th1=70, th2=75):

    # split to 3 tables, plot all on same hist
    df_modern = df[th2 <= df.Expectancy]
    df_transfer = df[(th1 <= df.Expectancy) & (df.Expectancy < th2)]
    df_medieval = df[df.Expectancy < th1]

    # bins = np.concatenate(([0], np.arange(90, 120+1, 2), [1000]))

    fig, ax = plt.subplots()

    plt.style.use('seaborn-deep')
    growths = [df_modern.Growth, df_transfer.Growth, df_medieval.Growth]
    labels = [sy(th2) + ' <= LE', sy(th1) + ' <= LE < ' + sy(th2), 'LE < ' + sy(th1)]
    colors = ['g', 'y', 'r']
     
    ax.set_xticks(bins)
    plt.hist(growths, bins, label=labels, color=colors)
    plt.xlabel(caption)
    plt.ylabel(translations.AMOUNT)

    plt.legend(loc='upper right')
    plt.plot()
    if stop:
        plt.show()
