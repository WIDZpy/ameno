# import numpy as np
# import lemon_drop as tk_win
# from matplotlib.pyplot import imshow, showorama as co
import pygame as pg
from simulations.gol import maraudersMap
import cellular_automaton.aparecium as aparecium
import cellular_automaton.mandragore as uti


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
		self.afiche_info = True

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

	def afiche_info_(self):
		self.afiche_info = not self.afiche_info
		if self.afiche_info:
			self.menu.section_lst[1].option_lst[0].set_caracteristic(image='textures/buttons/chek.png')
		else:
			self.menu.section_lst[1].option_lst[0].set_caracteristic(image='textures/buttons/void.png')

	def edit_mod_(self):
		self.edit_mod = not self.edit_mod
		if self.edit_mod:
			self.menu.section_lst[1].option_lst[1].set_caracteristic(image='textures/buttons/chek.png')
		else:
			self.menu.section_lst[1].option_lst[1].set_caracteristic(image='textures/buttons/void.png')

	def mainloop(self):
		self.menu.add_sections([[['textures/buttons/prev.png', 'prev', self.prev_, 'ctl + <-'],
								 ['textures/actions/play.png', 'play', self.play_pause_, 'space'],
								 ['textures/buttons/next.png', 'next', self.next_, 'ctl + ->'],
								 ['textures/buttons/turnCCW.png', 'reset', self.restart_, "ctl + <"]],
								[['textures/buttons/chek.png', 'info', self.afiche_info_, ""],
								 ['textures/buttons/void.png', 'edit mod', self.edit_mod_, ''], ]])

		pg.init()
		clock = pg.time.Clock()
		frame_count = 0
		program_run = True

		# self.simulations.point_and_clic((1,0))
		# self.simulations.point_and_clic((0, 0))
		# self.simulations.point_and_clic((0, 1))
		# self.simulations.point_and_clic((1, 1))
		# self.simulations.point_and_clic((1, 0))
		# self.simulations.draw_adapt('canadagoose', (10, 10), rotation=2)
		# self.simulations.draw_random()
		self.game_of_life.draw_adapt('spacefiller1', (10, 10), rotation=2)
		self.game_of_life.draw_adapt('lobster', (80, 80), rotation=2)

		self.pg_win.set_decalage(self.game_of_life.bordure[0][0], self.game_of_life.bordure[1][0])

		while program_run:
			clock.tick(60)

			self.pg_win.input()
			arr = self.game_of_life.get_life(True)
			self.pg_win.set_decalage(self.game_of_life.bordure[0][0], self.game_of_life.bordure[1][0])
			self.pg_win.aparecium(arr)

			self.menu.menu_clasic_comportement_right_clic()

			self.data_display.update_data({
				"génération": self.game_of_life.count,
				"fps": round(clock.get_fps()),
				"nb de cellul": self.game_of_life.global_current_life.sum(),
				"taile": self.game_of_life.global_shape,
				'array_pos': self.game_of_life.bordure,
			})
			if self.afiche_info:
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
