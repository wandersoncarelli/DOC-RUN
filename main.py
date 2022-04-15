# Importando as bibliotecas necessárias.
import pygame
from os import path

# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'img')

# Dados gerais do jogo.
TITULO = 'DOC RUN'
WIDTH = 800  # Largura da tela
HEIGHT = 600  # Altura da tela
FPS = 60  # Frames por segundo
BLACK = (0, 0, 0)  # Define a cor preta para preencher o fundo da tela
BACKGROUND_IMG = 'background_img'

# Define a velocidade do mundo, por camadas (temos 11 camadas)
world_speeds = [0, -0.5, -1, -1.5, -2, -2.5, -3, -3.5, -4, -4.5, -5]

# Define a aceleração da gravidade
GRAVITY = 1
# Define a velocidade inicial no pulo
JUMP_SIZE = 20
# Define a altura do chão
GROUND = 555

# Define estados possíveis do jogador
STILL = 0
WALKING = 1
JUMPING = 2
FALLING = 3


# Carrega todos os assets do background.
def load_assets(img_dir):
    assets = {BACKGROUND_IMG: []}
    for i in range(1, 12):
        background = pygame.image.load(path.join(img_dir, f'background-{i}.png')).convert_alpha()
        # Redimensiona o fundo
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        assets[BACKGROUND_IMG].append(background)
    return assets


# Recebe uma imagem de sprite sheet e retorna uma lista de imagens.
# É necessário definir quantos sprites estão presentes em cada linha e coluna.
# Essa função assume que os sprites no sprite sheet possuem todos o mesmo tamanho.
def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows

    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    return sprites


# Classe Jogador que representa o herói
class Player(pygame.sprite.Sprite):

    # Construtor da classe. O argumento player_sheet é uma imagem contendo um spritesheet.
    def __init__(self, player_sheet):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        player_sheet = pygame.transform.scale(player_sheet, (288, 288))

        # Define sequências de sprites de cada animação
        spritesheet = load_spritesheet(player_sheet, 4, 4)
        self.animations = {
            STILL: spritesheet[0:1],
            WALKING: spritesheet[1:4],
            JUMPING: spritesheet[1:2],
            FALLING: spritesheet[1:2],
        }
        # Define estado atual (define qual animação mostrar)
        # Define se o jogador pode ou não pular
        self.state = STILL
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Armazena as posições em que o herói surge na tela.
        self.rect.left = 100
        self.rect.y = GROUND

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        self.speedy = 0

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 150

    # Metodo que atualiza a posição do personagem
    def update(self):
        self.speedy += GRAVITY
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING
        self.rect.y += self.speedy
        # Se bater no chão, para de cair
        if self.rect.bottom > GROUND:
            # Reposiciona para a posição do chão
            self.rect.bottom = GROUND
            # Para de cair
            self.speedy = 0
            # Atualiza o estado para parado
            self.state = WALKING

        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0

            # Armazena a posição do herói na imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center

    # Método que faz o personagem pular
    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL or self.state == WALKING:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING


def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets
    assets = load_assets(img_dir)
    # Carrega spritesheet
    player_sheet = pygame.image.load(path.join(img_dir, 'player.png')).convert_alpha()

    # Carrega o fundo do jogo
    backgrounds = assets[BACKGROUND_IMG]
    background_rects = []
    for background in backgrounds:
        background_rects.append(background.get_rect())

    # Cria Sprite do jogador
    player = Player(player_sheet)
    # Cria um grupo de todos os sprites e adiciona o jogador.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

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
                if event.key == pygame.K_LEFT:
                    player.state = STILL
                elif event.key == pygame.K_RIGHT:
                    player.state = WALKING
                elif event.key == pygame.K_UP:
                    player.jump()
                    player.state = JUMPING

        # Depois de processar os eventos.
        # Atualiza a ação de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
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

        # A cada loop, redesenha os sprites do jogador
        all_sprites.draw(screen)
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
