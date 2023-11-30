import pygame as pg
# from pyg.locals import *
# Pygame defines colors using RGB - can scale numbers by value
# Matplotlib heatmap

def main():
    pg.init()

    DISPLAY=pg.display.set_mode((500,400),0,32)

    WHITE=(255,255,255)
    GREEN=(100,150,20)
    YELLOW = (220, 170, 60)
    ORANGE = (200, 90, 40)
    RED = (160, 40, 40)

    DISPLAY.fill(WHITE)

    pg.draw.rect(DISPLAY, GREEN, (200, 50, 100, 50))
    pg.draw.rect(DISPLAY, YELLOW, (200, 100, 100, 50))
    pg.draw.rect(DISPLAY, ORANGE, (200, 150, 100, 50))
    pg.draw.rect(DISPLAY, RED, (200, 200, 100, 50))
    

    while True:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
        pg.display.update()

main()