from math import *
import numpy as np
import pygame.image
# import maraudersMap as backend

import pygame as pg
import mandragore

'''réorganisation'''


class Win:
	def __init__(self):
		self.window_caracteristique = {
			'title': "John Conway's Game of Life",
			'length side': (2 ** 9, 2 ** 9),
			'size of cells': 2 ** 9 // 2 ** 6,
			'active border': False,
			'border': 4,
			'pading': 3,

		}

		if not self.window_caracteristique['active border']:
			self.window_caracteristique['border'] = 0

		self.win = pg.display.set_mode((self.window_caracteristique['length side'][0] + self.window_caracteristique['border'] * 2,
										self.window_caracteristique['length side'][1] + self.window_caracteristique['border'] * 2), pg.RESIZABLE)
		self.winPrevMousePos = pg.mouse.get_pos()
		pg.display.set_icon(pygame.image.load('textures/logo.png'))
		pg.display.set_caption(self.window_caracteristique['title'])
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

		self.camX = 0
		self.camY = 0
		self.CellClr = (255, 255, 255)
		self.BgClr = (0, 0, 0)
		self.log_var = ''
		self.decalage = 0, 0
		return

	def set_decalage(self, x, y):
		self.decalage = x, y

	def log(self, *info):

		self.log_var += "".join([f'{" | " if i % 2 == 0 else ": "}{info[i]}' for i in range(len(info))])
		return self.log_var

	def aparecium(self, world=np.array([[1, 0, 1], [1, 1, 1], [1, 0, 1]])):
		"""
		fiche un array dans la fenêtre pygame
		:param world: l'array a afficher dans la fenêtre pygame
		"""

		world_size = world.shape

		self.win.fill(self.BgClr)

		dec_y = self.camY + self.decalage[0] * self.window_caracteristique['size of cells']
		dec_x = self.camX + self.decalage[1] * self.window_caracteristique['size of cells']

		view = world[mandragore.clamp(dec_y // self.window_caracteristique['size of cells'], 0, world_size[0]):
					 mandragore.clamp(ceil(dec_y / self.window_caracteristique['size of cells']) + ceil(self.window_caracteristique['length side'][1] / self.window_caracteristique['size of cells']),
									  0, world_size[0]),
			   mandragore.clamp(dec_x // self.window_caracteristique['size of cells'], 0, world_size[1]):
			   mandragore.clamp(ceil(dec_x / self.window_caracteristique['size of cells']) + ceil(self.window_caracteristique['length side'][0] / self.window_caracteristique['size of cells']), 0,
								world_size[1])]

		view_cordantate = np.array(np.where(view == 1)).tolist()

		decalage_x = dec_x % self.window_caracteristique['size of cells'] if dec_x > 0 else dec_x
		decalage_y = dec_y % self.window_caracteristique['size of cells'] if dec_y > 0 else dec_y

		print("size of cell : ", self.window_caracteristique['size of cells'], "decalage :", decalage_x, "dec", dec_x)

		for cy, cx in zip(*view_cordantate):

			pg.draw.rect(self.win, self.CellClr, (cx * self.window_caracteristique['size of cells'] + self.window_caracteristique['border'] - decalage_x,
												  cy * self.window_caracteristique['size of cells'] + self.window_caracteristique['border'] - decalage_y,
												  self.window_caracteristique['size of cells'], self.window_caracteristique['size of cells']))

		if self.window_caracteristique['active border']:
			self.edgeBorders(world.shape)

		return

	def edgeBorders(self, world_shape):
		# revoir le comportement des bordure dans le cas d'un désoume
		return

	def moov(self, x=0, y=0):
		self.camX += x
		self.camY += y

	def zoom(self, z):
		self.window_caracteristique['size of cells'] = mandragore.clamp(self.window_caracteristique['size of cells'] + z, 1)


class MenuContextuele:
	rectangle = [0, 0, 0, 0]
	padding = 5

	def __init__(self, surface, width, size, color, menu_contenue=[]):

		self.surface = surface
		self.width = width
		self.size = size
		self.color = color

		self.section_lst = []
		self.add_sections(menu_contenue)
		self.afiche = False
		self.menu_surface = None

	def add_sections(self, menu_contenue):
		for section in menu_contenue:
			self.section_lst.append(self.Section(section, self.width, self.size, self.color))
		return

	def menu_clasic_comportement_right_clic(self):

		souris_event_up = pg.event.get(pg.MOUSEBUTTONUP)

		if souris_event_up:
			souris_event_up = souris_event_up[0]

			if souris_event_up.button == 3 and not pg.rect.Rect(self.rectangle).collidepoint(souris_event_up.pos):
				self.afiche = True
				self.rectangle[:2] = souris_event_up.pos

			elif souris_event_up.button == 1 and not pg.rect.Rect(self.rectangle).collidepoint(souris_event_up.pos):
				self.afiche = False

		if self.afiche:
			self.show_menue(self.surface, self.rectangle[0:2].copy(), self.width, self.size, self.color)
			if pg.rect.Rect(self.rectangle).collidepoint(pg.mouse.get_pos()):
				pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
			else:
				pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)
		else:
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

	def show_menue(self, surface, pos, width, size, color):

		pos = tuple(pos)
		self.menu_surface = pg.Surface(surface.get_size(), pg.SRCALPHA).convert_alpha()

		self.rectangle[2] = self.padding
		self.rectangle[3] = self.padding
		self.rectangle[0:2] = pos

		for section in self.section_lst:
			section.show_section(self.menu_surface, self.rectangle, width, size, color, section != self.section_lst[0])

		self.rectangle[2] += width * size
		self.rectangle[2] += self.padding
		self.rectangle[3] += 1 + self.padding
		pg.draw.rect(surface, (np.array((mandragore.invertion_colorimetrique(color)) + np.array(color)) / 2).tolist(), self.rectangle)
		pg.draw.rect(surface, color, (self.rectangle[0] + 1, self.rectangle[1] + 1, self.rectangle[2] - 2, self.rectangle[3] - 2))
		surface.blit(self.menu_surface, (0, 0))
		# self.rectangle = [0,0,0,0]
		return

	class Section:
		def __init__(self, options, width, size, color):
			self.option_lst = []
			self.add_options(options, width, size, color)

		def add_options(self, options, width, size, color):
			for option in options:
				self.option_lst.append(self.Option(*option, width, size, color))

		def show_section(self, surface, rect, width, size, color, line=True):
			if line:
				rect[3] += 4
				pg.draw.line(surface, mandragore.invertion_colorimetrique(color), (rect[0] + rect[2], rect[1] + rect[3]), (rect[0] + rect[2] + width * size, rect[1] + rect[3]), 1)
				rect[3] += 4 + 1

			for option in self.option_lst:
				option.show_option(surface, rect, width, size, color)
				rect[3] += size

		class Option:
			padding_y = 1
			border_image = padding_y
			image_title = padding_y
			short_border = padding_y
			font = 'textures/SmallMemory.ttf'
			color_coef = 450

			def __init__(self, image, name, function, short, width, size, color):
				self.image = pg.image.load(image) if image != '' else ''
				self.name = name
				self.function = function
				self.short = short

				######################################################################################################################

				self.main_rect = 0, 0, 0, 0
				self.bg_color = (0, 0, 0)
				self.historry_pos = None
				self.pos = (0, 0)
				self.color = color
				self.rect = [0, 0, 0, 0]
				self.width = width
				self.size = size

				self.image_size = (0, 0)
				self.image_pos = (0, 0)

				self.font_object = None

				self.name_surf = None
				self.name_rect = None

				self.short_surf = None
				self.short_rect = None

				pg.font.init()

			def set_caracteristic(self, image=None, name=None, short=None, fonction=None):

				self.name = name if name is not None else self.name
				self.image = pg.image.load(image) if image is not None else self.image
				self.short = short if short is not None else self.short
				self.function = fonction if fonction is not None else self.function

				self.name = name if name is not None else self.name
				self.name = name if name is not None else self.name
				self.name = name if name is not None else self.name
				self.name = name if name is not None else self.name

				self.update()

			def update(self):
				self.historry_pos = self.rect[:2]

				self.bg_color = mandragore.clamp(self.color[0] - self.color[0] * self.color_coef / 100, 0, 255), \
								mandragore.clamp(self.color[1] - self.color[1] * self.color_coef / 100, 0, 255), \
								mandragore.clamp(self.color[2] + self.color[2] * self.color_coef / 100, 0, 255)

				xpos = self.border_image

				self.pos = self.rect[0] + self.rect[2], self.rect[1] + self.rect[3]
				self.main_rect = (*self.pos[:2], self.width * self.size, self.size)

				self.image_size = (self.size - 2 * self.padding_y, self.size - 2 * self.padding_y)
				self.image_pos = (self.pos[0] + xpos, self.pos[1] + self.padding_y)
				self.image = pg.transform.scale(self.image, self.image_size)

				xpos += self.size - 2 * self.padding_y + self.image_title
				# self.font_object = pg.font.Font(self.font, self.size - 2 * self.padding_y)

				self.font_object = pg.font.Font('textures/SmallMemory.ttf', 18)
				self.name_surf = self.font_object.render(self.name, True, mandragore.invertion_colorimetrique(self.color))
				self.name_rect = self.name_surf.get_rect()
				self.name_rect.center = (self.pos[0] + xpos + self.name_rect[2] / 2, self.pos[1] + self.size / 2)

				self.short_surf = self.font_object.render(self.short, True, (np.array((mandragore.invertion_colorimetrique(self.color)) + np.array(self.color)) / 2).tolist())
				self.short_rect = self.short_surf.get_rect()
				self.short_rect.center = (self.pos[0] + self.main_rect[2] - self.short_rect.size[0] / 2, self.pos[1] + self.size / 2)

			def show_option(self, surface, rect, width, size, color):
				self.rect = rect.copy()

				if rect[:2] != self.historry_pos:
					self.update()

				hillighted = False
				if pg.rect.Rect(self.main_rect).collidepoint(pg.mouse.get_pos()):
					hillighted = True

				mouse = pg.event.get(pg.MOUSEBUTTONDOWN)
				if mouse:
					mouse2 = mouse[0]
					if pg.rect.Rect(self.main_rect).collidepoint(mouse2.pos):
						self.function()
					else:
						pg.event.post(mouse2)

				bg_color = self.bg_color if hillighted else color

				pg.draw.rect(surface, bg_color, self.main_rect)

				surface.blit(self.image.convert_alpha(), self.image_pos)
				surface.blit(self.name_surf.convert_alpha(), self.name_rect)
				surface.blit(self.short_surf.convert_alpha(), self.short_rect)
