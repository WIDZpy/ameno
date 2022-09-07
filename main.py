import pygame as pg
from time import *
# import lemon_drop as tk_win
# import aparecium as pg_win

if __name__ == '__main__':
	pg.init()
	clock = pg.time.Clock()
	frameCount = 0
	program_run = True
	while program_run:
		clock.tick(30)
		if pg.event.get(pg.QUIT):
			program_run = False
	#	if pg_win.run
