import numpy as np

# --- next values are used only for assertions, change not supported ---
# (to ensure thet descriptions match data, match filters)

# main infographic target, how population changed (%) between
C_FROM_Y = 2000
C_TO_Y = 2020

# threshold to remove countries with unstable %
# (total population must be higher than)
CT_POPULATION_M = 5
CT_POPULATION_AT_Y = C_TO_Y

# threshold to remove countries without education systems
# (amount of nobel prize winners higher than)
CT_NOBELS = 2
CT_NOBELS_AT_Y = 2022

# threshold to remove countries without healthcare systems
# (life expectancy must be higher than)
CT_LE_DELEVOPED = 65.0
CT_LE_MODERN = 76.0
CT_LE_AT_Y = 2019

# --- next values can be changed ---
C_HIST_BINS = np.arange(50, 200 + 1, 5)
C_HIST_THRESHOLDS = (CT_LE_DELEVOPED, CT_LE_MODERN)
