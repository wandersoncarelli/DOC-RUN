import pygame
import pygame_menu
import game_screen

# Dados gerais do jogo.
TITULO = 'DOC RUN'
WIDTH = 1024  # Largura da tela
HEIGHT = 768  # Altura da tela
FPS = 60  # Frames por segundo
BLACK = (0, 0, 0)  # Define a cor preta para preencher o fundo da tela
WHITE = (255, 255, 255)  # Define a cor branca para os textos que serão apresentados

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def run_game():
    game_screen.game_screen(screen)


def how_to_play():

    # Textos a serem exibidos na tela
    TEXT_STATES = [
        'Os comandos do jogo é muito simples... [aperte espaço para continuar]',
        'Aperte ESPAÇO para "atirar" nas pessoas infectadas e curá-las... [aperte espaço para continuar]',
        'Você pode tentar desviar delas apertando a seta para cima ↑ ... [aperte espaço para continuar]',
        'Não deixe que as pessoas infectadas encostem em você, ou perderá vidas... [aperte espaço para continuar]',
        'Você tem 3 vidas. Bom jogo! [aperte espaço para continuar]'
    ]

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega a fonte padrão do sistema
    font = pygame.font.SysFont('Cambria', 20, True)

    # Vamos utilizar esta variável para controlar o texto a ser mostrado
    text_index = 0
    game = True
    while text_index < len(TEXT_STATES) and game:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                game = False

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_SPACE:
                    text_index += 1

        # Depois de processar os eventos.
        # Atualiza o texto a ser mostrado na tela
        if text_index < len(TEXT_STATES):
            text = TEXT_STATES[text_index]
        else:
            text = ''
        text_image = font.render(text, True, WHITE)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(text_image, (10, 10))

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


def game_credits():
    # Textos a serem exibidos na tela
    TEXT_STATES = [
        'O jogo DOC RUN foi desenvolvido como atividade prática da UNIGRANRIO... '
        '[aperte espaço para continuar]',
        'Os participantes do grupo são... [aperte espaço para continuar]',
        'Wanderson Carelli Pereira - github.com/wandersoncarelli ... [aperte espaço para continuar]',
        'Milena de Oliveira - github.com/xxxx ... [aperte espaço para continuar]',
        'Gabriel Pereira de Rezende - github.com/xxxx ... [aperte espaço para continuar]',
        'Claudio Vinicius Melo Lima - github.com/xxxx ... [aperte espaço para continuar]'
    ]

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega a fonte padrão do sistema
    font = pygame.font.SysFont('Cambria', 20, True)

    # Vamos utilizar esta variável para controlar o texto a ser mostrado
    text_index = 0
    game = True
    while text_index < len(TEXT_STATES) and game:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                game = False

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_SPACE:
                    text_index += 1

        # Depois de processar os eventos.
        # Atualiza o texto a ser mostrado na tela
        if text_index < len(TEXT_STATES):
            text = TEXT_STATES[text_index]
        else:
            text = ''
        text_image = font.render(text, True, WHITE)

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(text_image, (10, 10))

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()


def start_game():
    menu = pygame_menu.Menu('DOC RUN', 400, 300, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Jogar', run_game)
    menu.add.button('Como jogar', how_to_play)
    menu.add.button('Créditos', game_credits)
    menu.add.button('Sair', pygame_menu.events.EXIT)

    menu.mainloop(screen)
