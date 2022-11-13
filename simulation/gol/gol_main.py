# import numpy as np
# import lemon_drop as tk_win
# from matplotlib.pyplot import imshow, show
import colorama as co
import pygame as pg
from simulation.gol import maraudersMap
import aparecium
import mandragore as uti


class GameOfLife:
	def __init__(self):
		color1 = (255, 255, 255)
		color2 = (0, 0, 0)
		color3 = (30, 30, 30)
		self.pg_win = aparecium.Win(color2, color1)
		self.game_of_life = maraudersMap.Life((2 ** 7, 2 ** 7), max_historic=2000)
		self.menu = aparecium.MenuContextuele(self.pg_win.win, 7, 20, color3)
		self.data_display = aparecium.DataDisplay(color=uti.invertion_colorimetrique(color3), bgcolor=color3)
		self.edit_mod = False

		self.pg_win.racoursit['play/pause'] = self.play_pause_
		self.pg_win.racoursit['next'] = self.next_
		self.pg_win.racoursit['prev'] = self.prev_
		self.pg_win.racoursit['restart'] = self.restart_

	def play_pause_(self):
		if not self.game_of_life.run:
			self.game_of_life.play()
			self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/pause.png', name='pause')
		else:
			self.game_of_life.pause()
			self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play')

	def prev_(self):
		self.game_of_life.back()

	def next_(self):
		self.game_of_life.evolve()

	def edit_(self):
		self.edit_mod = not self.edit_mod

	def restart_(self):
		self.game_of_life.pause()
		self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play')
		self.game_of_life.load_historic(0)
		del self.game_of_life.historic[1:]
		self.pg_win.reset_cam()

	def mainloop(self):

		self.menu.add_sections([[['textures/buttons/prev.png', 'prev', self.prev_, 'ctl + <-'],
								 ['textures/actions/play.png', 'play', self.play_pause_, 'space'],
								 ['textures/buttons/next.png', 'next', self.next_, 'ctl + ->'],
								 ['', 'reset', self.restart_, "ctl + <"]]])

		pg.init()
		clock = pg.time.Clock()
		frame_count = 0
		program_run = True

		# self.game_of_life.point_and_clic((1,0))
		self.game_of_life.point_and_clic((0, 0))
		self.game_of_life.point_and_clic((0, 1))
		self.game_of_life.point_and_clic((1, 1))
		self.game_of_life.point_and_clic((1, 0))

		self.game_of_life.draw_adapt('canadagoose', (10, 10), rotation=2)
		# self.game_of_life.draw_random()

		self.pg_win.set_decalage(self.game_of_life.bordure[0][0], self.game_of_life.bordure[1][0])

		while program_run:
			clock.tick(60)

			self.pg_win.key_bord_input()
			arr = self.game_of_life.get_life(True)
			self.pg_win.set_decalage(self.game_of_life.bordure[0][0], self.game_of_life.bordure[1][0])
			self.pg_win.aparecium(arr)

			self.menu.menu_clasic_comportement_right_clic()

			self.data_display.update_data({
				"génération": self.game_of_life.count,
				"fps": round(clock.get_fps()),
				"nb de cellul": self.game_of_life.global_current_life.sum(),
				"taile": self.game_of_life.global_shape,
			})
			self.data_display.draw(self.pg_win.win)
			# menu.show_menue(pg_win.win, (0, 0), 12, 20, (140,140,140))
			print("\r", self.pg_win.log('fps', clock), end='')
			self.pg_win.log_var = ''
			# if pg_win.run
			frame_count += 1

			if pg.event.get(pg.QUIT):
				print("\n", co.Fore.RED + "END", sep='', end='')
				program_run = False
			pg.display.update()


if __name__ == '__main__':
	GOL = GameOfLife()
	GOL.mainloop()

