import pygame
from configurações import *
from pytmx.util_pygame import load_pygame
from suporte import *
from random import choice

class SoloTiles(pygame.sprite.Sprite):
	def __init__(self, posicao, surf, grupo):
		super().__init__(grupo)
		self.image = surf
		self.rect = self.image.get_rect(topleft = posicao)
		self.z = Camadas['solo']

class AguaTiles(pygame.sprite.Sprite):
	def __init__(self, posicao, surf, grupo):
		super().__init__(grupo)
		self.image = surf
		self.rect = self.image.get_rect(topleft = posicao)
		self.z = Camadas['solo molhado']

class CamadaSolo:
	def __init__(self, all_sprites, colisao_sprites):

		# sprite groups
		self.all_sprites = all_sprites
		self.colisao_sprites = colisao_sprites
		self.solo_sprites = pygame.sprite.Group()
		self.solo_molhado_sprites = pygame.sprite.Group()
		self.planta_sprites = pygame.sprite.Group()

		# graphics
		self.solo_surfs = importa_dicionario('./graficos/solo/')
		self.solo_molhado_surf = importa_pasta("./graficos/solo_molhado")

		self.cria_solo()
		self.cria_rects_araveis()

	def cria_solo(self):
		chao = pygame.image.load('./graficos/mundo/ground.png')
		horizontal_tiles = chao.get_width() // tile_size
		vertical_tiles = chao.get_height() // tile_size

		self.grid = [[[] for coluna in range(horizontal_tiles)] for linha in range(vertical_tiles)]
		for x, y, _ in load_pygame('./data/map.tmx').get_layer_by_name('Farmable').tiles():
			self.grid[y][x].append('F')

	def cria_rects_araveis(self):
		self.hit_rects = []
		for indice_linha, linha in enumerate(self.grid):
			for indice_coluna, coluna in enumerate(linha):
				if 'F' in coluna:
					x = indice_coluna * tile_size
					y = indice_linha * tile_size
					rect = pygame.Rect(x, y, tile_size, tile_size)
					self.hit_rects.append(rect)

	def arar(self, posicao_alvo):
		for rect in self.hit_rects:
			if rect.collidepoint(posicao_alvo):
				x = rect.x // tile_size
				y = rect.y // tile_size
				if 'F' in self.grid[y][x]:
					self.grid[y][x].append('X')
					self.solo_tiles()
					if self.chovendo:
						self.choveu_molhou()

	def solo_tiles(self):
		self.solo_sprites.empty()
		for indice_linha, linha in enumerate(self.grid):
			for indice_coluna, coluna in enumerate(linha):
				if 'X' in coluna:

					t = 'X' in self.grid[indice_linha - 1][indice_coluna]
					b = 'X' in self.grid[indice_linha + 1][indice_coluna]
					r = 'X' in linha[indice_coluna + 1]
					l = 'X' in linha[indice_coluna - 1]

					tile_padrao = 'o'

					# Verficando onde foi arado
					if all((t,b,r,l)): tile_padrao = 'x'

					# Vertical
					if t and not any((b,r,l)): tile_padrao = 'b'
					if b and not any((t,r,l)): tile_padrao = 't'
					if t and b and not any((r,l)): tile_padrao = 'tb'

					# horizontal
					if r and not any((t,b,l)): tile_padrao = 'l'
					if l and not any((t,b,r)): tile_padrao = 'r'
					if r and l and not any((t,b)): tile_padrao = 'lr'

					# Cantos e meios
					if l and b and not any((t, r)): tile_padrao = 'tr'
					if r and b and not any((t, l)): tile_padrao = 'tl'
					if l and t and not any((b, r)): tile_padrao = 'br'
					if r and t and not any((b, l)): tile_padrao = 'bl'

					if all((t,b,r)) and not l: tile_padrao = 'tbr'
					if all((t,b,l)) and not r: tile_padrao = 'tbl'
					if all((l,r,t)) and not b: tile_padrao = 'lrb'
					if all((l,r,b)) and not t: tile_padrao = 'lrt'

					SoloTiles((indice_coluna * tile_size, indice_linha * tile_size), self.solo_surfs[tile_padrao],
							  [self.all_sprites, self.solo_sprites])

	def agua(self, posicao_alvo):
		for solo_sprite in self.solo_sprites.sprites():
			if solo_sprite.rect.collidepoint(posicao_alvo):
				x = solo_sprite.rect.x // tile_size
				y = solo_sprite.rect.y // tile_size
				self.grid[y][x].append('A')

				AguaTiles(solo_sprite.rect.topleft, choice(self.solo_molhado_surf), [self.all_sprites, self.solo_molhado_sprites])

	def choveu_molhou(self):
		for indice_linha, linha in enumerate(self.grid):
			for indice_coluna, coluna in enumerate(linha):
				if 'X' in coluna and 'A' not in coluna:
					coluna.append('A')
					x = indice_coluna * tile_size
					y = indice_linha * tile_size
					AguaTiles((x,y), choice(self.solo_molhado_surf), [self.all_sprites, self.solo_molhado_sprites])

	def remove_agua(self):

		# Remove sprites de agua
		for sprite in self.solo_molhado_sprites.sprites():
			sprite.kill()

		# Limpa o A do grid
		for linha in self.grid:
			for coluna in linha:
				if 'A' in coluna:
					coluna.remove('A')

	def verifica_molhado(self, posicao):
		x = posicao[0] // tile_size
		y = posicao[1] // tile_size
		coluna = self.grid[y][x]
		molhado = 'A' in coluna
		return molhado

	def semente_planta(self, posicao_alvo, semente):
		for solo_sprite in self.solo_sprites.sprites():
			if solo_sprite.rect.collidepoint(posicao_alvo):

				x = solo_sprite.rect.x // tile_size
				y = solo_sprite.rect.y // tile_size

				if 'P' not in self.grid[y][x]:
					self.grid[y][x].append('P')
					Planta(semente, [self.all_sprites, self.planta_sprites, self.colisao_sprites], solo_sprite, self.verifica_molhado)

	def update_plantas(self):
		for planta in self.planta_sprites.sprites():
			planta.crescimento_planta()


class Planta(pygame.sprite.Sprite):
	def __init__(self, tipo_planta, grupo, solo, verifica_molhado):
		super().__init__(grupo)

		# setup
		self.tipo_planta = tipo_planta
		self.frames = importa_pasta(f'./graficos/frutas/{tipo_planta}')
		self.solo = solo
		self.verifica_molhado = verifica_molhado

		# Crecimento da planta
		self.crescimento = 0
		self.crescimento_maximo = len(self.frames) - 1
		self.velocidade_crescimento = VelocidadeCrescimento[tipo_planta]
		self.maduro = False

		# sprite setup
		self.image = self.frames[self.crescimento]
		self.y_offset = -16 if tipo_planta == 'corn' else -8
		self.rect = self.image.get_rect(midbottom=solo.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
		self.z = Camadas['planta']

	def crescimento_planta(self):
		if self.verifica_molhado(self.rect.center):
			self.crescimento += self.velocidade_crescimento

			if int(self.crescimento) > 0:
				self.z = Camadas['main']
				self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

			if self.crescimento >= self.crescimento_maximo:
				self.crescimento = self.crescimento_maximo
				self.maduro = True

			self.image = self.frames[int(self.crescimento)]
			self.rect = self.image.get_rect(midbottom= self.solo.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
