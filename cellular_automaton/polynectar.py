import colorama as co
import pygame as pg
from simulation.gol import maraudersMap
from cellular_automaton import aparecium, mandragore as uti, maraudersMap


class CellularMain:
	def __init__(self):
		color1 = (255, 255, 255)
		color2 = (0, 0, 0)
		color3 = (30, 30, 30)
		self.pg_win = aparecium.Win(color2, color1)
		self.simulation = maraudersMap.Life((2 ** 7, 2 ** 7), max_historic=2000)
		self.menu = aparecium.MenuContextuele(self.pg_win.win, 7, 20, color3)
		self.data_display = aparecium.DataDisplay(color=uti.invertion_colorimetrique(color3), bgcolor=color3)
		self.edit_mod = False
		self.afiche_info = True

		self.pg_win.racoursit['play/pause'] = self.play_pause_
		self.pg_win.racoursit['next'] = self.next_
		self.pg_win.racoursit['prev'] = self.prev_
		self.pg_win.racoursit['restart'] = self.restart_

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

		# self.simulation.point_and_clic((1,0))
		# self.simulation.point_and_clic((0, 0))
		# self.simulation.point_and_clic((0, 1))
		# self.simulation.point_and_clic((1, 1))
		# self.simulation.point_and_clic((1, 0))
		# self.simulation.draw_adapt('canadagoose', (10, 10), rotation=2)
		# self.simulation.draw_random()
		self.simulation.draw_adapt('p5lumpsofmuckhassler', (10, 10), rotation=2)
		self.simulation.draw_adapt('lobster', (50, 50), rotation=2)

		self.pg_win.set_decalage(self.simulation.bordure[0][0], self.simulation.bordure[1][0])

		while program_run:
			clock.tick(60)

			self.pg_win.key_bord_input()
			arr = self.simulation.get_life(True)
			self.pg_win.set_decalage(self.simulation.bordure[0][0], self.simulation.bordure[1][0])
			self.pg_win.aparecium(arr)

			self.menu.menu_clasic_comportement_right_clic()

			self.data_display.update_data({
				"génération": self.simulation.count,
				"fps": round(clock.get_fps()),
				"nb de cellul": self.simulation.current_gen.sum(),
				"taile": self.simulation.shape,
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
	A = CellularMain()