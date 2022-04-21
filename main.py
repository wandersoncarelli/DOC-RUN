import pygame
from menu import start_game

# Dados gerais do jogo.
TITULO = 'DOC RUN'
WIDTH = 1024  # Largura da tela
HEIGHT = 768  # Altura da tela

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Nome do jogo
pygame.display.set_caption(TITULO)

start_game()
