from cellular_automaton import polynectar, aparecium, maraudersMap
import numpy as np

class Main(polynectar.CellularMain):
	def __init__(self):
		super(Main, self).__init__()
		self.simulation = Logic()
		self.pg_win = Display()

	def mainloop(self):
		while self.main_loop_condition:
			self.frame()


class Logic(maraudersMap.Automaton):
	def __init__(self):
		super(Logic, self).__init__()

	def evolve(self):
		if self.global_current_life.sum():

			self.count += 1

			sets = np.pad(self.global_current_life, np.ones((2, 2)).astype(int) * 2)
			# sets = self.current_gen
			evolve = np.pad(np.zeros(self.global_shape).astype(int), np.ones((2, 2)).astype(int))
			evolve[:, :] = (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
							sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])
			evolve = np.logical_or(evolve == 3, np.logical_and(sets[1:-1, 1:-1] == 1, evolve == 2)).astype(int)

			self.bordure = (np.array(self.bordure) + 1).tolist()  # rajoute 1 a toute la valeur de self.array_pos

			for to in 'ab':
				if evolve[0].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.bordure[0][0] >= self.bordure[0][1]):  # test s'il y a une ou plusieurs cellules en vie sur la première ligne
					evolve = evolve[1:]  # retourne l'array substituer de la première lig1ne
					self.bordure[0][0] -= 1  # soustrait 1 a la valeur de la première ligne
				if evolve[-1].sum() == 0 or (self.max_x_y[0] <= evolve.shape[0] and self.bordure[0][1] >= self.bordure[0][0]):  # test s'il y a une ou plusieurs cellules en vie sur la première ligne
					evolve = evolve[:-1]  # retourne l'array substituer de la première ligne
					self.bordure[0][1] -= 1  # soustrait 1 a la valeur de la première ligne
				if evolve[:, 0].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.bordure[1][0] >= self.bordure[1][1]):  # test s'il y a une ou plusieurs cellules en vie sur la première ligne
					evolve = evolve[:, 1:]  # retourne l'array substituer de la première ligne
					self.bordure[1][0] -= 1  # soustrait 1 a la valeur de la première ligne
				if evolve[:, -1].sum() == 0 or (self.max_x_y[1] <= evolve.shape[1] and self.bordure[1][1] >= self.bordure[1][0]):  # test s'il y a une ou plusieurs cellules en vie sur dernière colonne
					evolve = evolve[:, :-1]  # retourne l'array substituer de derni ère colonne
					self.bordure[1][1] -= 1  # soustrait 1 a la valeur de la dernière colonne

			self.global_current_life = evolve.astype(int)
			# print(evolve, "\n", self.array_pos, "\n", self.restricted_shape)
			self.global_shape = self.global_current_life.shape

			if len(self.historic) >= self.max_historic:
				del self.historic[1]
			self.historic.append((self.global_current_life, self.bordure, self.global_shape, self.count))


class Display(aparecium.Win):
	def __init__(self):
		super(Display, self).__init__()


simu = Main()