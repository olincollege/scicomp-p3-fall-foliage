import numpy as np
import pygame as pg
from constants import PARAM_DICT, TREE_DICT, DAILY_PHOTOPERIOD, TEMP_DATA
import helpers as h

class Tree:
    def __init__(self, species, type, photo_start, trigger_temp, eq_version, x, y):
        self.species = species
        self.type = type
        self.photo_start = photo_start
        self.trigger_temp = trigger_temp
        self.eq_version = eq_version
        self.x = x
        self.y = y

    @classmethod
    def create_tree(cls, species, type):
        params = TREE_DICT[species, type]
        return cls(species, type, **params)
        
class Tree_Modeller:

    def __init__(self, species, type, year):
        # Tree Model
        self.tree = Tree.create_tree(species, type)
        
        self.year = year
        self.sen_daily = np.zeros([365, 1])
        self.sen_norm = np.zeros([365, 1])

        self.max_sen = self.get_threshold(90) * (10/9)
        
    def get_temperature(self, day_of_year):
        try:
            temperature = TEMP_DATA[(TEMP_DATA["year"] == self.year) & (TEMP_DATA["doy"] == day_of_year)]["temperature"].values[0]
            return temperature
        except IndexError:
            print("Error: Year and/or day of year not available in queried data")
            return None
        
    def get_threshold(self, percent):
        params = PARAM_DICT[self.tree.species, self.tree.type, percent]
        return params["threshold"]

    def photo_func_selector(self, day_of_year):
        if self.tree.eq_version == 1:
            return(DAILY_PHOTOPERIOD[day_of_year - 1] / self.tree.photo_start)
        
        if self.tree.eq_version == 2:
            return(1 - (DAILY_PHOTOPERIOD[day_of_year - 1] / self.tree.photo_start))
        
        print("ERROR: Invalid Value")
        return -1

    def rate_senescence(self, day_of_year):
        t_today = self.get_temperature(day_of_year)
        if  t_today >= self.tree.trigger_temp:
            return 0
        
        return (((self.tree.trigger_temp - t_today) ** self.tree.x) * (self.photo_func_selector(day_of_year) ** self.tree.y))

    def update_senescence(self, day_of_year):
        if DAILY_PHOTOPERIOD[day_of_year - 1] >= self.tree.photo_start:
            self.sen_daily[day_of_year - 1] = 0
        else:
            self.sen_daily[day_of_year - 1] = self.sen_daily[day_of_year - 2] + self.rate_senescence(day_of_year)

        self.sen_norm[day_of_year - 1] = min(1, self.sen_daily[day_of_year - 1] / self.max_sen)

class Tree_View:

    def __init__(self, species, year, screen):
        self.color_model = Tree_Modeller(species, "coloring", year)
        self.fall_model = Tree_Modeller(species, "falling", year)
        self.screen = screen

    def update(self, doy):
        self.color_model.update_senescence(doy)
        self.fall_model.update_senescence(doy)

    def draw_tree(self, x, y, doy, show_fall = True):
        radius = 30
        width = 20
        height = 40
        color = self.color_model.sen_norm[doy - 1]
        fallen = self.fall_model.sen_norm[doy - 1]
        # print(color)
        pg.draw.rect(self.screen, (139, 69, 19), (x, y, width, height))  # Trunk
        target_rect = pg.Rect((x + width // 2, y), (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
        pg.draw.circle(shape_surf, h.scale_color(color, fallen, show_fall), (radius, radius), radius)
        self.screen.blit(shape_surf, target_rect)