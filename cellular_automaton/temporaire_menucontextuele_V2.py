import numpy as np
import pygame.image

import pygame as pg
import cellular_automaton.mandragore as mandragore


class MenuContextuele:
	padding = 5
	padding_2 = 1

	def __init__(self, color, surface: pygame.surface, menu_contenue=None, width: int = 7, size: int = 20):

		self.target_surf = surface
		self.surface = pg.Surface(surface.get_size(), pg.SRCALPHA).convert_alpha()

		self.afiche = False
		self.pos = (0,0)

		self.width = width
		self.size = size

		self.color = color
		self.color2 = mandragore.invertion_colorimetrique(color)
		self.hightligh_color = (mandragore.clamp(self.color[0] - self.color[0] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[1] - self.color[1] * 450 / 100, 0, 255),
								mandragore.clamp(self.color[2] + self.color[2] * 450 / 100, 0, 255))

		self.lst_orine = menu_contenue if menu_contenue is not None else []
		self.section_lst = []

		self.rectangle = [0, 0, 0, 0]

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
		self.surface = pg.Surface(self.surface.get_size(), pg.SRCALPHA).convert_alpha()
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

					if pg.rect.Rect(obtion_rect).collidepoint(ev.pos):
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
		pg.draw.rect(self.target_surf, (255, 255, 0), self.rectangle)
		self.target_surf.blit(self.surface, (0, 0))

	def generate_pg_obbject(self):
		font_object = pg.font.Font('textures/SmallMemory.ttf', self.size - (self.size//10))
		self.section_lst = []
		for section in self.lst_orine:
			lst_obtion = []
			for obtion in section:
				lst_obtion.append([pg.transform.scale(pg.image.load(obtion[0]) if obtion[0] != '' else pg.image.load('../textures/buttons/void.png'),
													  (self.size - 2 * self.padding_2, self.size - 2 * self.padding_2)),
								   font_object.render(obtion[1], True, self.color2),
								   font_object.render(obtion[3], True, ((np.array(self.color2) + np.array(self.color)) / 2).tolist()),
								   obtion[2]
								   ])

			self.section_lst.append(lst_obtion)