import pygame
from configurações import *
class Generico(pygame.sprite.Sprite):
    def __init__(self, posicao, surf, grupo, z = Camadas['main']):
        super().__init__(grupo)
        self.image = surf
        self.rect = self.image.get_rect(topleft = posicao)
        self.z = z