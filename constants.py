"""
Calculate and store constants relating to model
"""

import pandas as pd
import helpers
import temperature

# Read parameters, shape into dictionary
param_df = pd.read_csv("params.csv")
PARAM_DICT = param_df.set_index(['species', 'type', 'percent']).to_dict(orient='index')

# From parameters, isolate those specific to a tree (but specify leaf color or fall)
tree_df = param_df.drop(["threshold", "percent"], axis=1)
tree_df = tree_df.drop_duplicates()
TREE_DICT = tree_df.set_index(['species', 'type']).to_dict(orient='index')

# Coordinates of Harvard Forest
LATITUDE = 42.53169917668065
LONGITUDE = -72.1899469241446

# Period for temperature data
START_DATE = "1993-01-01"
END_DATE = "2010-12-31"

# Hours of daylight for every day of year
DAILY_PHOTOPERIOD = helpers.photoperiod(LATITUDE)

# Temperature data for specified location and time period
TEMP_DATA = temperature.get_data(LATITUDE, LONGITUDE, START_DATE, END_DATE)
