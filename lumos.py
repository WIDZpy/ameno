### lumos MAXIMAAAA *lights on*

import numpy as np
import random as rnd


def lumos(w, h):
    # World = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    World = np.array([0])
    World.resize(w, h)
    for x in range(w):
        for y in range(h):
            World[x][y] = rnd.randint(0, 1)
    return World


print(lumos(4, 4))
