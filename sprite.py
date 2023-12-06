import pygame
from configurações import *
class Generico(pygame.sprite.Sprite):
	def __init__(self, posicao, surf, grupo, z = Camadas['main']):
		super().__init__(grupo)
		self.image = surf
		self.rect = self.image.get_rect(topleft = posicao)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Agua(Generico):
	def __init__(self, posicao, frames, grupo):

		self.frames = frames
		self.indice_frames = 0


		super().__init__(
				posicao = posicao,
				surf = self.frames[self.indice_frames],
				grupo = grupo,
				z = Camadas['agua'])

	def animacao(self, dt):
		self.indice_frames += 5 * dt
		if self.indice_frames >= len(self.frames):
			self.indice_frames = 0
		self.image = self.frames[int(self.indice_frames)]
	def update(self, dt):
		self.animacao(dt)

class Vegetacao(Generico):
	def __int__(self, posicao, surf, grupo):
		super().__int__(posicao, surf, grupo)
		self.hitbox = self.rect.copy().inflate(-20, -self.rect.heigth * 0.9)

class Arvore(Generico):
	def __init__(self, posicao, surf, grupo, name):
		super().__init__(posicao, surf, grupo)