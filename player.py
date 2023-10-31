import pygame
from configurações import *
from suporte import *


# criado uma classe para o personagem
class Player(pygame.sprite.Sprite):

    def __init__(self, posicao, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.indice_frame = 0

        # Setup geral
        self.image = self.animacoes[self.status][self.indice_frame]
        self.rect = self.image.get_rect(center=posicao)

        # Atributos de movimento
        self.direcao = pygame.math.Vector2()
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.velocidade = 200

    # importando as sprites
    def import_assets(self):
        self.animacoes = {'up': [], 'down': [], 'left': [], 'right': [],
                          'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                          'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                          'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                          'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        for animacao in self.animacoes.keys():
            full_path = './graficos/personagem/' + animacao
            self.animacoes[animacao] = import_folder(full_path)

    # animando o personagem
    def animado(self, dt):
        self.indice_frame += 4 * dt
        if self.indice_frame >= len(self.animacoes[self.status]):
            self.indice_frame = 0
        self.image = self.animacoes[self.status][int(self.indice_frame)]

    # Recebendo os comandos da teclas
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direcao.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direcao.y = 1
            self.status = 'down'
        else:
            self.direcao.y = 0

        if keys[pygame.K_d]:
            self.direcao.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direcao.x = -1
            self.status = 'left'
        else:
            self.direcao.x = 0

    def get_status(self):
        if self.direcao.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

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
        self.get_status()
        self.movimento(dt)
        self.animado(dt)
