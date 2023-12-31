import pygame
from configurações import *
from suporte import *
from Time import Timer

# criado uma classe para o personagem
class Player(pygame.sprite.Sprite):

    def __init__(self, posicao, grupo, colisao_sprites, arvore_sprites, interacao, camada_solo, alterna_loja):
        super().__init__(grupo)

        self.import_assets()
        self.status = 'down_idle'
        self.indice_frame = 0

        # Setup geral
        self.image = self.animacoes[self.status][self.indice_frame]
        self.rect = self.image.get_rect(center=posicao)
        self.z = Camadas['main']

        # Atributos de movimento
        self.direcao = pygame.math.Vector2()
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.velocidade = 600

        # Colisão
        self.colisao_sprites = colisao_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # Timers
        self.timers = {
            "usando ferramentas": Timer(500, self.usar_ferramentas),
            "escolhendo ferramentas": Timer(200),
            "usando sementes": Timer(500, self.usar_sementes),
            "escolhendo sementes": Timer(200)
        }
        # Ferramentas
        self.ferramentas = ['hoe', 'axe', 'water']
        self.indice_ferramenta = 1
        self.selecionando_ferramenta = self.ferramentas[self.indice_ferramenta]

        # Sementes
        self.sementes = ['corn', 'tomato']
        self.indice_sementes = 0
        self.selecionando_sementes = self.sementes[self.indice_sementes]

        # Inventario
        self.inventory = ['Madeira','Maçã',
            'Trigo','Tomate']

        self.item_inventario = {
            'Madeira': 1,'Maçã': 1,
            'Trigo': 9,'Tomate': 1
        }
        self.sementes_inventario = {
            'Semente de Trigo': 5, 'Semente de Tomate': 5
        }
        self.dinheiro = 200

        # Interações
        self.arvore_sprites = arvore_sprites
        self.interacao = interacao
        self.dormir = False
        self.camada_solo = camada_solo
        self.alterna_loja = alterna_loja

        # Audio
        self.regando = pygame.mixer.Sound('./audio/water.mp3')
        self.regando.set_volume(0.1)

    def obtem_alvo(self):
        self.posicao_alvo = self.rect.center + Offset_ferramentas[self.status.split('_')[0]]

    def usar_ferramentas(self):
        if self.selecionando_ferramenta == 'axe':
            for arvore in self.arvore_sprites.sprites():
                if arvore.rect.collidepoint(self.posicao_alvo):
                    arvore.dano()

        if self.selecionando_ferramenta == 'hoe':
            self.camada_solo.arar(self.posicao_alvo)

        if self.selecionando_ferramenta == 'water':
            self.camada_solo.agua(self.posicao_alvo)
            self.regando.play()

    def usar_sementes(self):
        if self.sementes_inventario['Semente de Trigo' if self.selecionando_sementes == 'corn' else 'Semente de Tomate'] > 0:
            self.camada_solo.semente_planta(self.posicao_alvo, self.selecionando_sementes)
            self.sementes_inventario['Semente de Trigo' if self.selecionando_sementes == 'corn' else 'Semente de Tomate'] -= 1

    # importando as sprites
    def import_assets(self):
        self.animacoes = {'up': [], 'down': [], 'left': [], 'right': [],
                          'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                          'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                          'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                          'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        for animacao in self.animacoes.keys():
            todos_arquivos = './graficos/personagem/' + animacao
            self.animacoes[animacao] = importa_pasta(todos_arquivos)

    # animando o personagem
    def animacao(self, dt):
        self.indice_frame += 4 * dt
        if self.indice_frame >= len(self.animacoes[self.status]):
            self.indice_frame = 0
        self.image = self.animacoes[self.status][int(self.indice_frame)]

    # Recebendo os comandos da teclas
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers["usando ferramentas"].ativo and not self.dormir:
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
                if self.indice_ferramenta == len(self.ferramentas):
                    self.indice_ferramenta = 0
                self.selecionando_ferramenta = self.ferramentas[self.indice_ferramenta]

            # Usando Semenetes
            if keys[pygame.K_LCTRL]:
                for solo_sprite in self.camada_solo.solo_sprites.sprites():
                    if solo_sprite.rect.collidepoint(self.posicao_alvo):
                        x = solo_sprite.rect.x // tile_size
                        y = solo_sprite.rect.y // tile_size
                        if 'P' not in self.camada_solo.grid[y][x]:
                            self.timers["usando sementes"].ativado()
                            self.direcao = pygame.math.Vector2()
                            self.indice_frame = 0

            # Mudando a sementes
            if keys[pygame.K_e] and not self.timers["escolhendo sementes"].ativo:
                self.timers["escolhendo sementes"].ativado()
                self.indice_sementes += 1
                if self.indice_sementes == len(self.sementes):
                    self.indice_sementes = 0
                self.selecionando_sementes = self.sementes[self.indice_sementes]

            # Verificando se está na area de interação
            if keys[pygame.K_RETURN]:
                colisao_interacao = pygame.sprite.spritecollide(self, self.interacao, False)
                if colisao_interacao:
                    if colisao_interacao[0].name == 'Trader':
                        self.alterna_loja()

                    else:
                        self.status = 'right_idle'
                        self.dormir = True

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

    def colisao(self, direcao):
        for sprite in self.colisao_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direcao == 'horizontal':
                        if self.direcao.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direcao.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.posicao.x = self.hitbox.centerx

                    if direcao == 'vertical':
                        if self.direcao.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direcao.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.posicao.y = self.hitbox.centery

    # Gerando o movimento na tela
    def movimento(self, dt: float):
        # utilizando a função normalize do pygame, para ajustar a velocidade do movimento diagonal
        if self.direcao.magnitude() > 0:
            self.direcao = self.direcao.normalize()

        # Movimento horizontal
        self.posicao.x += self.direcao.x * self.velocidade * dt
        self.hitbox.centerx = round(self.posicao.x)
        self.rect.centerx = self.hitbox.centerx
        self.colisao('horizontal')

        # Movimento vertical
        self.posicao.y += self.direcao.y * self.velocidade * dt
        self.hitbox.centery = round(self.posicao.y)
        self.rect.centery = self.hitbox.centery
        self.colisao('vertical')


    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.movimento(dt)
        self.animacao(dt)
        self.obtem_alvo()