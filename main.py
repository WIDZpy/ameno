import numpy as np
import pygame as pg
from time import *
# import lemon_drop as tk_win
import aparecium
import numpy



if __name__ == '__main__':
	pg_win = aparecium.Win()
	menu = aparecium.Menu_contextuele((('pause.png', 'pause', func)))
	pg.init()
	clock = pg.time.Clock()
	frameCount = 0
	program_run = True
	pg_win.show()

	while program_run:
		clock.tick(30)
		if pg.event.get(pg.QUIT):
			program_run = False
		pg_win.aparecium()
		pg.display.update()

		print(pg_win.log())
		pg_win.log_var = ''
	#	if pg_win.run
