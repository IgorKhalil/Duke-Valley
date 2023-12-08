import pygame
from configurações import *


class Transicao:
    def __init__(self, reset, player):

        # setup
        self.superfice_tela = pygame.display.get_surface()
        self.reset = reset
        self.player = player

        # overlay image
        self.image = pygame.Surface((largura, altura))
        self.cor = 255
        self.velocidade = -2

    def play(self):
        self.cor += self.velocidade
        if self.cor <= 0:
            self.velocidade *= -1
            self.cor = 0
            self.reset()
        if self.cor > 255:
            self.cor = 255
            self.player.dormir = False
            self.velocidade = -2

        self.image.fill((self.cor, self.cor, self.cor))
        self.superfice_tela.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)