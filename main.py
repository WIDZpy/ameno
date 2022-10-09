import numpy as np
import pygame as pg
import maraudersMap
# import lemon_drop as tk_win
import aparecium
from matplotlib.pyplot import imshow, show

pg_win = aparecium.Win()
game_of_life = maraudersMap.Life((2 ** 6, 2 ** 6))
menu = aparecium.Menu_contextuele()

def func():
	print('eaeaefzekfjzef,kzjek,kfk,k,ks,kg,kr,k,e,')

def play():
	game_of_life.pause()
	menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/pause.png', name='pause', fonction=pause)

def pause():
	game_of_life.pause()
	menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play', fonction=play)

def main():
	global pg_win, game_of_life, menu

	menu.add_sections([[['textures/buttons/prev.png', 'prev', func, ''], ['textures/actions/pause.png', 'pause', pause, ''],
						['textures/buttons/next.png', 'next', func, '']], [['textures/actions/pause.png', 'pause', func, '']]])

	temporaire_var =None

	pg.init()
	clock = pg.time.Clock()
	frameCount = 0
	program_run = True
	pg_win.show()
	# game_of_life.draw_adapt('canadagoose', (12, 22), rotation=2)
	game_of_life.draw_random()
	while program_run:
		clock.tick(60)
		print(clock)
		print(game_of_life.global_shape)
		if clock.get_fps() < 10 and temporaire_var is None and frameCount > 15:
			temporaire_var = np.copy(game_of_life.global_current_life)
			imshow(temporaire_var)
			show()

		if pg.event.get(pg.QUIT):
			program_run = False


		pg_win.aparecium(game_of_life.getlife())
		menu.menu_clasic_comportement_right_clic(pg_win.win, 5, 20, (30, 30, 30))
		pg.display.update()
		# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
		# print(pg_win.log())
		pg_win.log_var = ''
		# if pg_win.run

		game_of_life.evolve()
		frameCount += 1





if __name__ == '__main__':
	main()
