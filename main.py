import numpy as np
import pygame as pg
import maraudersMap
# import lemon_drop as tk_win
import aparecium


def func():
	print('eaeaefzekfjzef,kzjek,kfk,k,ks,kg,kr,k,e,')


if __name__ == '__main__':
	pg_win = aparecium.Win()
	menu = aparecium.Menu_contextuele([[['textures/buttons/prev.png', 'prev', func, ''], ['textures/actions/pause.png', 'pause', func, ''], ['textures/buttons/next.png', 'next', func, '']],[['textures/actions/pause.png', 'pause', func, '']]])
	game_of_life = maraudersMap.Life((100,100))

	pg.init()
	clock = pg.time.Clock()
	frameCount = 0
	program_run = True
	pg_win.show()
	# game_of_life.draw_adapt('canadagoose', (12, 22), rotation=2)
	game_of_life.draw_random()
	while program_run:
		clock.tick(10)


		if pg.event.get(pg.QUIT):
			program_run = False



		if True:
			menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play')

		pg_win.aparecium(game_of_life.getlife())
		menu.menu_clasic_comportement_right_clic(pg_win.win, 5, 20, (30, 30, 30))
		pg.display.update()
		# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
		# print(pg_win.log())
		pg_win.log_var = ''
		# if pg_win.run

		game_of_life.evolve()