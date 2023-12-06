import pygame
from configurações import *
from random import randint, choice
from Time import Timer
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

		# atributos

		self.vida = 5
		self.viva = True
		local_toco = f'./graficos/toco/{"small" if name == "Small" else "large"}.png'
		self.toco_surf = pygame.image.load(local_toco).convert_alpha()
		self.invul_timer = Timer(200)

		# maçãs
		self.maca_surf = pygame.image.load('./graficos/frutas/apple.png')
		self.maca_posicao = PosicaoMaca[name]
		self.maca_sprites = pygame.sprite.Group()
		self.cria_fruta()




	def dano(self):

		self.vida -= 1

		if len(self.maca_sprites.sprites()) > 0:
			maca_aleatoria = choice(self.maca_sprites.sprites())
			maca_aleatoria.kill()

	def verifica_morte(self):
		if self.vida <= 0:
			self.image = self.toco_surf
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
			self.hitbox = self.rect.copy().inflate(-10,-self.rect.height*0.6)
			self.viva = False

	def update(self,dt):
		if self.viva:
			self.verifica_morte()
	def cria_fruta(self):
		for posicao in self.maca_posicao:
			if randint(0, 10) < 2:
				x = posicao[0] + self.rect.left
				y = posicao[1] + self.rect.top
				Generico(
					posicao=(x, y),
					surf=self.maca_surf,
					grupo=[self.maca_sprites, self.groups()[0]],
					z=Camadas['fruta'])