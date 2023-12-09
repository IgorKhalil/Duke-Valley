import pygame
from configurações import *
from Time import Timer

class Menu:
	def __init__(self, player, alterna_menu):

		# setup
		self.player = player
		self.alterna_menu = alterna_menu
		self.superfice_tela = pygame.display.get_surface()
		self.fonte = pygame.font.Font('./fonte/LycheeSoda.ttf', 30)

		# variaveis
		self.largura = 350
		self.espaco = 10
		self.padding = 8

		# lista de inventario
		self.opcoes = list(self.player.item_inventario.keys()) + list(self.player.sementes_inventario.keys())
		self.area_de_venda = len(self.player.item_inventario) - 1
		self.setup()

		# movement
		self.indice = 0
		self.timer = Timer(200)

	def tela_dinheiro(self):
		texto_surf = self.fonte.render(f'R${self.player.dinheiro}', False, 'Black')
		texto_rect = texto_surf.get_rect(midbottom = (largura / 2, altura - 20))

		pygame.draw.rect(self.superfice_tela, 'White', texto_rect.inflate(10, 10), 0, 4)
		self.superfice_tela.blit(texto_surf, texto_rect)

	def setup(self):

		# Superficies de texto
		self.texto_surfs = []
		self.total_altura = 0

		for item in self.opcoes:
			texto_surf = self.fonte.render(item, False, 'Black')
			self.texto_surfs.append(texto_surf)
			self.total_altura += texto_surf.get_height() + (self.padding * 2)

		self.total_altura += (len(self.texto_surfs) - 1) * self.espaco
		self.menu_top = altura / 2 - self.total_altura / 2
		self.rect_principal = pygame.Rect(largura / 2 - self.largura / 2, self.menu_top, self.largura, self.total_altura)

		# Superfice de compra e venda
		self.texto_comprar = self.fonte.render('Comprar', False, 'Black')
		self.texto_vender =  self.fonte.render('Vender', False, 'Black')

	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()

		if keys[pygame.K_ESCAPE]:
			self.alterna_menu()

		if not self.timer.ativo:
			if keys[pygame.K_w]:
				self.indice -= 1
				self.timer.ativado()

			if keys[pygame.K_s]:
				self.indice += 1
				self.timer.ativado()

			if keys[pygame.K_SPACE]:
				self.timer.ativado()

				# Pega o item atual
				item_atual = self.opcoes[self.indice]

				# Vende
				if self.indice <= self.area_de_venda:
					if self.player.item_inventario[item_atual] > 0:
						self.player.item_inventario[item_atual] -= 1
						self.player.dinheiro += Preco_de_venda[item_atual]

				# Compra
				else:
					preco_da_semente = Preco_de_compra[item_atual]
					if self.player.dinheiro >= preco_da_semente:
						self.player.sementes_inventario[item_atual] += 1
						self.player.dinheiro -= Preco_de_compra[item_atual]

		# Roleta de seleção
		if self.indice < 0:
			self.indice = len(self.opcoes) - 1
		if self.indice > len(self.opcoes) - 1:
			self.indice = 0

	def exibindo_entradas(self, texto_surf, montante, top, selecionado):

		# Background
		background_rect = pygame.Rect(self.rect_principal.left, top, self.largura, texto_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.superfice_tela, 'White', background_rect, 0, 4)

		# Texto
		texto_rect = texto_surf.get_rect(midleft = (self.rect_principal.left + 20, background_rect.centery))
		self.superfice_tela.blit(texto_surf, texto_rect)

		# Montante
		montante_surf = self.fonte.render(str(montante), False, 'Black')
		montante_rect = montante_surf.get_rect(midright = (self.rect_principal.right - 20, background_rect.centery))
		self.superfice_tela.blit(montante_surf, montante_rect)

		# Selecionado
		if selecionado:
			pygame.draw.rect(self.superfice_tela, 'green', background_rect, 4, 4)
			if self.indice <= self.area_de_venda:
				posicao_rect = self.texto_vender.get_rect(midleft = (self.rect_principal.right + 20, background_rect.centery))
				background_texto_rect = pygame.Rect(self.rect_principal.right + 13, top, self.texto_vender.get_width() + 10, texto_surf.get_height() + (self.padding * 2) )
				pygame.draw.rect(self.superfice_tela, 'white', background_texto_rect, 0, 4)
				self.superfice_tela.blit(self.texto_vender, posicao_rect)

			else:
				posicao_rect = self.texto_comprar.get_rect(midleft = (self.rect_principal.right + 20, background_rect.centery))
				background_texto_rect = pygame.Rect(self.rect_principal.right + 13, top, self.texto_vender.get_width() + 28, texto_surf.get_height() + (self.padding * 2) )
				pygame.draw.rect(self.superfice_tela, 'white', background_texto_rect, 0, 4)
				self.superfice_tela.blit(self.texto_comprar, posicao_rect)

	def update(self):
		self.input()
		self.tela_dinheiro()

		for indice_texto, texto_surf in enumerate(self.texto_surfs):
			top = self.rect_principal.top + indice_texto * (texto_surf.get_height() + (self.padding * 2) + self.espaco)
			montante_lista = list(self.player.item_inventario.values()) + list(self.player.sementes_inventario.values())
			montante = montante_lista[indice_texto]
			self.exibindo_entradas(texto_surf, montante, top, self.indice == indice_texto)