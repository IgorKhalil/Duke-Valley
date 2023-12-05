import pygame
from configurações import *
from suporte import *
from Time import Timer

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

        #Timers
        self.timers = {
            "usando ferramentas": Timer(350,self.usar_ferramentas),
            "escolhendo ferramentas": Timer(200),
            "usando sementes": Timer(350, self.usar_ferramentas),
            "escolhendo sementes": Timer(200)
        }
        #Ferramentas
        self.ferramentas = ['hoe','axe','water']
        self.indice_ferramenta = 0
        self.selecionando_ferramenta = self.ferramentas[self.indice_ferramenta]

        #Sementes
        self.sementes = ['corn','tomato']
        self.indice_sementes = 0
        self.selecionando_sementes = self.sementes[self.indice_sementes]\

    def usar_ferramentas(self):
        pass
    def usar_sementes(self):
        pass

    # importando as sprites
    def import_assets(self):
        self.animacoes = {'up': [], 'down': [], 'left': [], 'right': [],
                          'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                          'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                          'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                          'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        for animacao in self.animacoes.keys():
            todos_arquivos = './graficos/personagem/' + animacao
            self.animacoes[animacao] = import_folder(todos_arquivos)

    # animando o personagem
    def animado(self, dt):
        self.indice_frame += 4 * dt
        if self.indice_frame >= len(self.animacoes[self.status]):
            self.indice_frame = 0
        self.image = self.animacoes[self.status][int(self.indice_frame)]

    # Recebendo os comandos da teclas
    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["usando ferramentas"].ativo:
            # Direções
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

            # Usando Ferramentas
            if keys[pygame.K_SPACE]:
                self.timers["usando ferramentas"].ativado()
                self.direcao = pygame.math.Vector2()
                self.indice_frame = 0

            # Mudando a Ferramenta
            if keys[pygame.K_q] and not self.timers["escolhendo ferramentas"].ativo:
                self.timers["escolhendo ferramentas"].ativado()
                self.indice_ferramenta += 1
                self.indice_ferramenta = self.indice_ferramenta if self.indice_ferramenta < len(self.ferramentas) else 0
                # if self.indice_ferramenta == len(self.ferramentas):
                #     self.indice_ferramenta = 0
                self.selecionando_ferramenta = self.ferramentas[self.indice_ferramenta]

            #Usando Semenetes
            if keys[pygame.K_LCTRL]:
                self.timers["usando sementes"].ativado()
                self.direcao = pygame.math.Vector2()
                self.indice_frame = 0

             # Mudando a sementes
            if keys[pygame.K_e] and not self.timers["escolhendo sementes"].ativo:
                self.timers["escolhendo sementes"].ativado()
                self.indice_sementes += 1
                self.indice_sementes = self.indice_sementes if self.indice_sementes < len(self.sementes) else 0
                # if self.indice_sementes == len(self.sementes):
                #     self.indice_sementes = 0
                self.selecionando_sementes = self.sementes[self.indice_sementes]

    def get_status(self):

        # Idle
        if self.direcao.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # Usando Ferramentas

        if self.timers["usando ferramentas"].ativo:
            self.status = self.status.split('_')[0] + '_' + self.selecionando_ferramenta

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

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
        self.update_timers()
        self.movimento(dt)
        self.animado(dt)
