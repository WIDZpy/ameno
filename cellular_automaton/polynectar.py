import colorama as co
import pygame as pg
from cellular_automaton import aparecium, mandragore as uti, maraudersMap


class CellularMain:
	def __init__(self,
				 pg_win=aparecium.Win(),
				 simulation=maraudersMap.Automaton(),
				 color1: tuple[int, int, int] = (255, 255, 255),
				 color2: tuple[int, int, int] = (0, 0, 0),
				 color3: tuple[int, int, int] = (30, 30, 30)):

		pg.init()

		self.pg_win = pg_win
		self.simulation = simulation
		self.clock = pg.time.Clock()
		self.data_display = aparecium.DataDisplay(color=uti.invertion_colorimetrique(color3), bgcolor=color3)

		self.main_loop_condition = True
		self.edit_mod = False
		self.affiche_info = True

		self.pg_win.set_color(color2, color1)

		self.pg_win.racoursit['play/pause'] = self.play_pause_
		self.pg_win.racoursit['next'] = self.next_
		self.pg_win.racoursit['prev'] = self.prev_
		self.pg_win.racoursit['restart'] = self.restart_

		self.edit_menu = aparecium.MenuContextuele(color3, self.pg_win.win,
												   [[['textures/buttons/void.png', 'point and clic', self.active_point_clic_, '']],
													[['textures/buttons/chek.png', 'info', self.afiche_info_, ""],
													 ['textures/buttons/chek.png', 'edit mod', self.edit_mod_, ""], ]], 7, 20)

		self.run_menu = aparecium.MenuContextuele(color3, self.pg_win.win,
												  [[['textures/buttons/prev.png', 'prev', self.prev_, 'ctl + <-'],
													['textures/actions/play.png', 'play', self.play_pause_, 'space'],
													['textures/buttons/next.png', 'next', self.next_, 'ctl + ->'],
													['textures/buttons/turnCCW.png', 'reset', self.restart_, "ctl + <"]],
												   [['textures/buttons/chek.png', 'info', self.afiche_info_, ""],
													['textures/buttons/void.png', 'edit mod', self.edit_mod_, ""], ]], 7, 20)

	def active_point_clic_(self):
		pass

	def play_pause_(self):
		if not self.simulation.run:
			self.simulation.play()
			self.run_menu.set_obtion(0, 1, image='textures/actions/pause.png', name='pause')
		else:
			self.simulation.pause()
			self.run_menu.set_obtion(0, 1, image='textures/actions/play.png', name='play')

	def prev_(self):
		self.simulation.back()

	def next_(self):
		self.simulation.evolve()

	def edit_(self):
		self.simulation.pause()
		self.edit_mod = not self.edit_mod

	def restart_(self):
		self.simulation.pause()
		self.run_menu.set_obtion(0, 1, image='textures/actions/play.png', name='play')
		self.simulation.load_historic(0)
		del self.simulation.historic[1:]
		self.pg_win.reset_cam()

	def afiche_info_(self):
		self.affiche_info = not self.affiche_info
		if self.affiche_info:
			self.edit_menu.set_obtion(1, 0, image='textures/buttons/chek.png')
			self.run_menu.set_obtion(1, 0, image='textures/buttons/chek.png')
		else:
			self.edit_menu.set_obtion(1, 0, image='textures/buttons/void.png')
			self.run_menu.set_obtion(1, 0, image='textures/buttons/void.png')

	def edit_mod_(self):
		self.edit_mod = not self.edit_mod
		if self.edit_mod:
			self.run_menu.afiche = False
		else:
			self.edit_menu.afiche = False


	def frame(self):
		self.clock.tick(60)

		self.pg_win.input()

		arr = self.simulation.get_curent_gen(True)

		self.pg_win.set_array_pos(*self.simulation.array_pos)

		self.pg_win.aparecium(arr, self.edit_mod)

		if self.edit_mod:
			self.edit_menu.menu_clasic_comportement_right_clic()
		else:
			self.run_menu.menu_clasic_comportement_right_clic()

		self.data_display.update_data({
			"génération": self.simulation.count,
			"fps": round(self.clock.get_fps()),
			"viventes": self.simulation.current_gen.sum(),
			"taile": self.simulation.shape,

		})

		if self.affiche_info:
			self.data_display.draw(self.pg_win.win)

		# print("\r", self.pg_win.log('fps', self.clock), end='')
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
