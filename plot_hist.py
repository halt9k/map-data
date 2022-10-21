from matplotlib import pyplot as plt
from math import isnan
from i18n import t


# th1, th2 - thresholds to split countries to 3 categories by life expectancy
def plot_growth_hist(df, bins, caption, stop, th1=70, th2=75):
    ndf = df[df.Expectancy.isna()]
    print('Expectancy hist: skipped due to nan: ' + str(ndf.Code))
    df = df[~df.Expectancy.isna()]

    # split to 3 tables, plot all on same hist
    df_modern = df[df.Expectancy > th2]
    l_modern = 'LE > {:2.1f}y'.format(th2)

    df_transfer = df[(th2 >= df.Expectancy) & (df.Expectancy > th1)]
    l_transfer = '{:2.1f}y >= LE > {:2.1f}y'.format(th2, th1)

    df_medieval = df[th1 >= df.Expectancy]
    l_medieval = '{:2.1f}y >= LE'.format(th1)

    assert(len(df_modern) + len(df_transfer) + len(df_medieval) == len(df))

    growths = [df_modern.Growth, df_transfer.Growth, df_medieval.Growth]
    labels = [l_modern, l_transfer, l_medieval]
    colors = ['g', 'y', 'r']

    # bins = np.concatenate(([0], np.arange(90, 120+1, 2), [1000]))
    fig, ax = plt.subplots()
    plt.style.use('seaborn-deep')

    ax.set_xticks(bins)
    plt.hist(growths, bins, label=labels, color=colors)
    plt.xlabel(caption)
    plt.ylabel(t('AMOUNT'))

    plt.legend(loc='upper right')
    plt.plot()
    if stop:
        plt.show()
