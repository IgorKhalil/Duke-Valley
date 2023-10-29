import pygame
from configurações import *
from player import Player

class Level:
    def __init__(self):
        #pega a tela do main
        self.superfice_tela = pygame.display.get_surface()

        # Grupo das sprites
        self.all_sprites = pygame.sprite.Group()

        # Chamando o setup
        self.setup()

    def setup(self):
        self.player = Player((640,360), self.all_sprites)

    def rodando(self,dt):
        self.superfice_tela.fill('black')
        self.all_sprites.draw(self.superfice_tela)
        self.all_sprites.update(dt)
