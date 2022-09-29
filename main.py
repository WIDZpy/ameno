import numpy as np
import pygame as pg
from time import *
# import lemon_drop as tk_win
import aparecium
import numpy

def func():
	print('eaeae')


if __name__ == '__main__':
	pg_win = aparecium.Win()
	menu = aparecium.Menu_contextuele([[['textures/actions/pause.png', 'pause', func, ''], ['textures/actions/pause.png', 'pause', func, '']],[['textures/actions/pause.png', 'pause', func, ''],['textures/actions/pause.png', 'pause', func, '']]])
	pg.init()
	clock = pg.time.Clock()
	frameCount = 0
	program_run = True
	pg_win.show()

	while program_run:
		clock.tick(60)

		if pg.event.get(pg.QUIT):
			program_run = False
		pg_win.aparecium()
		menu.menu_clasic_comportement_right_clic(pg_win.win, 5, 20, (30, 30, 30))
		pg.display.update()
		# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
		# print(pg_win.log())
		pg_win.log_var = ''
	#	if pg_win.run
