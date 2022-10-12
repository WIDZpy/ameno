# import numpy as np
# import lemon_drop as tk_win
# from matplotlib.pyplot import imshow, show
import pygame as pg
from GOL import maraudersMap
import aparecium


class GameOfLife:
	def __init__(self):
		self.pg_win = aparecium.Win()
		self.game_of_life = maraudersMap.Life((2 ** 6, 2 ** 6))
		self.menu = aparecium.Menu_contextuele()
		self.edit_mod = False

	def void_(self):
		return

	def play_(self):
		self.game_of_life.play()
		self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/pause.png', name='pause', fonction=self.pause_)

	def pause_(self):
		self.game_of_life.pause()
		self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play', fonction=self.play_)

	def prev_(self):
		return

	def next_(self):
		self.game_of_life.evolve()

	def edit_(self):

		self.edit_mod = not self.edit_mod

	def main(self):
		self.menu.add_sections([[['../textures/buttons/prev.png', 'prev', self.prev_, ''], ['textures/actions/play.png', 'play', self.play_, ''],
							['textures/buttons/next.png', 'next', self.next_, '']]])

		pg.init()
		clock = pg.time.Clock()
		frame_count = 0
		program_run = True
		self.pg_win.show()
		# game_of_life.draw_adapt('canadagoose', (12, 22), rotation=2)
		self.game_of_life.draw_random()
		while program_run:
			clock.tick(60)
			print('\r', clock, self.game_of_life.global_shape, end='')
			if pg.event.get(pg.QUIT):
				program_run = False

			self.pg_win.aparecium(self.game_of_life.get_life(True))
			self.menu.menu_clasic_comportement_right_clic(self.pg_win.win, 5, 20, (30, 30, 30))
			pg.display.update()
			# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
			# print(pg_win.log())
			self.pg_win.log_var = ''
			# if pg_win.run

			frame_count += 1


if __name__ == '__main__':
	GOL = GameOfLife()
	GOL.main()
