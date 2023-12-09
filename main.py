import pygame
import sys
from configurações import *
from level import Level
pygame.joystick.init()

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
