import pygame
from os import path
from random import random
from characters import Player, Citizen
from background import load_assets

# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'img')

FPS = 60  # Frames por segundo
BLACK = (0, 0, 0)  # Define a cor preta para preencher o fundo da tela
BACKGROUND_IMG = 'background_img'

# Define a velocidade do mundo, por camadas (temos 11 camadas).
world_speeds = [0, -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -4, -4.5, -5]

# Define estados possíveis do jogador.
WALKING = 0
JUMPING = 1
FALLING = 2


def game_screen(screen):
    # Variável para contagem para definir tempo de aparição dos citizens
    timer = 0

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega os assets
    assets = load_assets(img_dir)

    # Carrega o fundo do jogo
    backgrounds = assets[BACKGROUND_IMG]
    background_rects = []
    for background in backgrounds:
        background_rects.append(background.get_rect())

    # Cria um grupo para todos os sprites.
    all_sprites = pygame.sprite.Group()

    # Cria os sprites do jogador e dos citizens e adiciona no grupo de sprites
    player = Player(all_sprites)
    citizen = Citizen(all_sprites)

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

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_UP:
                    player.jump()
                    player.state = JUMPING
                if event.key == pygame.K_ESCAPE:
                    state = DONE

        # Faz a contagem de tempo para aparecer citizens
        timer += 1
        # O jogo está rodando a 60 FPS, neste caso, a cada 30 FPS (meio segundo) vai aparecer um novo citizen
        if timer > 30:
            timer = 0
            if random() < 0.5:
                newCitizen = Citizen(all_sprites)

        # Depois de processar os eventos.
        # Atualiza a ação de cada sprite. O grupo chama o método update() de cada Sprite dentro dele.
        all_sprites.update()

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

        # A cada loop, redesenha os sprites.
        all_sprites.draw(screen)
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
