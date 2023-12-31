import pygame
from configurações import *
from suporte import *
from sprite import Generico
from random import randint, choice

class Chuva:
	def __init__(self, all_sprites):
		self.all_sprites = all_sprites
		self.pingos_chuva = importa_pasta('./graficos/chuva/drops/')
		self.chao_molhado = importa_pasta('./graficos/chuva/floor/')
		self.largura, self.altura = pygame.image.load('./graficos/mundo/ground.png').get_size()

	def cria_chao_molhado(self):
		Pingos(choice(self.chao_molhado),(randint(0, self.largura), randint(0, self.altura)),
			   False, self.all_sprites, z = Camadas['chao molhado'])

	def cria_pingos_chuva(self):
		Pingos(choice(self.pingos_chuva),(randint(0, self.largura), randint(0, self.altura)),
			   True,self.all_sprites,z = Camadas['pingos de chuva'])

	def update(self):
		self.cria_chao_molhado()
		self.cria_pingos_chuva()

class Pingos(Generico):
	def __init__(self, surf, posicao, movimento, grupo, z):
		super().__init__(posicao, surf, grupo, z)
		self.lifetime = randint(400,500)
		self.tempo_inicial = pygame.time.get_ticks()

		# Movimento
		self.movimento = movimento
		if self.movimento:
			self.posicao = pygame.math.Vector2(self.rect.topleft)
			self.direcao = pygame.math.Vector2(-2,4)
			self.velocidade = randint(180,240)

	def update(self, dt):
		tempo_atual = pygame.time.get_ticks()
		if self.movimento:
			self.posicao += self.direcao * self.velocidade * dt
			self.rect.topleft = (round(self.posicao.x), round(self.posicao.y))

		if tempo_atual - self.tempo_inicial >= self.lifetime:
			self.kill()

class Ceu:
	def __init__(self):
		self.superfice_tela = pygame.display.get_surface()
		self.surf = pygame.Surface((largura, altura))
		self.cor_inicial = [255, 255, 255]
		self.cor_pordosol = [242,72,130]
		self.cor_final = (46, 68, 130)

	def tela(self, dt):
		#print(self.cor_inicial)
		for indice, valor in enumerate(self.cor_pordosol):
			if self.cor_inicial[indice] > valor:
				self.cor_inicial[indice] -= 2 * dt
			elif self.cor_inicial[indice] <= valor:
				for indice2, valor2 in enumerate(self.cor_final):
					if self.cor_inicial[indice2] > valor2:
						self.cor_inicial[indice2] -= 2 * dt

		self.surf.fill(self.cor_inicial)
		self.superfice_tela.blit(self.surf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)