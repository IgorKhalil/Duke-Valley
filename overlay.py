import pygame
from configurações import *


class Overlay:
    def __int__(self,player):

        self.superfice_tela = pygame.display.get_surface()
        self.player = player

        local_overlay = './graficos/overlay/'
        self.ferramentas_superf = {ferramenta: pygame.image.load(f'{local_overlay}{ferramenta}.png').convert_alpha() for ferramenta in player.ferramentas}
        self.sementes_superf = {semente: pygame.image.load(f'{local_overlay}{semente}.png').convert_alpha() for semente in player.sementes}
        print(self.ferramentas_superf)
        print(self.sementes_superf)
    def tela(self):

        ferramenta_superf = self.ferramentas_superf[self.player.selecionando_ferramenta]
        ferramenta_rect = ferramenta_superf.get_rect(midbottom = OVERLAY_POSICAO['ferramenta'])
        self.superfice_tela.blit(ferramenta_superf,ferramenta_rect)

        semente_superf = self.sementes_superf[self.player.selecionando_sementes]
        semente_rect = semente_superf.get_rect(midbottom=OVERLAY_POSICAO['semente'])
        self.superfice_tela.blit(semente_superf, semente_rect)