import pygame
from configurações import *

class Overlay:
	def __init__(self,player):

		# general setup
		self.superfice_tela = pygame.display.get_surface()
		self.player = player

		# imports
		overlay_local = './graficos/overlay/'
		self.ferramentas_surf = {ferramenta: pygame.image.load(f'{overlay_local}{ferramenta}.png').convert_alpha() for ferramenta in player.ferramentas}
		self.sementes_surf = {semente: pygame.image.load(f'{overlay_local}{semente}.png').convert_alpha() for semente in player.sementes}

	def tela(self):


		ferramenta_surf = self.ferramentas_surf[self.player.selecionando_ferramenta]
		ferramenta_rect = ferramenta_surf.get_rect(midbottom = Overlay_Posicao['ferramenta'])
		self.superfice_tela.blit(ferramenta_surf, ferramenta_rect)

		semente_surf = self.sementes_surf[self.player.selecionando_sementes]
		semente_rect = semente_surf.get_rect(midbottom = Overlay_Posicao['semente'])
		self.superfice_tela.blit(semente_surf, semente_rect)