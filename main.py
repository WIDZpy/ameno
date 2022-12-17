import numpy as np

from simulations.gameOfLife import main as simulation


def main():
	simulation.simu.simulation.draw_array(np.ones((10, 10)))
	simulation.simu.mainloop()


if __name__ == '__main__':
	main()

