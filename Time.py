import pygame

class Timer:
	def __init__(self,duracao,func = None):
		self.duracao = duracao
		self.func = func
		self.start_time = 0
		self.ativo = False

	def ativado(self):
		self.ativo = True
		self.start_time = pygame.time.get_ticks()

	def desativado(self):
		self.ativo = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duracao:
			if self.func and self.start_time != 0:
				self.func()
			self.desativado()