import simulation.gol.gol_main as game_of_life

simu = None


def init_gol():
	global simu
	simu = game_of_life.GameOfLife()

