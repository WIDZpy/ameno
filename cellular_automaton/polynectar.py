import colorama as co
import pygame as pg
from simulations.gol import maraudersMap
from cellular_automaton import aparecium, mandragore as uti, maraudersMap


class CellularMain:
	def __init__(self,
				 color1: tuple[int, int, int] = (255, 255, 255),
				 color2: tuple[int, int, int] = (0, 0, 0),
				 color3: tuple[int, int, int] = (30, 30, 30),
				 ):

		pg.init()

		self.pg_win = aparecium.Win(color2, color1)
		self.simulation = maraudersMap.Automaton((2 ** 7, 2 ** 7), max_historic=2000)
		self.clock = pg.time.Clock()
		self.menu = aparecium.MenuContextuele(self.pg_win.win, 7, 20, color3)
		self.data_display = aparecium.DataDisplay(color=uti.invertion_colorimetrique(color3), bgcolor=color3)

		self.main_loop_condition = True
		self.edit_mod = False
		self.affiche_info = True

		self.pg_win.racoursit['play/pause'] = self.play_pause_
		self.pg_win.racoursit['next'] = self.next_
		self.pg_win.racoursit['prev'] = self.prev_
		self.pg_win.racoursit['restart'] = self.restart_

		self.menu.add_sections([[['textures/buttons/prev.png', 'prev', self.prev_, 'ctl + <-'],
								 ['textures/actions/play.png', 'play', self.play_pause_, 'space'],
								 ['textures/buttons/next.png', 'next', self.next_, 'ctl + ->'],
								 ['textures/buttons/turnCCW.png', 'reset', self.restart_, "ctl + <"]],
								[['textures/buttons/chek.png', 'info', self.afiche_info_, ""],
								 ['textures/buttons/void.png', 'edit mod', self.edit_mod_, ""], ]])

	def play_pause_(self):
		if not self.simulation.run:
			self.simulation.play()
			self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/pause.png', name='pause')
		else:
			self.simulation.pause()
			self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play')

	def prev_(self):
		self.simulation.back()

	def next_(self):
		self.simulation.evolve()

	def edit_(self):
		self.edit_mod = not self.edit_mod

	def restart_(self):
		self.simulation.pause()
		self.menu.section_lst[0].option_lst[1].set_caracteristic(image='textures/actions/play.png', name='play')
		self.simulation.load_historic(0)
		del self.simulation.historic[1:]
		self.pg_win.reset_cam()

	def afiche_info_(self):
		self.affiche_info = not self.affiche_info
		if self.affiche_info:
			self.menu.section_lst[1].option_lst[0].set_caracteristic(image='textures/buttons/chek.png')
		else:
			self.menu.section_lst[1].option_lst[0].set_caracteristic(image='textures/buttons/void.png')

	def edit_mod_(self):
		self.edit_mod = not self.edit_mod
		if self.edit_mod:
			self.menu.section_lst[1].option_lst[1].set_caracteristic(image='textures/buttons/chek.png')
		else:
			self.menu.section_lst[1].option_lst[1].set_caracteristic(image='textures/buttons/void.png')

	def frame(self):
		self.clock.tick(60)

		self.pg_win.key_bord_input()
		if self.affiche_info:
			self.data_display.draw(self.pg_win.win)

		arr = self.simulation.get_curent_gen(True)

		self.pg_win.set_array_pos(*self.simulation.array_pos)

		self.pg_win.aparecium(arr)

		self.menu.menu_clasic_comportement_right_clic()

		self.data_display.update_data({
			"génération": self.simulation.count,
			"fps": round(self.clock.get_fps()),
			"viventes": self.simulation.current_gen.sum(),
			"taile": self.simulation.shape,
		})

		# print("\r", self.pg_win.log('fps', clock), end='')
		self.pg_win.log_var = ''

		if pg.event.get(pg.QUIT):
			print("\n", co.Fore.RED + "END", sep='', end='')
			self.main_loop_condition = False
		pg.display.update()

	def mainloop(self):

		self.pg_win.set_array_pos(*self.simulation.array_pos)

		while self.main_loop_condition:
			self.frame()


if __name__ == '__main__':
	import numpy as np
	A = CellularMain()
	A.simulation.draw_array(np.ones((5, 6)), (10, 10))
	A.mainloop()
