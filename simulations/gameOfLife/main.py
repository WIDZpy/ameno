from cellular_automaton import polynectar, aparecium, maraudersMap, mandragore
import numpy as np
import pygame as pg


class Main(polynectar.CellularMain):
	def __init__(self):
		super(Main, self).__init__(Display(), Logic())
		self.simulation.draw_array(np.pad(np.array([[1,1,1], [1,0,1], [1,1,1]]), [[10,10],[10,10]]))

	def mainloop(self):
		while self.main_loop_condition:
			self.frame()


class Logic(maraudersMap.Automaton):
	def __init__(self):
		super(Logic, self).__init__()

	def evolve(self):
		if self.current_gen.sum():
			self.count += 1
			neigh = mandragore.neightbor_array(self.current_gen)
			self.current_gen = np.logical_or(neigh == 3, np.pad(np.logical_and(self.current_gen == 1, neigh[1:-1, 1:-1] == 2), [[1, 1], [1, 1]])).astype(int)
			self.array_pos[0] -= 1
			self.array_pos[1] -= 1
			self.shape = list(self.current_gen.shape)

			self.crop_gen()

			self.add_histoic()


class Display(aparecium.Win):
	def __init__(self):
		super(Display, self).__init__()


simu = Main()
