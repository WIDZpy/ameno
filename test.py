import pygame as pg
pg.init()
win = pg.display.set_mode((500,500),pg.SRCALPHA)
import cellular_automaton.temporaire_menucontextuele_V2 as a
m = a.MenuContextuele((255, 0, 0), win, menu_contenue=[[['textures/buttons/void.png', 'point and clic', "self.active_point_clic_", '12646'],
														['textures/buttons/void.png', 'point and clic', "self.active_point_clic_", '12646']],
													   [['textures/buttons/void.png', 'point and clic', "self.active_point_clic_", '12646'],
														['textures/buttons/void.png', 'point and clic', "self.active_point_clic_", '12646']]
													   ])
m.show((20,20))
pg.display.update()
input()