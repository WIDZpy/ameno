from math import *
import numpy as np
import pygame.image
# import maraudersMap as backend

import pygame as pg
import cellular_automaton.mandragore as mandragore

'''réorganisation'''


class Win:
	void = lambda *x : None
	def __init__(self, bgcolor=(0, 0, 0), colorcell=(255, 255, 255)):
		self.win_spec = {
			'title': "John Conway's Game of Life",
			'length side': (2 ** 9, 2 ** 9),
			'size of cells': 2 ** 9 // 2 ** 6,
			'active border': True,
			'border': 1,
			'pading': 1,
			'resizable': True,
		}

		if not self.win_spec['active border']:
			self.win_spec['border'] = 0
			self.win_spec['pading'] = 0

		if self.win_spec.get('resizable'):
			self.win = pg.display.set_mode((self.win_spec['length side'][0],
											self.win_spec['length side'][1]), pg.RESIZABLE)
		else:
			self.win = pg.display.set_mode((self.win_spec['length side'][0],
											self.win_spec['length side'][1]))


		self.winPrevMousePos = pg.mouse.get_pos()
		pg.display.set_icon(pygame.image.load('textures/logo.png'))
		pg.display.set_caption(self.win_spec['title'])
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

		self.camX = 0
		self.camY = 0
		self.CellClr = colorcell
		self.BgClr = bgcolor
		self.log_var = ''
		self.touche = ''
		self.array_pos = 0, 0



		self.racoursit = {
			'play/pause': Win.void,
			'next': Win.void,
			'prev': Win.void
		}

		return

	def set_array_pos(self, x, y):
		self.array_pos = x, y

	def set_center(self, x, y):
		self.camX = x - self.win_spec['length side'][0] // 2
		self.camY = y - self.win_spec['length side'][1] // 2

	def get_center(self):
		return self.camX + self.win_spec['length side'][0] // 2, \
			   self.camY + self.win_spec['length side'][1] // 2

	def reset_cam(self):
		self.camX = 0
		self.camY = 0
		self.array_pos = 0, 0
		self.win_spec['size of cells'] = 2 ** 9 // 2 ** 6

	def log(self, *info):
		self.log_var += "".join([f'{" | " if i % 2 == 0 else ": "}{info[i]}' for i in range(len(info))])
		return self.log_var

	def aparecium(self, world=np.array([[1, 0, 1], [1, 1, 1], [1, 0, 1]])):
		"""
		fiche un array dans la fenêtre pygame
		:param world: l'array a afficher dans la fenêtre pygame
		"""

		self.win_spec['length side'] = self.win.get_size()

		world_size = world.shape

		self.win.fill(self.BgClr)

		dec_y = self.camY - self.array_pos[1] * self.win_spec['size of cells']
		dec_x = self.camX - self.array_pos[0] * self.win_spec['size of cells']

		view = world[mandragore.clamp(dec_y // self.win_spec['size of cells'], 0, world_size[0]):
					 mandragore.clamp(ceil(dec_y / self.win_spec['size of cells']) + ceil(self.win_spec['length side'][1] / self.win_spec['size of cells']),
									  0, world_size[0]),
			   mandragore.clamp(dec_x // self.win_spec['size of cells'], 0, world_size[1]):
			   mandragore.clamp(ceil(dec_x / self.win_spec['size of cells']) + ceil(self.win_spec['length side'][0] / self.win_spec['size of cells']), 0,
								world_size[1])]


		decalage_x = dec_x % self.win_spec['size of cells'] if dec_x > 0 else dec_x
		decalage_y = dec_y % self.win_spec['size of cells'] if dec_y > 0 else dec_y


		for cy, cx in zip(*mandragore.get_coordinates(view, 1)):
			pg.draw.rect(self.win, self.CellClr, (cx * self.win_spec['size of cells'] - decalage_x,
												  cy * self.win_spec['size of cells'] - decalage_y,
												  self.win_spec['size of cells'], self.win_spec['size of cells']))

		if self.win_spec['active border']:
			self.edgeBorders(world.shape, dec_x, dec_y)

		return

	def edgeBorders(self, world_shape, dec_x, dec_y):
		pg.draw.rect(self.win, self.CellClr, (-1*(dec_x + self.win_spec['pading'] + self.win_spec['border']),
										     -1*(dec_y + self.win_spec['pading'] + self.win_spec['border']),
											 self.win_spec['border'], (self.win_spec['border'] + self.win_spec['pading']) * 2 + world_shape[0] * self.win_spec['size of cells']))

		pg.draw.rect(self.win, self.CellClr, (-1 * (dec_x + self.win_spec['pading'] + self.win_spec['border']),
											 -1 * (dec_y + self.win_spec['pading'] + self.win_spec['border']),
											(self.win_spec['border'] + self.win_spec['pading']) * 2 + world_shape[1] * self.win_spec['size of cells'], self.win_spec['border']))

		pg.draw.rect(self.win, self.CellClr, (-1 * dec_x + world_shape[1] * self.win_spec['size of cells'] + self.win_spec['pading'],
											 -1*(dec_y + self.win_spec['pading'] + self.win_spec['border']),
											 self.win_spec['border'], (self.win_spec['border'] + self.win_spec['pading']) * 2 + world_shape[0] * self.win_spec['size of cells']))

		pg.draw.rect(self.win, self.CellClr, (-1 * (dec_x + self.win_spec['pading'] + self.win_spec['border']),
											 -1 * dec_y + world_shape[0] * self.win_spec['size of cells'] + self.win_spec['pading'],
											(self.win_spec['border'] + self.win_spec['pading']) * 2 + world_shape[1] * self.win_spec['size of cells'],self.win_spec['border']))

	def key_bord_input(self):
		speed = 0.5
		speed_zoom = 10
		pressed = pg.key.get_pressed()
		key_event = pg.event.get(pg.KEYDOWN)

		# self.log("touche", self.touche)

		if len(key_event) == 0 and not (pressed[pg.K_LCTRL] or pressed[pg.K_LALT]):

			if pressed[pg.K_RIGHT]:
				self.moov(speed, 0)
				self.touche = "→"

			if pressed[pg.K_LEFT]:
				self.moov(-speed)
				self.touche = "←"

			if pressed[pg.K_UP]:
				self.moov(0, -speed)
				self.touche = "↑"

			if pressed[pg.K_DOWN]:
				self.moov(0, speed)
				self.touche = "↓"

		for key in key_event:
			if key.unicode == ' ':
				self.touche = "space"
				self.racoursit['play/pause']()

			if key.scancode == 79:  # fleche de droite
				if pressed[pg.K_LCTRL]:
					self.racoursit['next']()
					self.touche = "ctl + →"

				if pressed[pg.K_LALT]:
					self.moov(10)
					self.touche = "alt + →"

			if key.scancode == 100:
				if pressed[pg.K_LCTRL]:
					self.racoursit['restart']()
					self.touche = "ctl + <"

			if key.scancode == 80:
				if pressed[pg.K_LCTRL]:
					self.racoursit['prev']()
					self.touche = "ctl + ←"
				if pressed[pg.K_LALT]:
					self.moov(-10)
					self.touche = "alt + ←"

			if key.scancode == 82:
				if pressed[pg.K_LCTRL]:
					self.zoom_middle(-1 * speed_zoom)
					self.touche = "ctl + ↑"
				if pressed[pg.K_LALT]:
					self.moov(0, -10)
					self.touche = "alt + ↑"

			if key.scancode == 81:
				if pressed[pg.K_LCTRL]:
					self.zoom_middle(speed_zoom)
					self.touche = "ctl + ↓"
				if pressed[pg.K_LALT]:
					self.moov(0, 10)
					self.touche = "alt + ↓"

	def moov(self, x=0, y=0):
		self.camX += mandragore.ceil_floor(x * self.win_spec['size of cells'])
		self.camY += mandragore.ceil_floor(y * self.win_spec['size of cells'])

	def zoom_corner(self, z):
		new_size = mandragore.clamp(self.win_spec['size of cells'] + mandragore.ceil_floor((self.win_spec['size of cells'] * z) / 100), 1)

		self.camX = round(self.camX * new_size / self.win_spec['size of cells'])
		self.camY = round(self.camY * new_size / self.win_spec['size of cells'])

		self.win_spec['size of cells'] = new_size

	def zoom_middle(self,z):
		new_size = mandragore.clamp(self.win_spec['size of cells'] + mandragore.ceil_floor((self.win_spec['size of cells'] * z) / 100), 1)

		center = self.get_center()
		new_center = round(center[0] * new_size / self.win_spec['size of cells']), \
					 round(center[1] * new_size / self.win_spec['size of cells'])

		self.set_center(*new_center)
		self.win_spec['size of cells'] = new_size


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
				self.image = pg.image.load(image) if image != '' else pg.image.load('../textures/buttons/void.png')
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
				self.image = (pg.image.load(image) if image is not None else self.image) if image != '' else pg.image.load(textures/buttons/void.png)
				self.short = short if short is not None else self.short
				self.function = fonction if fonction is not None else self.function

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


class DataDisplay:
	def __init__(self, data={}, mod='top_right',color=(255, 255, 255),bgcolor=(0, 0, 0),size=20):
		# self.surf = pg.surface.Surface()
		self.mod =  mod # bottom_left bottom_right top_left top_right
		self.data = data
		self.size = size
		self.color = color
		self.bgcolor = bgcolor

	def update_data(self,dict: dict):
		self.data.update(dict)


	def draw(self,surface=None):
		self.font_object = pg.font.Font('textures/SmallMemory.ttf', self.size)
		self.string = "".join([f"  {cey}: {value}  " for cey, value in self.data.items()])
		self.data_surf = self.font_object.render(self.string, True, self.color)
		bg_surf = pg.surface.Surface(self.data_surf.get_size())
		bg_surf.fill(self.bgcolor)
		bg_surf.blit(self.data_surf,(0,0))

		if self.mod == 'top_right':
			surface.blit(bg_surf, (surface.get_size()[0]-(bg_surf.get_size()[0]), 5))
		elif self.mod == 'top_left':
			surface.blit(bg_surf, (0, 5))
		elif self.mod == 'bottom_left':
			surface.blit(bg_surf, (0, surface.get_size()[1]-bg_surf.get_size()[1]))
		elif self.mod == 'bottom_right':
			surface.blit(bg_surf, (surface.get_size()[0]-(self.size+5), 5))

if __name__ == '__main__':
	pg.init()
	color1 = (255, 255, 255)
	color2 = (0, 0, 0)
	pg_win = Win(color2, color1)
	clock = pg.time.Clock()

	pg_win.set_array_pos(-1,4)

	while True:
		clock.tick(60)

		if pg.event.get(pg.QUIT):
			# print("\n", co.Fore.RED + "END", sep='', end='')
			break
		pg.display.update()
		pg_win.aparecium(np.array([[1,0,1],[1,1,1],[0,0,1]]))


