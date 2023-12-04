"""
Contains classes for Tree parameters, modelling, and viewing
"""

import numpy as np
import pygame as pg
from constants import PARAM_DICT, TREE_DICT, DAILY_PHOTOPERIOD, TEMP_DATA
import helpers as h

class Tree:
    """
    A class representing a tree species of a specific phenomenon type.

    Attributes:
        species (str): The species of the tree.
        type (str): The phenomenon type associated with the tree.
        photo_start (float): The threshold photoperiod after which senescence starts
        trigger_temp (float): The temperature below which senescence is triggered
        eq_version (int): The version of an equation used in modeling - 1 or 2
        x (int): Temperature weight: 0, 1 or 2
        y (int): Photoperiod weight: 0, 1, or 2
    """
    def __init__(self, species, type, photo_start, trigger_temp, eq_version, x, y):
        # Tree Instance
        self.species = species
        self.type = type
        self.photo_start = photo_start
        self.trigger_temp = trigger_temp
        self.eq_version = eq_version
        self.x = x
        self.y = y

    @classmethod
    def create_tree(cls, species, type):
        """
        Class method that creates a tree using TREE_DICT

        Args:
            species (str): 4-letter tree species code
            type (str): phenomenon type: either "coloring" or "falling"

        Returns:
            Newly created Tree class with all parameters for given species and type filled in
        """
        params = TREE_DICT[species, type]
        return cls(species, type, **params)

class TreeModeller:
    """
    A modelling instance of a tree

    Atttributes:
        tree (Tree): An instance of a Tree class for specified species and type
        year (int): Year of modelling between 1993 and 2010 (see constants.py)
        sen_daily (numpy array): Contains the sensecence values in arbitrary units
        sen_norm (numpy array): Contains the normalized senescence values (by max_sen)
        max_sen (float): The maximum theoretical senescence value (approximated to 100%)
    """
    def __init__(self, species, type, year):
        # Tree Model
        self.tree = Tree.create_tree(species, type)

        self.year = year
        self.sen_daily = np.zeros([365, 1])
        self.sen_norm = np.zeros([365, 1])

        self.max_sen = self.get_threshold(90) * (10/9)

    def get_temperature(self, day_of_year):
        """
        Retrieves the temperature for a specific day of the year from the temperature data.

        Args:
            day_of_year (int): The day of the year for which temperature is required.

        Returns:
            The float temperature for the specified day of the year.
                  Returns None if the data is not available.
        """
        try:
            temperature = TEMP_DATA[(TEMP_DATA["year"] == self.year) & \
                                    (TEMP_DATA["doy"] == day_of_year)]["temperature"].values[0]
            return temperature
        except IndexError:
            print("Error: Year and/or day of year not available in queried data")
            return None

    def get_threshold(self, percent):
        """
        Retrieves the senescence threshold for a given percentage from the parameter dictionary.

        Args:
            percent (int): The percentage for which to retrieve the senescence threshold.

        Returns:
            The float senescence threshold for the specified percentage.
        """
        params = PARAM_DICT[self.tree.species, self.tree.type, percent]
        return params["threshold"]

    def photo_func_selector(self, day_of_year):
        """
        Selects the appropriate photoperiod function based on the equation version specified.

        Args:
            day_of_year (int): The day of the year for which to select the photoperiod function.

        Returns:
            The results from the specified equation being run as a float
                  Returns -1 if an invalid equipment version is encountered.
        """
        # Photoperiod positively affects senescence
        if self.tree.eq_version == 1:
            return DAILY_PHOTOPERIOD[day_of_year - 1] / self.tree.photo_start

        # Photoperiod negatively affects senescence
        if self.tree.eq_version == 2:
            return 1 - (DAILY_PHOTOPERIOD[day_of_year - 1] / self.tree.photo_start)

        print("ERROR: Invalid Value")
        return -1

    def rate_senescence(self, day_of_year):
        """
        Calculates the rate of senescence at a given day of the year.

        Args:
            day_of_year (int): The day of the year for which to calculate the senescence rate.

        Returns:
            The float calculated senescence rate.
        """
        # Get the day's temperature
        t_today = self.get_temperature(day_of_year)

        # If temperature is greater than trigger temp, no further senscence occurs
        if  t_today >= self.tree.trigger_temp:
            return 0

        return (((self.tree.trigger_temp - t_today) ** self.tree.x)\
                 * (self.photo_func_selector(day_of_year) ** self.tree.y))

    def update_senescence(self, day_of_year):
        """
        Updates the daily and normalized senescence values for a specific day of the year.

        Args:
            day_of_year (int): The day of the year for which to update senescence values.
        """
        # If photoperiod above starting value, sensescence is zero
        if DAILY_PHOTOPERIOD[day_of_year - 1] >= self.tree.photo_start:
            self.sen_daily[day_of_year - 1] = 0

        # Otherwise, senscence today is yesterday + today's rate
        else:
            self.sen_daily[day_of_year - 1] = self.sen_daily[day_of_year - 2]\
                  + self.rate_senescence(day_of_year)

        # Update normalized senescence, ceiling at 1
        self.sen_norm[day_of_year - 1] = min(1, self.sen_daily[day_of_year - 1] / self.max_sen)

class TreeView:
    """
    A class representing the view of a tree for visualization.

    Attributes:
        color_model (TreeModeller): A TreeModeller instance for modeling color changes.
        fall_model (TreeModeller): A TreeModeller instance for modeling falling changes.
        screen (pygame.display): The pygame display on which to draw the tree.
    """
    def __init__(self, species, year, screen):
        # Tree visualizer
        self.color_model = TreeModeller(species, "coloring", year)
        self.fall_model = TreeModeller(species, "falling", year)
        self.screen = screen

    def update(self, day_of_year):
        """
        Updates the color and falling models for a specific day of the year.

        Args:
            day_of_year (int): The day of the year for which to update the models.
        """
        self.color_model.update_senescence(day_of_year)
        self.fall_model.update_senescence(day_of_year)

    def draw_tree(self, x, y, day_of_year, show_fall = False):
        """
        Draws the tree on the screen at the specified coordinates for a given day of the year.

        Args:
            x (int): The x-coordinate of the top-left corner of the tree.
            y (int): The y-coordinate of the top-left corner of the tree.
            day_of_year (int): The day of the year for which to draw the tree.
            show_fall (bool): Optional whether to show leaf falling. Defaults to True.
        """
        # Radius of leaves in tree
        radius = 30

        # Width and height of tree trunk
        width = 20
        height = 40

        # Color and fallen normalized values
        color = self.color_model.sen_norm[day_of_year - 1]
        fallen = self.fall_model.sen_norm[day_of_year - 1]

        # Draw the tree trunk
        pg.draw.rect(self.screen, (139, 69, 19), (x, y, width, height))

        # Create a target rectangle and surface
        target_rect = pg.Rect((x + width // 2, y), (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)

        # Draw circle (for leaves) and blit onto surface so that alpha value can change
        pg.draw.circle(shape_surf, h.scale_color(color, fallen, show_fall),
                       (radius, radius), radius)
        self.screen.blit(shape_surf, target_rect)
