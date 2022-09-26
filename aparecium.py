from math import *
import numpy as np
import pygame.image
import maraudersMap as backend
import pygame as pg
import mandragore

'''réorganisation'''


class Win:
	def __init__(self):
		self.window_caracteristique = {
			'title': "John Conway's Game of Life",
			'definition': 2 ** 6,
			'length side': 2 ** 9,
			'active border': True,
			'border': 4,

		}
		self.window_caracteristique['size of cells'] = int(self.window_caracteristique['length side'] /
														   self.window_caracteristique['definition'])


		if not self.window_caracteristique['active border']:
			self.window_caracteristique['border'] = 0

		self.win = None
		self.winPrevMousePos = None
		self.CamX = 1
		self.CamY = 0
		self.CellClr = (255, 255, 255)
		self.BgClr = (0, 0, 0)
		self.log_var = ''
		return

	def show(self):
		self.win = pg.display.set_mode((self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2,
										self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2))
		self.winPrevMousePos = pg.mouse.get_pos()
		pg.display.set_icon(pygame.image.load('textures/logo.png'))
		pg.display.set_caption(self.window_caracteristique['title'])
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)
		return

	def log(self, *info):

		self.log_var += "".join([f'{" | " if i % 2 == 0 else ": "}{info[i]}' for i in range(len(info))])
		return self.log_var

	def aparecium(self, world=np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])):
		"""
		afiche un array dans la fenaitre pygame
		:param world: l'array a aficher dans la fenetre pygame
		"""
		self.win.fill(self.BgClr)

		self.log('pre camx', self.CamX, 'pre camy', self.CamY, 'pre world shape', world.shape)

		self.CamX = mandragore.clamp(self.CamX, 0, mandragore.clamp(world.shape[0] - self.window_caracteristique['definition'], 0, self.window_caracteristique['definition']))
		self.CamY = mandragore.clamp(self.CamY, 0, mandragore.clamp(world.shape[1] - self.window_caracteristique['definition'], 0, self.window_caracteristique['definition']))

		self.log('camx', self.CamX, 'camy', self.CamY)

		view = np.array(world[floor(self.CamY):floor(self.CamY) + self.window_caracteristique['definition'],
						floor(self.CamX):floor(self.CamX) + self.window_caracteristique['definition']])

		view_cordantate = np.array(np.where(view == 1)).tolist()

		for cy, cx in zip(view_cordantate[0], view_cordantate[1]):
			pg.draw.rect(self.win, self.CellClr, (cx * self.window_caracteristique['size of cells'] + self.window_caracteristique['border'],
												  cy * self.window_caracteristique['size of cells'] + self.window_caracteristique['border'],
												  self.window_caracteristique['size of cells'],
												  self.window_caracteristique['size of cells']))

		if self.window_caracteristique['active border']:
			self.edgeBorders(world.shape)

	def edgeBorders(self, world_shape):
		# revoir le comportement des bordure dans le cas d'un désoume
		self.log('world_shape', world_shape)
		if self.CamX == 0:
			pg.draw.rect(self.win, self.CellClr, (0, 0,
												  self.window_caracteristique['border'], self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2))
		if self.CamX >= world_shape[0] - self.window_caracteristique['definition']:
			pg.draw.rect(self.win, self.CellClr, (self.window_caracteristique['length side'] + self.window_caracteristique['border'], 0,
												  self.window_caracteristique['border'], self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2))
		if self.CamY == 0:
			pg.draw.rect(self.win, self.CellClr, (0, 0,
												  self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2, self.window_caracteristique['border']))
		if self.CamY >= world_shape[1] - self.window_caracteristique['definition']:
			pg.draw.rect(self.win, self.CellClr, (0, self.window_caracteristique['length side'] + self.window_caracteristique['border'],
												  self.window_caracteristique['length side'] + self.window_caracteristique['border'] * 2, self.window_caracteristique['border']))


class Menu_contextuele:
	def __init__(self, menu_contenue):
		self.section_lst = []
		self.add_sections(menu_contenue)
		self.rectangle = [0,0,0,0]
		self.afiche = False
		self.menu_surface = None

	def add_sections(self, menu_contenue):
		for section in menu_contenue:
			self.section_lst.append(self.Section(section))

		return

	def menu_clasic_comportement_right_clic(self, surface, width, size, color):
		if pg.mouse.get_pressed()[0]:
			self.afiche = False
		if pg.mouse.get_pressed()[2]:
			self.afiche = True
			self.rectangle[0:2] = pg.mouse.get_pos()
			self.show_menue(surface, self.rectangle[0:2], width, size, color)
		elif self.afiche:
			self.show_menue(surface, self.rectangle[0:2].copy(), width, size, color)


	def show_menue(self, surface, pos, width, size, color):
		pos = tuple(pos)
		self.menu_surface = pg.Surface(surface.get_size()).convert_alpha()

		self.rectangle[2] = width * size
		self.rectangle[3] = 8
		self.rectangle[0:2] = pos
		for section in self.section_lst:
			pos = [self.rectangle[0], self.rectangle[1] + self.rectangle[3]]
			section.show_section(self.menu_surface, self.rectangle[0:2], width, size, color, section != self.section_lst[0])

		self.rectangle[3] += 1 + 8
		pg.draw.rect(surface, mandragore.invertion_colorimetrique(color), self.rectangle)
		surface.blit(self.menu_surface, (0, 0))
		# self.rectangle = [0,0,0,0]
		return

	class Section:
		def __init__(self, options):
			self.option_lst = []
			self.add_options(options)

		def add_options(self, options):
			for option in options:
				self.option_lst.append(self.Option(*option))

		def show_section(self, surface, pos, width, size, color, line=True):
			if line:
				pos[1] += 4
				pg.draw.line(surface, mandragore.invertion_colorimetrique(color), pos, (pos[0] + width * size, pos[1]), 1)
				pos[1] += 4 + 1

			for option in self.option_lst:
				option.show_option(surface, pos, width, size, color)
				pos[1] += size
			return pos[1]

		class Option:
			padding_y = 2
			border_image = 8
			image_title = 4
			racourci_border = 4
			font = 'textures/SmallMemory.ttf'

			def __init__(self, image, name, function, racourcie):
				self.image = pg.image.load(image) if image != '' else ''
				self.name = name
				self.text_rect = None
				self.function = function
				self.racourcie = racourcie
				self.font_object = None

			def show_option(self, surface, pos, width, size, color):
				pg.draw.rect(surface, color, (*pos, width * size, size))
				xpos = self.border_image + self.padding_y
				self.image = pg.transform.scale(self.image, (size - 2 * self.padding_y, size - 2 * self.padding_y))
				surface.blit(self.image.convert_alpha(), (pos[0] + xpos, pos[1] + self.padding_y))

				xpos += size - 2 * self.padding_y + self.image_title

				self.font_object = pg.font.Font(self.font, size - 2 * self.padding_y)
				self.name_surf = self.font_object.render(self.name, True, mandragore.invertion_colorimetrique(color))
				self.text_rect= self.name_surf.get_rect()
				#self.name_surf.set_colorkey(mandragore.invertion_colorimetrique(color))
				self.text_rect.center = (pos[0] + xpos + self.text_rect[2] / 2, pos[1] + size / 2)

				surface.blit(self.name_surf.convert_alpha(), self.text_rect)
				surface.convert_alpha()
