import pygame
from configurações import *

class Overlay:
	def __init__(self, player):

		# general setup
		self.superfice_tela = pygame.display.get_surface()
		self.player = player

		# imports
		overlay_local = './graficos/overlay/'
		self.ferramentas_surf = {ferramenta: pygame.image.load(f'{overlay_local}{ferramenta}.png').convert_alpha() for ferramenta in player.ferramentas}
		self.sementes_surf = {semente: pygame.image.load(f'{overlay_local}{semente}.png').convert_alpha() for semente in player.sementes}

		# import overlay inventario
		self.overlay_madeira = pygame.image.load('./graficos/overlay/Madeira.png').convert_alpha()
		self.overlay_maca = pygame.image.load('./graficos/overlay/Maçã.png').convert_alpha()
		self.overlay_trigo = pygame.image.load(f'{overlay_local}Trigo.png').convert_alpha()
		self.overlay_tomate = pygame.image.load(f'{overlay_local}Tomate.png').convert_alpha()
		self.overlay_dinheiro = pygame.image.load(f'{overlay_local}dinheiro.png').convert_alpha()

		# pegando os valores do inventario
		self.quantidade_item = list(self.player.item_inventario.values())
		self.quantidade_sementes = list(self.player.sementes_inventario.values())
		self.fonte = pygame.font.Font('./fonte/LycheeSoda.ttf', 30)


	def tela(self):


		ferramenta_surf = self.ferramentas_surf[self.player.selecionando_ferramenta]
		ferramenta_rect = ferramenta_surf.get_rect(midbottom = Overlay_Posicao['ferramenta'])
		self.superfice_tela.blit(ferramenta_surf, ferramenta_rect)

		semente_surf = self.sementes_surf[self.player.selecionando_sementes]
		semente_rect = semente_surf.get_rect(midbottom = Overlay_Posicao['semente'])
		self.semente_rect = semente_rect
		self.superfice_tela.blit(semente_surf, semente_rect)
	def overlay_inventario(self):
		self.quantidade_item = list(self.player.item_inventario.values())
		self.quantidade_sementes = list(self.player.sementes_inventario.values())


		pygame.Surface((largura,altura))
		retangulo_inventario = pygame.Rect(10,10, 56*4,58)
		pygame.draw.rect(self.superfice_tela, (111, 78, 55), retangulo_inventario)

		back1_rect = pygame.Rect(14, 14, 50,50)
		pygame.draw.rect(self.superfice_tela, (193, 154, 107), back1_rect)

		back2_rect = pygame.Rect(back1_rect.right + 5, 14, 50, 50)
		pygame.draw.rect(self.superfice_tela, (193, 154, 107), back2_rect)

		back3_rect = pygame.Rect(back2_rect.right + 5, 14, 50, 50)
		pygame.draw.rect(self.superfice_tela, (193, 154, 107), back3_rect)

		back4_rect = pygame.Rect(back3_rect.right + 5, 14, 50, 50)
		pygame.draw.rect(self.superfice_tela, (193, 154, 107), back4_rect)

		self.superfice_tela.blit(pygame.transform.scale(self.overlay_madeira, (40,40)), (back1_rect.x +5, back1_rect.y + 5))
		self.superfice_tela.blit(pygame.transform.scale(self.overlay_maca, (50, 40)), (back2_rect.x, back2_rect.y + 5))
		self.superfice_tela.blit(pygame.transform.scale(self.overlay_trigo, (50, 50)), back3_rect)
		self.superfice_tela.blit(pygame.transform.scale(self.overlay_tomate, (50, 50)), back4_rect)

		surf_texto_madeira = self.fonte.render(str(self.quantidade_item[0]), False, 'Black')
		rect_texto_madeira = surf_texto_madeira.get_rect(topleft = (back1_rect.x + 2, back1_rect.y - 6))
		self.superfice_tela.blit(surf_texto_madeira,rect_texto_madeira)

		surf_texto_maca = self.fonte.render(str(self.quantidade_item[1]), False, "black")
		rect_texto_maca = surf_texto_maca.get_rect(topleft = (back2_rect.x + 2, back2_rect.y - 6))
		self.superfice_tela.blit(surf_texto_maca,rect_texto_maca)

		surf_texto_milho = self.fonte.render(str(self.quantidade_item[2]), False, "black")
		rect_texto_milho = surf_texto_milho.get_rect(topleft=(back3_rect.x + 2, back3_rect.y - 6))
		self.superfice_tela.blit(surf_texto_milho, rect_texto_milho)

		surf_texto_tomate = self.fonte.render(str(self.quantidade_item[3]), False, "black")
		rect_texto_tomate = surf_texto_tomate.get_rect(topleft=(back4_rect.x + 2, back4_rect.y - 6))
		self.superfice_tela.blit(surf_texto_tomate, rect_texto_tomate)

		surf_semente = self.fonte.render(str(self.quantidade_sementes[0 if self.player.selecionando_sementes == 'corn' else 1]), False, "white")
		rect_semente = surf_semente.get_rect(bottomleft=(self.semente_rect.right + 3, self.semente_rect.centery))
		self.superfice_tela.blit(surf_semente,rect_semente)