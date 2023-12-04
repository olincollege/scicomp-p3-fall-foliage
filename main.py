from tree import Tree_View
import pygame as pg
import time
import datetime as dt

pg.init()

DISPLAY=pg.display.set_mode((500,400),0,32)

red_maple = Tree_View("ACRU", 2010, DISPLAY)
sugar_maple = Tree_View("ACSA", 2010, DISPLAY)
white_oak = Tree_View("QUAL", 2010, DISPLAY)
red_oak = Tree_View("QURU", 2010, DISPLAY)

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pg.font.SysFont("Calibri", 15)

for doy in range(200, 366):
    red_maple.update(doy)
    sugar_maple.update(doy)
    white_oak.update(doy)
    red_oak.update(doy)

    DISPLAY.fill((255, 255, 255))

    red_maple.draw_tree(50, 350, doy)
    red_oak.draw_tree(100, 350, doy)
    sugar_maple.draw_tree(150, 350, doy)
    red_oak.draw_tree(200, 350, doy)
    sugar_maple.draw_tree(250, 350, doy)
    red_maple.draw_tree(300, 350, doy)
    sugar_maple.draw_tree(350, 350, doy)
    red_oak.draw_tree(400, 350, doy)
    red_oak.draw_tree(450, 350, doy)

    red_oak.draw_tree(50, 250, doy)
    sugar_maple.draw_tree(100, 250, doy)
    red_maple.draw_tree(150, 250, doy)
    red_maple.draw_tree(200, 250, doy)
    sugar_maple.draw_tree(250, 250, doy)
    red_oak.draw_tree(300, 250, doy)
    sugar_maple.draw_tree(350, 250, doy)
    white_oak.draw_tree(400, 250, doy)
    red_maple.draw_tree(450, 250, doy)

    sugar_maple.draw_tree(50, 150, doy)
    red_maple.draw_tree(100, 150, doy)
    red_oak.draw_tree(150, 150, doy)
    white_oak.draw_tree(200, 150, doy)
    red_maple.draw_tree(250, 150, doy)
    sugar_maple.draw_tree(300, 150, doy)
    red_maple.draw_tree(350, 150, doy)
    red_oak.draw_tree(400, 150, doy)
    white_oak.draw_tree(450, 150, doy)
    
    red_maple.draw_tree(190, 50, doy)
    sugar_maple.draw_tree(260, 50, doy)
    white_oak.draw_tree(330, 50, doy)
    red_oak.draw_tree(400, 50, doy)

    date_now = dt.datetime(2010, 1, 1) + dt.timedelta(doy - 1)
    # render text
    label = myfont.render(date_now.strftime("%B %d"), 0, (0, 0, 0))
    DISPLAY.blit(label, (20, 20))
    time.sleep(0.1)

    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
    pg.display.flip()

