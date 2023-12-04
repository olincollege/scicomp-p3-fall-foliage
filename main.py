"""
Main code run to display the changing color of leaves
"""

import time
import datetime as dt
import pygame as pg
from tree import TreeView

# Initialize pygame, create display
pg.init()
DISPLAY = pg.display.set_mode((500,400),0,32)

# Define view objects for three tree species
red_maple = TreeView("ACRU", 2010, DISPLAY)
sugar_maple = TreeView("ACSA", 2010, DISPLAY)
white_oak = TreeView("QUAL", 2010, DISPLAY)
red_oak = TreeView("QURU", 2010, DISPLAY)

# Initialize Font
my_font = pg.font.SysFont("Calibri", 15)

# Loop through each day from end July until December
for doy in range(200, 366):
    # Update the senescence values based on the day of the year
    red_maple.update(doy)
    sugar_maple.update(doy)
    white_oak.update(doy)
    red_oak.update(doy)

    # Wipe clean the display
    DISPLAY.fill((255, 255, 255))

    # Draw bottom row of trees
    red_maple.draw_tree(50, 350, doy)
    red_oak.draw_tree(100, 350, doy)
    sugar_maple.draw_tree(150, 350, doy)
    red_oak.draw_tree(200, 350, doy)
    sugar_maple.draw_tree(250, 350, doy)
    red_maple.draw_tree(300, 350, doy)
    sugar_maple.draw_tree(350, 350, doy)
    red_oak.draw_tree(400, 350, doy)
    red_oak.draw_tree(450, 350, doy)

    # Draw middle row of trees
    red_oak.draw_tree(50, 250, doy)
    sugar_maple.draw_tree(100, 250, doy)
    red_maple.draw_tree(150, 250, doy)
    red_maple.draw_tree(200, 250, doy)
    sugar_maple.draw_tree(250, 250, doy)
    red_oak.draw_tree(300, 250, doy)
    sugar_maple.draw_tree(350, 250, doy)
    white_oak.draw_tree(400, 250, doy)
    red_maple.draw_tree(450, 250, doy)

    # Draw third row of trees
    sugar_maple.draw_tree(50, 150, doy)
    red_maple.draw_tree(100, 150, doy)
    red_oak.draw_tree(150, 150, doy)
    white_oak.draw_tree(200, 150, doy)
    red_maple.draw_tree(250, 150, doy)
    sugar_maple.draw_tree(300, 150, doy)
    red_maple.draw_tree(350, 150, doy)
    red_oak.draw_tree(400, 150, doy)
    white_oak.draw_tree(450, 150, doy)

    # Draw top row, one tree of each species
    red_maple.draw_tree(190, 50, doy)
    sugar_maple.draw_tree(260, 50, doy)
    white_oak.draw_tree(330, 50, doy)
    red_oak.draw_tree(400, 50, doy)

    # Get the date based on day of the year
    date_now = dt.datetime(2010, 1, 1) + dt.timedelta(doy - 1)
    # Print the date
    label = my_font.render(date_now.strftime("%B %d"), 0, (0, 0, 0))
    DISPLAY.blit(label, (20, 20))

    # Pause
    time.sleep(0.1)

    # Check for user input
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
    pg.display.flip()
