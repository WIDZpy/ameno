import numpy as np
import pygame.image

import pygame as pg
import cellular_automaton.mandragore as mandragore


class MenuContextuele:
	padding = 5
	padding_2 = 1

	def __init__(self, color, surface: pygame.surface, width: int = 7, size: int = 20, menu_contenue=None):

		self.surface = surface
		self.width = width
		self.size = size
		self.color = color
		self.color2 = mandragore.invertion_colorimetrique(color)
		self.hightligh_color = (mandragore.clamp(self.color[0] - self.color[0] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[1] - self.color[1] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[2] + self.color[2] * 450 / 100, 0, 255))
		self.lst_orine = menu_contenue
		self.section_lst = []
		self.rectangle = [0, 0, 0, 0]
		self.generate_pg_obbject()

	def show(self, pos: tuple[int, int]):
		self.rectangle[2] = self.padding
		self.rectangle[3] = self.padding
		self.rectangle[0:2] = pos
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

				self.surface.blit(obtion[0].convert_alpha(), (pos[0] + xpos, pos[1] + self.padding_2))
				xpos += self.size - 2 * self.padding_2 + self.padding_2

				name_rect = obtion[1].get_rect()
				name_rect.center = (pos[0] + xpos + name_rect[2] / 2, pos[1] + self.size / 2)
				self.surface.blit(obtion[1].convert_alpha(), name_rect)

				short_rect = object[2].get_rect()
				short_rect.center = (pos[0] + size[0] - short_rect.size[0] / 2, pos[1] + self.size / 2)
				self.surface.blit(obtion[2].convert_alpha(), short_rect)

				self.rectangle[3] += self.size

	def generate_pg_obbject(self):
		font_object = pg.font.Font('textures/SmallMemory.ttf', self.size - (self.size//10))
		self.section_lst = []
		for section in self.lst_orine:
			lst_obtion = []
			for obtion in section:
				lst_obtion.append([pg.transform.scale(pg.image.load(obtion[0]) if obtion[0] != '' else pg.image.load('../textures/buttons/void.png'),
													  (self.size - 2 * self.padding_2, self.size - 2 * self.padding_2)),
								   font_object.render(obtion[1], True, self.color2),
								   font_object.render(obtion[3], True, ((np.array(self.color2) + np.array(self.color)) / 2).tolist())
								   ])


			self.section_lst.append()

