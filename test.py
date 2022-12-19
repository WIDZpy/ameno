import time

import pygame as pg
import cellular_automaton.temporaire_menucontextuele_V2 as za


def func():
	print("ferkjk")

pg.init()

c = pg.time.Clock()

win = pg.display.set_mode((500, 500), pg.SRCALPHA)
m = za.MenuContextuele((255, 0, 0), win, menu_contenue=[[['textures/buttons/void.png', 'point and clic', func, '12646'],
														['textures/buttons/void.png', 'point and clic', func, '12646']],
													   [['textures/buttons/void.png', 'point and clic', func, '12646'],
														['textures/buttons/void.png', 'point and clic', func, '12646']]
													   ])


x = 0



while True:

	if pg.event.get(pg.QUIT):
		break

	c.tick(20)

	m.menu_clasic_comportement_right_clic()
	pg.display.update()
	win.fill((0, 0, 0))

	x += 1

