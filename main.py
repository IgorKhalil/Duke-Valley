import pygame
import sys
from configurações import *
from level import Level
pygame.joystick.init()

'''Olá professor: esse jogo foi inspirado em um jogo que gosto muito, chamdado Stardew Valley.
    Foi utilizado como base um video do canal Clear Code https://youtu.be/T4IX36sP_0c?si=fvsijHKY5gOmgzVa 
    Foi utilizado outro video para a construção da indepêndencia de frames https://www.youtube.com/watch?v=rWtfClpWSb8&t=
    Por fim utilizei como ajuda o livro Introdução ao Desenvolvimento de Jogos em Python com PyGame de Harrison Kinsley e Will McGugan'''
     

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption('Duke Valley')
        self.relogio = pygame.time.Clock()
        self.level = Level()

    def rodando(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            # dt é delta timing, uma variavél que irei utilizar para ter independecia dos frames.
            dt = self.relogio.tick() / 1000
            self.level.rodando(dt)
            pygame.display.update()


if __name__ == '__main__':
    jogo = Jogo()
    jogo.rodando()
