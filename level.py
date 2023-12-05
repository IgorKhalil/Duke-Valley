import pygame
from configurações import *
from player import Player
from overlay import Overlay
from sprite import Generico
class Level:
    def __init__(self):
        #pega a tela do main
        self.superfice_tela = pygame.display.get_surface()

        # Grupo das sprites
        self.all_sprites = CameraGroup()

        # Chamando o setup
        self.setup()
        self.overlay = Overlay(self.player)
    def setup(self):
        self.player = Player((640, 360), self.all_sprites)
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
            for sprite in self.sprites():
                if sprite.z == camada:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.superfice_tela.blit(sprite.image, offset_rect)