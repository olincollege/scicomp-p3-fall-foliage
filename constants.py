import pandas as pd
import helpers
import temperature

param_df = pd.read_csv("params.csv")
PARAM_DICT = param_df.set_index(['species', 'type', 'percent']).to_dict(orient='index')

tree_df = param_df.drop(["threshold", "percent"], axis=1)
tree_df = tree_df.drop_duplicates()
TREE_DICT = tree_df.set_index(['species', 'type']).to_dict(orient='index')
# Convert DataFrame to dictionary

LATITUDE = 42.53169917668065
LONGITUDE = -72.1899469241446
START_DATE = "1993-01-01"
END_DATE = "2010-12-31"

DAILY_PHOTOPERIOD = helpers.photoperiod(LATITUDE)
TEMP_DATA = temperature.get_data(LATITUDE, LONGITUDE, START_DATE, END_DATE)