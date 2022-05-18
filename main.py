import pygame
from menu import start_game

# Dados gerais do jogo.
TITULO = 'DOC RUN'

# Inicialização do Pygame.
pygame.init()

# Nome do jogo
pygame.display.set_caption(TITULO)

start_game()
