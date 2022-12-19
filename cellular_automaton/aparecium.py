from math import *
import numpy as np
import pygame.image
# import maraudersMap as backend

import pygame as pg
import cellular_automaton.mandragore as mandragore

'''réorganisation'''


class Win:
	void = lambda *x : None
	def __init__(self, logo: str = False ):
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
		pg.display.set_icon(pygame.image.load(logo)) if logo else None
		pg.display.set_caption(self.win_spec['title'])
		pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

		self.camX = 0
		self.camY = 0
		self.CellClr = 0,0,0
		self.BgClr = 0,0,0
		self.OtherClr = 0,0,0
		self.log_var = ''
		self.touche = ''
		self.array_pos = 0, 0



		self.racoursit = {
			'play/pause': Win.void,
			'next': Win.void,
			'prev': Win.void,
			'restart': Win.void,
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

	def set_color(self, bg, cell):
		self.BgClr = bg
		self.CellClr = cell
		self.OtherClr = mandragore.moy_color(bg,cell)

	def aparecium(self, world: np.array = np.array([[1, 0, 1], [1, 1, 1], [1, 0, 1]]), grid=False):
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

		if grid:
			for loop in range(view.shape[1]-1):
				pg.draw.line(self.win, self.OtherClr, ((loop+1) * self.win_spec['size of cells'] - decalage_x, 0-decalage_y),
							 ((loop+1) * self.win_spec['size of cells'] - decalage_x, view.shape[0] * self.win_spec['size of cells']-(decalage_y+1)))
			for loop in range(view.shape[0]-1):
				pg.draw.line(self.win, self.OtherClr, (0-decalage_x, (loop+1) * self.win_spec['size of cells'] - decalage_y),
							 (view.shape[1] * self.win_spec['size of cells'] - (decalage_x+1), (loop + 1) * self.win_spec['size of cells'] - decalage_y))


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

	def input(self):
		speed = 0.5
		speed_zoom = 10
		pressed = pg.key.get_pressed()
		key_event = pg.event.get(pg.KEYDOWN)

		for loop in pg.event.get(pg.MOUSEWHEEL):
			self.zoom_middle(loop.y)

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

		for dep in pg.event.get(pg.MOUSEMOTION):
			if dep.buttons[0]:

				self.camX -= dep.rel[0]
				self.camY -= dep.rel[1]


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
	padding = 5
	padding_2 = 1

	def __init__(self, color, surface: pygame.surface, menu_contenue=None, width: int = 7, size: int = 20):

		self.target_surf = surface
		self.surface = pg.Surface(surface.get_size(), pg.SRCALPHA).convert_alpha()

		self.afiche = False
		self.pos = (0, 0)

		self.width = width
		self.size = size

		self.color = color
		self.color2 = mandragore.invertion_colorimetrique(color)
		self.color3 = ((np.array(self.color2) + np.array(self.color)) / 2).tolist()
		self.hightligh_color = (mandragore.clamp(self.color[0] - self.color[0] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[1] - self.color[1] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[2] + self.color[2] * 450 / 100, 0, 255))

		self.lst_orine = menu_contenue if menu_contenue is not None else []
		self.section_lst = []

		self.rectangle = [0, 0, 0, 0]

		self.font_object = pg.font.Font('textures/SmallMemory.ttf', self.size - (self.size // 10))

		self.generate_pg_obbject()

	def menu_clasic_comportement_right_clic(self):
		souris_event_up_list = pg.event.get(pg.MOUSEBUTTONUP)

		for souris_event_up in souris_event_up_list:
			if souris_event_up.button == 3 and not pg.rect.Rect(self.rectangle).collidepoint(souris_event_up.pos):
				self.afiche = True
				self.pos = souris_event_up.pos

			elif souris_event_up.button == 1 and not pg.rect.Rect(self.rectangle).collidepoint(souris_event_up.pos):
				self.afiche = False

		if self.afiche:
			self.show(self.pos)
			if pg.rect.Rect(self.rectangle).collidepoint(pg.mouse.get_pos()):
				pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
			else:
				pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)
		else:
			pg.mouse.set_cursor(pg.SYSTEM_CURSOR_SIZEALL)

	def show(self, pos: tuple[int, int]):
		pos = tuple(pos)
		self.surface = pg.Surface(self.target_surf.get_size(), pg.SRCALPHA).convert_alpha()
		self.rectangle[2] = self.padding
		self.rectangle[3] = self.padding
		self.rectangle[0:2] = pos

		mouse = pg.event.get(pg.MOUSEBUTTONDOWN)

		for section in self.section_lst:
			if section != self.section_lst[0]:
				self.rectangle[3] += 4
				pg.draw.line(self.surface, mandragore.invertion_colorimetrique(self.color), (self.rectangle[0] + self.rectangle[2], self.rectangle[1] + self.rectangle[3]),
							 (self.rectangle[0] + self.rectangle[2] + self.width * self.size, self.rectangle[1] + self.rectangle[3]), 1)
				self.rectangle[3] += 4 + 1

			for obtion in section:

				xpos = self.padding_2
				pos = self.rectangle[0] + self.rectangle[2], self.rectangle[1] + self.rectangle[3]
				size = self.width * self.size, self.size
				obtion_rect = (*pos, *size)

				for ev in mouse:

					if pg.rect.Rect(obtion_rect).collidepoint(ev.pos) and ev.button == 1:
						obtion[3]()

				if pg.rect.Rect(obtion_rect).collidepoint(pg.mouse.get_pos()):
					pg.draw.rect(self.surface, self.hightligh_color, obtion_rect)

				self.surface.blit(obtion[0].convert_alpha(), (pos[0] + xpos, pos[1] + self.padding_2))
				xpos += self.size - 2 * self.padding_2 + self.padding_2

				name_rect = obtion[1].get_rect()
				name_rect.center = (pos[0] + xpos + name_rect[2] / 2, pos[1] + self.size / 2)
				self.surface.blit(obtion[1].convert_alpha(), name_rect)

				short_rect = obtion[2].get_rect()
				short_rect.center = (pos[0] + size[0] - short_rect.size[0] / 2, pos[1] + self.size / 2)
				self.surface.blit(obtion[2].convert_alpha(), short_rect)

				self.rectangle[3] += self.size

		self.rectangle[3] += 1 + self.padding
		self.rectangle[2] += self.width * self.size
		self.rectangle[2] += self.padding
		pg.draw.rect(self.target_surf, self.color3, self.rectangle)
		pg.draw.rect(self.target_surf, self.color, (self.rectangle[0] + 1, self.rectangle[1] + 1, self.rectangle[2] - 2, self.rectangle[3] - 2))
		self.target_surf.blit(self.surface, (0, 0))

	def generate_pg_obbject(self):
		self.font_object = pg.font.Font('textures/SmallMemory.ttf', self.size - (self.size // 10))
		self.section_lst = []
		for section in self.lst_orine:
			lst_obtion = []
			for obtion in section:
				lst_obtion.append([pg.transform.scale(pg.image.load(obtion[0]) if obtion[0] != '' else pg.image.load('../textures/buttons/void.png'),
													  (self.size - 2 * self.padding_2, self.size - 2 * self.padding_2)),
								   self.font_object.render(obtion[1], True, self.color2),
								   self.font_object.render(obtion[3], True, self.color3),
								   obtion[2]
								   ])

			self.section_lst.append(lst_obtion)

	def set_color(self, color):
		self.color = color
		self.color2 = mandragore.invertion_colorimetrique(color)
		self.color3 = ((np.array(self.color2) + np.array(self.color)) / 2).tolist()

		self.hightligh_color = (mandragore.clamp(self.color[0] - self.color[0] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[1] - self.color[1] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[2] + self.color[2] * 450 / 100, 0, 255))

	def set_obtion(self, section_index, obtion_index, image=None, name=None, short=None, func=None):
		obtion = self.section_lst[section_index][obtion_index]
		if image is not None:
			obtion[0] = pg.transform.scale(pg.image.load(image) if image != '' else pg.image.load('../textures/buttons/void.png'),
										   (self.size - 2 * self.padding_2, self.size - 2 * self.padding_2))

		if name is not None:
			obtion[1] = self.font_object.render(name, True, self.color2)

		if short is not None:
			obtion[2] = self.font_object.render(short, True, self.color3)

		if func is not None:
			obtion[3] = func

	def pxcord_arraycord(self,cord:tuple[int, int]):

		return


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


