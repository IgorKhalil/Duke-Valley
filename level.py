import pygame
from configurações import *
from player import Player
from overlay import Overlay
from sprite import Generico, Agua, Vegetacao, Arvore, Interacao, Particulas
from pytmx.util_pygame import load_pygame
from suporte import *
from transicao import Transicao
from solo import CamadaSolo
from ceu import Chuva, Ceu
from random import randint
from menu import Menu

class Level:
    def __init__(self):
        #pega a tela do main
        self.superfice_tela = pygame.display.get_surface()

        # Grupo das sprites
        self.all_sprites = CameraGroup()
        self.colisao_sprites = pygame.sprite.Group()
        self.arvore_sprites = pygame.sprite.Group()
        self.interacao_sprites = pygame.sprite.Group()

        self.camada_solo = CamadaSolo(self.all_sprites, self.colisao_sprites)
       # Chamando o setup
        self.setup()
        self.overlay = Overlay(self.player)
        self.transicao = Transicao(self.reset, self.player)

        # Ceu
        self.ceu = Ceu()
        self.chuva = Chuva(self.all_sprites)
        self.chovendo = randint(0,12) > 8
        self.camada_solo.chovendo = self.chovendo

        # Loja
        self.menu = Menu(self.player, self.alterna_loja)
        self.loja_ativa = False

        # Audio
        self.sucesso = pygame.mixer.Sound('./audio/success.wav')
        self.sucesso.set_volume(0.03)

        self.musica = pygame.mixer.Sound('./audio/music.mp3')
        self.musica.set_volume(0.02)
        self.musica.play(-1)

    def setup(self):
        tmx_data = load_pygame('./data/map.tmx')

        #parte de baixo da casa
        for camada in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
                Generico((x * tile_size, y * tile_size), surf, self.all_sprites, Camadas['fundo da casa'])

        #parte de cima da casa
        for camada in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(camada).tiles():
                Generico((x * tile_size, y * tile_size), surf, self.all_sprites)

        #cerca no mapa
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generico((x * tile_size, y * tile_size), surf, [self.all_sprites, self.colisao_sprites])

        #agua no mapa
        frames_agua = importa_pasta('./graficos/agua')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Agua((x * tile_size, y * tile_size),frames_agua,self.all_sprites)

        #vegetação
        for objeto in tmx_data.get_layer_by_name('Decoration'):
            Vegetacao((objeto.x,objeto.y), objeto.image, [self.all_sprites, self.colisao_sprites])

        # Arvores
        for objeto in tmx_data.get_layer_by_name('Trees'):
            Arvore((objeto.x, objeto.y), objeto.image, [self.all_sprites, self.colisao_sprites, self.arvore_sprites],
                   objeto.name, self.all_sprites, player_add = self.player_add)

        # Colisão do mapa
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generico((x * tile_size, y * tile_size), pygame.Surface((tile_size,tile_size)), self.colisao_sprites)

        #Personagem
        for objeto in tmx_data.get_layer_by_name('Player'):
            if objeto.name =='Start':
                self.player = Player((objeto.x, objeto.y), self.all_sprites,
                                     self.colisao_sprites, self.arvore_sprites,
                                     self.interacao_sprites, self.camada_solo,
                                     self.alterna_loja)

            if objeto.name == 'Bed':
                Interacao((objeto.x, objeto.y), (objeto.width, objeto.height), self.interacao_sprites, objeto.name)

            if objeto.name == 'Trader':
                Interacao((objeto.x, objeto.y), (objeto.width, objeto.height), self.interacao_sprites, objeto.name)


        Generico(posicao = (0,0), surf= pygame.image.load("./graficos/mundo/ground.png").convert_alpha(),
                 grupo = self.all_sprites, z = Camadas['chao'])

    def player_add(self, item, montante):
        self.player.item_inventario[item] += montante
        self.sucesso.play()

    def alterna_loja(self):
        self.loja_ativa = not self.loja_ativa

    def reset(self):

        # Plantas
        self.camada_solo.update_plantas()
        self.ceu.cor_inicial = [255,255,255]

        # Reseta as maças nas arvores
        for arvore in self.arvore_sprites.sprites():
            for maca in arvore.maca_sprites.sprites():
                maca.kill()
            arvore.cria_fruta(self.all_sprites)
            #arvore.reseta_arvore() a self.image = surf e kill toco do grupo revisar

        # remove a agua
        self.camada_solo.remove_agua()

        # Molhando com a chuva
        self.chovendo = randint(0, 12) > 8
        self.camada_solo.chovendo = self.chovendo
        if self.chovendo:
            self.camada_solo.choveu_molhou()

    def colisao_planta(self):
        if self.camada_solo.planta_sprites:
            for planta in self.camada_solo.planta_sprites.sprites():
                if planta.maduro and planta.rect.colliderect(self.player.hitbox):
                    self.player_add('Trigo' if planta.tipo_planta == 'corn' else 'Tomate', randint(1,4))
                    planta.kill()
                    Particulas(planta.rect.topleft, planta.image, self.all_sprites, z = Camadas['main'])
                    self.camada_solo.grid[planta.rect.centery // tile_size][planta.rect.centerx // tile_size].remove('P')

    def verifica_semente(self):

        if self.camada_solo.semente_planta == 'True':
            self.player.sementes_inventario['Semente de Trigo' if self.player.selecionando_sementes == 'corn' else 'Semente de Tomate'] -= 1


    def rodando(self,dt):

        # Desenhando na tela
        self.superfice_tela.fill('black')
        self.all_sprites.desenho_customizado(self.player)

        # Updates
        if self.loja_ativa:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.colisao_planta()

        if self.player.dormir:
            self.transicao.play()
        # mudança de Céu (Noite e Chuva)
        self.ceu.tela(dt)
        if self.chovendo and not self.loja_ativa:
            self.chuva.update()

        # Transição Overlay
        self.overlay.tela()
        if not self.loja_ativa:
            self.overlay.overlay_inventario()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.superfice_tela = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def desenho_customizado(self, player):
        self.offset.x = player.rect.centerx - largura/2
        self.offset.y = player.rect.centery - altura/2

        for camada in Camadas.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == camada:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.superfice_tela.blit(sprite.image, offset_rect)