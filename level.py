import pygame
from configurações import *
from player import Player
from overlay import Overlay
from sprite import Generico, Agua, Vegetacao, Arvore
from pytmx.util_pygame import load_pygame
from suporte import *
class Level:
    def __init__(self):
        #pega a tela do main
        self.superfice_tela = pygame.display.get_surface()

        # Grupo das sprites
        self.all_sprites = CameraGroup()
        self.colisao_sprites = pygame.sprite.Group()

        # Chamando o setup
        self.setup()
        self.overlay = Overlay(self.player)
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
        frames_agua = import_folder('./graficos/agua')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Agua((x * tile_size, y * tile_size),frames_agua,self.all_sprites)

        #vegetação
        for objeto in tmx_data.get_layer_by_name('Decoration'):
            Vegetacao((objeto.x,objeto.y), objeto.image, [self.all_sprites, self.colisao_sprites])

        # Arvores
        for objeto in tmx_data.get_layer_by_name('Trees'):
            Arvore((objeto.x, objeto.y), objeto.image, [self.all_sprites, self.colisao_sprites], objeto.name)

        # Colisão do mapa
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generico((x * tile_size, y * tile_size), pygame.Surface((tile_size,tile_size)), self.colisao_sprites)

        #Personagem
        for objeto in tmx_data.get_layer_by_name('Player'):
            if objeto.name =='Start':
                self.player = Player((objeto.x, objeto.y), self.all_sprites, self.colisao_sprites)
                Generico(posicao = (0,0),
                         surf= pygame.image.load("./graficos/mundo/ground.png").convert_alpha(),
                         grupo = self.all_sprites, z = Camadas['chao'])

    def rodando(self,dt):
        self.superfice_tela.fill('black')
        self.all_sprites.desenho_customizado(self.player)
        self.all_sprites.update(dt)
        self.overlay.tela()

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