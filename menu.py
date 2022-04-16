# Importando as bibliotecas necessárias.
import pygame
import pygame_menu
from game_screen import game_screen

# Dados gerais do jogo.
TITULO = 'DOC RUN'
WIDTH = 1024  # Largura da tela
HEIGHT = 768  # Altura da tela

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def start():
    game_screen(screen)


def how_to_play():
    pass


def game_credits():
    pass


def run_game():
    menu = pygame_menu.Menu('DOC RUN', 400, 300, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Jogar', start)
    menu.add.button('Como jogar', how_to_play)
    menu.add.button('Créditos', game_credits)
    menu.add.button('Sair', pygame_menu.events.EXIT)

    menu.mainloop(screen)
