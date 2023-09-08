import numpy as np
import pandas as pd
from i18n import t

from data.df_preprocess_world import get_df_life_expectancy, get_df_nobels_amount, get_df_l_religions
from src.consts import *


def merge_geo_tables(df_into):
	df_le = get_df_life_expectancy(CT_LE_AT_Y)
	df_nb = get_df_nobels_amount(CT_NOBELS_AT_Y)
	df_l = get_df_l_religions()

	# combining all to unfiltered table
	df = pd.merge(df_into, df_le, on='Code', how='left', validate='1:1')
	df = pd.merge(df, df_nb, on='Code', how='left', validate='1:1')
	df = pd.merge(df, df_l, on='Code', how='left', validate='1:1')

	return df


def filter_geo_table(df_src):
	df = df_src.copy()
	df.Growth[CT_POPULATION_M * 10 ** 6 > df.at_2020] = np.nan
	df.Growth[df.Expectancy.isnull() | (CT_LE_DELEVOPED > df.Expectancy)] = np.nan
	df.Growth[df.Nobels.isnull() | (CT_NOBELS > df.Nobels)] = np.nan

	info = " P > {}M, LE > {}y, NB > {} \n".format(CT_POPULATION_M, CT_LE_DELEVOPED, CT_NOBELS)
	info += t('POPULATION') + ", {}; ".format(CT_POPULATION_AT_Y)
	info += t('EXPECTANCY') + ", {}; ".format(CT_LE_AT_Y)
	info += t('NOBLES') + ", {}; \n".format(CT_NOBELS_AT_Y)

	return df, info
