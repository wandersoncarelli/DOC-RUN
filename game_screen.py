import pygame
from os import path
from random import random
from characters import Player, Citizen
from background import load_assets
from shoot import Shoot

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
INFECTED = 3
HEALED = 4


def game_screen(screen):

    # Variável para definir a quantidade de vidas do jogador
    lives = 5

    # Variável para contagem para definir tempo de aparição dos citizens
    timer = 40

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega os assets do background
    assets = load_assets(img_dir)

    # Carrega o background do jogo
    backgrounds = assets[BACKGROUND_IMG]
    background_rects = []
    for background in backgrounds:
        background_rects.append(background.get_rect())

    # Variável para definir o jogador
    player = Player()
    shoot = Shoot()

    # Cria os grupos de sprites
    citizensGroup = pygame.sprite.Group()
    shootsGroup = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Adiciona o player no principal grupo de sprites
    all_sprites.add(player)

    PLAYING = 0
    DONE = 1

    # Variável para definir o estado atual do citizen
    citizen_state = INFECTED

    state = PLAYING
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Faz a contagem de tempo para aparecer citizens
        timer += 1
        # O jogo está rodando a 60 FPS, neste caso, a cada 30 FPS (meio segundo) vai aparecer um novo citizen
        if timer > 30:
            timer = 0
            if random() < 0.5:
                new_citizen = Citizen()
                citizensGroup.add(new_citizen)
                all_sprites.add(new_citizen)

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
                if event.key == pygame.K_SPACE:
                    shoot = Shoot()
                    shoot.rect.center = player.rect.center
                    shootsGroup.add(shoot)
                    all_sprites.add(shoot)

        # CÓDIGO ABAIXO FUNCIONANDO PARCIALMENTE, POSSUI BUG EM QUE SOMENTE O ÚLTIMO TIRO MUDA O STATE
        if citizen_state == INFECTED:
            citizens_collisions = pygame.sprite.groupcollide(shootsGroup, citizensGroup, True, False)
            if citizens_collisions:
                heal_collisions = pygame.sprite.spritecollide(shoot, citizensGroup, False)
                for citizen in heal_collisions:
                    citizen.state = HEALED
                    citizen.remove(citizensGroup)

            player_collisions = pygame.sprite.spritecollide(player, citizensGroup, True)
            if player_collisions:
                lives -= 1
                print(lives)
                if lives == 0:
                    print('Game over!')
                    state = DONE

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
