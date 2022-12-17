from dataclasses import dataclass
import pygame as pg
import numpy as np
import random as rnd
import math
'''
util function
'''


def ceil_floor(x):
    if x > 0:
        x = math.ceil(x)
    else:
        x = math.floor(x)
    return x


def var_name(var, dir):
    return [key for key, val in dir.items() if id(val) == id(var)]


def lumos(w, h):
    # World = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    World = np.array([0])
    World.resize(w, h)
    for x in range(w):
        for y in range(h):
            World[x][y] = rnd.randint(0, 1)
    return World


def clamp(var, low=None, high=None):
    out = var
    if high is not None:
        if var > high:
            out = high
    if low is not None:
        if var < low:
            out = low
    return out


def cluster():
    pass


def switch(var):
    return 1 - var


def readRLE(filename, c_shape=(50, 50)):
    '''la fonction qui permet de lire les rle'''
    if filename == 1:
        return np.zeros(c_shape).astype(int)
    filename = "simulations/gol/rle/" + filename + ".rle"
    f = open(filename, "r")
    s = ''
    while True:
        ligne = f.readline()

        if ligne == '':  # Empty indicates end of file. An empty line would be '\n'
            break

        if ligne[0] == '#':
            continue

        if ligne[0] == 'x':
            continue

        s = s + ligne[:-1]  # To remove EOL
    s = s + '$' if s[-1] != '$' else ''
    f.close()

    # curX, curY = 0, 0

    colone = np.array([[]]).astype(int)
    line = np.zeros(colone.shape[-1]).astype(int)
    coef = ""
    q = 1

    for loop in s:

        if loop == '':  # End of file
            break

        if loop == '$':

            q = 1 if coef == '' else int(coef)

            while int(colone.shape[-1]) < int(line.shape[-1]):
                colone = np.hstack((colone, np.zeros((colone.shape[0] if colone.shape[0] != 0 else 1, 1)).astype(int)))

            while int(colone.shape[-1]) > int(line.shape[-1]):
                line = np.hstack((line, [0]))

            for nn in range(q):
                colone = np.vstack((colone, line))
                line = np.zeros(colone.shape[-1]).astype(int)

            # reset line
            line = np.array([]).astype(int)
            coef = ""

        if 47 < ord(str(loop)) < 58:
            coef = coef + str(loop)

        if loop == 'b' or loop == 'o':
            q = 1 if coef == '' else int(coef)

            for i in range(q):
                line = np.hstack((line, [0 if loop == 'b' else 1]))

            coef = ''

    return colone[1:]


def invertion_colorimetrique(c):
    return ((255 - np.array(c)) % 255).tolist()


def get_coordinates(array, valu=1):
    return np.array(np.where(array == valu)).tolist()


def neightbor_array(ar: np.array):
    sets = np.pad(ar, np.ones((2, 2)).astype(int) * 2)

    return (sets[:-2, :-2] + sets[:-2, 1:-1] + sets[:-2, 2:] + sets[1:-1, :-2] +
             sets[1:-1, 2:] + sets[2:, :-2] + sets[2:, 1:-1] + sets[2:, 2:])


