from pygame.math import Vector2

largura = 1280
altura = 720
tile_size = 64

Overlay_Posicao = {
	'ferramenta' : (40, altura - 15),
	'semente': (70, altura - 5)}

Offset_ferramentas = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

Camadas = {
	'agua': 0,
	'chao': 1,
	'solo': 2,
	'solo molhado': 3,
	'chao molhado': 4,
	'fundo da casa': 5,
	'planta': 6,
	'main': 7,
	'topo da casa': 8,
	'fruta': 9,
	'pingos de chuva': 10
}

PosicaoMaca = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

VelocidadeCrescimento = {
	'corn': 1,
	'tomato': 0.7
}

Preco_de_venda = {
	'Madeira': 4,
	'Maçã': 2,
	'Milho': 10,
	'Tomate': 20
}
Preco_de_compra = {
	'Semente de milho': 4,
	'Semente de Tomate': 5
}