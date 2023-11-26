import pandas as pd
import numpy as np
import helpers as h
import temperature

# Refactor so that Tree and Tree_Specific are separate classes - Specific inherits Tree?

TEMP_DATA = temperature.get_data()

class Tree_Specific:
    def __init__(self, photo_start, temp_sen, version, x, y, y_crit, year):
        # Tree Model
        self.photo_start = photo_start
        self.temp_sen = temp_sen
        self.version = version
        self.x = x
        self.y = y
        self.temp_data = TEMP_DATA
        # Needham's lattitude
        self.lattitude = 42.53169917668065
        self.photo_daily = h.photoperiod(self.lattitude, np.arange(1, 366))
        

        # Specific model
        self.y_crit = y_crit
        self.year = year
        self.sen_daily = np.zeros([365, 1])
        
    def get_temperature(self, day_of_year):
        try:
            temperature = self.temp_data[(self.temp_data["year"] == self.year) & (self.temp_data["doy"] == day_of_year)]["temperature"].values[0]
            return temperature
        except IndexError:
            print("Error: Year and/or day of year not available in queried data")
            return None

    def photo_func_selector(self, day_of_year):
        if self.version == 1:
            return(self.photo_daily[day_of_year - 1] / self.photo_start)
        
        if self.version == 2:
            return(1 - (self.photo_daily[day_of_year - 1] / self.photo_start))
        
        print("ERROR: Invalid Value")
        return -1

    def rate_senescence(self, day_of_year):
        t_today = self.get_temperature(day_of_year)
        if  t_today >= self.temp_sen:
            return 0
        
        return (((self.temp_sen - t_today) ** self.x) * (self.photo_func_selector(day_of_year) ** self.y))

    def update_senescence(self, day_of_year):
        if self.photo_daily[day_of_year - 1] >= self.photo_start:
            self.sen_daily[day_of_year - 1] = 0
        else:
            self.sen_daily[day_of_year - 1] = self.sen_daily[day_of_year - 2] + self.rate_senescence(day_of_year)

