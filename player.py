import pygame
from configurações import *

# criado uma classe para o personagem
class Player(pygame.sprite.Sprite):
    def __init__(self, posicao, group):
        super().__init__(group)

        # Setup geral
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center = posicao)

        # Atributos de movimento
        self.direcao = pygame.math.Vector2()
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.velocidade = 200


    # Recebendo os comandos da teclas
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direcao.y = -1
        elif keys[pygame.K_s]:
            self.direcao.y = 1
        else:
            self.direcao.y = 0

        if keys[pygame.K_d]:
            self.direcao.x = 1
        elif keys[pygame.K_a]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0

    # Gerando o movimento na tela
    def movimento(self, dt):

        # utilizando a função normalize do pygame, para ajustar a velocidade do movimento diagonal
        if self.direcao.magnitude() > 0:
            self.direcao = self.direcao.normalize()

        # Movimento horizontal
        self.posicao.x += self.direcao.x * self.velocidade * dt
        self.rect.centerx = self.posicao.x

        # Movimento vertical
        self.posicao.y += self.direcao.y * self.velocidade * dt
        self.rect.centery = self.posicao.y

    def update(self, dt):
        self.input()
        self.movimento(dt)