# Importando as bibliotecas necessárias.
import pygame
from os import path

# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'img')

# Dados gerais do jogo.
TITULO = 'BACKGROUND DOC RUN'
WIDTH = 800  # Largura da tela
HEIGHT = 600  # Altura da tela
FPS = 60  # Frames por segundo
BLACK = (0, 0, 0)  # Define a cor preta para preencher o fundo da tela
BACKGROUND_IMG = 'background_img'

# Define a velocidade do mundo, por camadas (temos 11 camadas)
world_speeds = [0, -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -4, -4.5, -5]


# Carrega todos os assets de uma vez.
def load_assets(img_dir):
    assets = {BACKGROUND_IMG: []}
    for i in range(1, 12):
        background = pygame.image.load(path.join(img_dir, f'background_{i}.png')).convert_alpha()
        # Redimensiona o fundo
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        assets[BACKGROUND_IMG].append(background)
    return assets


def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets
    assets = load_assets(img_dir)

    # Carrega o fundo do jogo
    backgrounds = assets[BACKGROUND_IMG]
    background_rects = []
    for background in backgrounds:
        background_rects.append(background.get_rect())

    PLAYING = 0
    DONE = 1

    state = PLAYING
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)

        # Atualiza a posição de cada camada do fundo e desenha
        for i in range(len(backgrounds)):
            world_speed = world_speeds[i]
            background = backgrounds[i]
            background_rect = background_rects[i]

            # Atualiza a posição da imagem de fundo.
            background_rect.x += world_speed
            # Se o fundo saiu da janela, faz ele voltar para dentro.
            if background_rect.right < 0:
                background_rect.x += background_rect.width
            # Desenha o fundo e uma cópia para a direita.
            # Assumimos que a imagem selecionada ocupa pelo menos o tamanho da janela.
            # Além disso, ela deve ser cíclica, ou seja, o lado esquerdo deve ser continuação do direito.
            screen.blit(background, background_rect)
            # Desenhamos a imagem novamente, mas deslocada da largura da imagem em x.
            background_rect2 = background_rect.copy()
            background_rect2.x += background_rect2.width
            screen.blit(background, background_rect2)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption(TITULO)

# Comando para evitar travamentos.
try:
    game_screen(screen)
finally:
    pygame.quit()