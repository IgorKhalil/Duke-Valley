import pygame
from configurações import *

class Level:
    def __init__(self):
        #pega a tela do main
        self.superfice_tela = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()

    def rodando(self,dt):
        self.superfice_tela.fill('black')
        self.all_sprites.draw(self.superfice_tela)
        self.all_sprites.update()
