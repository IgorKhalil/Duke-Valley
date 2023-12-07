import pygame
from configurações import *
from random import randint, choice
from Time import Timer


class Generico(pygame.sprite.Sprite):
    def __init__(self, posicao, surf, grupo, z=Camadas['main']):
        super().__init__(grupo)
        self.image = surf
        self.rect = self.image.get_rect(topleft=posicao)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)


class Agua(Generico):
    def __init__(self, posicao, frames, grupo):
        self.frames = frames
        self.indice_frames = 0

        super().__init__(
            posicao=posicao,
            surf=self.frames[self.indice_frames],
            grupo=grupo,
            z=Camadas['agua'])

    def animacao(self, dt):
        self.indice_frames += 5 * dt
        if self.indice_frames >= len(self.frames):
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]

    def update(self, dt):
        self.animacao(dt)


class Vegetacao(Generico):
    def __int__(self, posicao, surf, grupo):
        super().__int__(posicao, surf, grupo)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.heigth * 0.9)

class Particulas(Generico):
    def __init__(self, posicao, surf, grupo, z, duracao=200):
        super().__init__(posicao, surf, grupo, z)
        self.tempo_inicial = pygame.time.get_ticks()
        self.duracao = duracao

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_inicial > self.duracao:
            self.kill()


class Maca(Generico):
    def __init__(self, posicao, surf, grupo):
        super().__init__(posicao, surf, grupo, Camadas['fruta'])


class Arvore(Generico):
    def __init__(self, posicao: tuple[float, float], surf, grupo, name, grupo_geral) -> None:
        super().__init__(posicao, surf, grupo)

        # atributos
        self.vida = 5
        self.viva = True
        local_toco = f'./graficos/toco/{"small" if name == "Small" else "large"}.png'
        self.toco_surf = pygame.image.load(local_toco).convert_alpha()
        self.invul_timer = Timer(200)

        # maçãs
        self.maca_surf = pygame.image.load('./graficos/frutas/apple.png')
        self.maca_posicao = PosicaoMaca[name]
        self.maca_sprites = pygame.sprite.Group()
        self.cria_fruta(grupo_geral)
        self.grupo_geral = grupo_geral

    def dano(self) -> int:

        if self.viva:
            self.vida -= 1

            if len(self.maca_sprites.sprites()) > 0:
                maca_aleatoria = choice(self.maca_sprites.sprites())
                Particulas(maca_aleatoria.rect.topleft, maca_aleatoria.image, self.grupo_geral, z=Camadas['fruta'])
                maca_aleatoria.kill()

    def verifica_morte(self):
        if self.vida <= 0:
            Particulas(self.rect.topleft, self.image, self.grupo_geral, Camadas['fruta'], 500)
            self.image = self.toco_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.viva = False

    def update(self, dt):
        if self.viva:
            self.verifica_morte()

    def cria_fruta(self, geral_group: dict) -> None:
        for posicao in self.maca_posicao:
            if randint(0, 10) < 2:
                x = posicao[0] + self.rect.left
                y = posicao[1] + self.rect.top
                grupo = [self.maca_sprites],geral_group
                maca = Maca(
                    posicao=(x, y),
                    surf=self.maca_surf,
                    grupo=grupo)
                geral_group.add(maca)
