import pygame
from configurações import *
from pytmx.util_pygame import load_pygame
from suporte import *

class SoloTiles(pygame.sprite.Sprite):
	def __init__(self, posicao, surf, grupo):
		super().__init__(grupo)
		self.image = surf
		self.rect = self.image.get_rect(topleft = posicao)
		self.z = Camadas['solo']

class CamadaSolo:
	def __init__(self, all_sprites):

		# sprite groups
		self.all_sprites = all_sprites
		self.solo_sprites = pygame.sprite.Group()

		# graphics
		self.solo_surf = pygame.image.load('./graficos/solo/o.png')
		self.solo_surfs = importa_dicionario('./graficos/solo/')

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

	def arar(self, ponto):
		for rect in self.hit_rects:
			if rect.collidepoint(ponto):
				x = rect.x // tile_size
				y = rect.y // tile_size
				if 'F' in self.grid[y][x]:
					self.grid[y][x].append('X')
					self.solo_tiles()

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
