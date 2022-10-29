# import numpy as np
# import lemon_drop as tk_win
# from matplotlib.pyplot import imshow, show
import pygame as pg
from simulation.gol import maraudersMap
import aparecium


class GameOfLife:
	def __init__(self):
		self.pg_win = aparecium.Win()
		self.game_of_life = maraudersMap.Life((2 ** 7, 2 ** 7))
		self.menu = aparecium.MenuContextuele(self.pg_win.win, 5, 20, (30, 30, 30))
		self.edit_mod = False
		self.touche = None

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

	def key_bord_input(self):
		speed = 1
		pressed = pg.key.get_pressed()
		key_event = pg.event.get(pg.KEYDOWN)
		self.pg_win.log("touche", self.touche)

		if len(key_event) == 0 and not (pressed[pg.K_LCTRL] or pressed[pg.K_LALT]):

			if pressed[pg.K_RIGHT]:
				self.pg_win.moov(speed)
				self.touche = "→"

			if pressed[pg.K_LEFT]:
				self.pg_win.moov(-speed)
				self.touche = "←"

			if pressed[pg.K_UP]:
				self.pg_win.moov(0, -speed)
				self.touche = "↑"

			if pressed[pg.K_DOWN]:
				self.pg_win.moov(0, speed)
				self.touche = "↓"

		for key in key_event:
			# print(key)
			if key.unicode == ' ':
				self.touche = "space"
				if self.game_of_life.run:
					self.pause_()
				else:
					self.play_()

			if key.scancode == 79:  # fleche de droite
				if pressed[pg.K_LCTRL]:
					self.next_()
					self.touche = "ctl + →"

				if pressed[pg.K_LALT]:
					self.pg_win.moov(10)
					self.touche = "alt + →"

			if key.scancode == 80:
				if pressed[pg.K_LCTRL]:
					self.prev_()
				if pressed[pg.K_LALT]:
					self.pg_win.moov(-10)
					self.touche = "alt + ←"

			if key.scancode == 82:
				if pressed[pg.K_LCTRL]:
					self.pg_win.zoom(-5)
					self.touche = "ctl + ↑"
				if pressed[pg.K_LALT]:
					self.pg_win.moov(0, -10)
					self.touche = "alt + ↑"

			if key.scancode == 81:
				if pressed[pg.K_LCTRL]:
					self.pg_win.zoom(5)
					self.touche = "ctl + ↓"
				if pressed[pg.K_LALT]:
					self.pg_win.moov(0, 10)
					self.touche = "alt + ↓"

	def mainloop(self):

		self.menu.add_sections([[['textures/buttons/prev.png', 'prev', self.prev_, ''],
								 ['textures/actions/play.png', 'play', self.play_, ''],
								 ['textures/buttons/next.png', 'next', self.next_, '']]])

		pg.init()
		clock = pg.time.Clock()
		frame_count = 0
		program_run = True

		# self.game_of_life.point_and_clic((1,0))
		# self.game_of_life.draw_adapt('canadagoose', (12, 22), rotation=0)
		self.game_of_life.draw_random()
		while program_run:
			self.pg_win.log()
			clock.tick(60)

			if pg.event.get(pg.QUIT):
				program_run = False
			self.key_bord_input()
			arr = self.game_of_life.get_life(True)
			# self.pg_win.set_decalage(self.game_of_life.bordure[0][0], self.game_of_life.bordure[1][0])
			self.pg_win.aparecium()

			self.menu.menu_clasic_comportement_right_clic()
			pg.display.update()
			# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
			print("\r", self.pg_win.log('fps', clock), end='')
			self.pg_win.log_var = ''
			# if pg_win.run

			frame_count += 1


if __name__ == '__main__':
	GOL = GameOfLife()
	GOL.mainloop()
