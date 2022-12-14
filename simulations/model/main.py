from cellular_automaton import polynectar, aparecium, maraudersMap


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
		return


class Display(aparecium.Win):
	def __init__(self):
		super(Display, self).__init__()


simu = Main()