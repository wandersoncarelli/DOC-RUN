import pygame
from os import path

# Dados gerais do jogo.
WIDTH = 1024  # Largura da tela
HEIGHT = 768  # Altura da tela
BACKGROUND_IMG = 'background_img'


# Carrega todos os assets do background.
def load_assets(img_dir):
    assets = {BACKGROUND_IMG: []}
    for i in range(1, 12):
        background = pygame.image.load(path.join(img_dir, f'background-{i}.png')).convert_alpha()
        # Redimensiona o fundo
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        assets[BACKGROUND_IMG].append(background)
    return assets
