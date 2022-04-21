import pygame
from os import path
from random import randint, random

# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'img')

# Define a aceleração da gravidade
GRAVITY = 1
# Define a velocidade inicial no pulo
JUMP_SIZE = 20
# Define a altura do chão
GROUND = 710

# Define estados possíveis do jogador
WALKING = 0
JUMPING = 1
FALLING = 2
INFECTED = 3
HEALED = 4


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


# Classe Player que representa o herói
class Player(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, *groups):
        super().__init__(*groups)

        # Carrega o spritesheet
        player_sheet = pygame.image.load(path.join(img_dir, 'characters.png')).convert_alpha()

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        player_sheet = pygame.transform.scale(player_sheet, (288, 288))

        # Define sequências de sprites de cada animação
        spritesheet = load_spritesheet(player_sheet, 4, 4)
        self.animations = {
            WALKING: spritesheet[0:4],
            JUMPING: spritesheet[3:4],
            FALLING: spritesheet[3:4],
        }
        # Define estado atual (define qual animação mostrar)
        # Define se o jogador pode ou não pular
        self.state = WALKING
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
        if self.state == WALKING:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING


# Classe Citizen que representa as pessoas doentes ou curadas
class Citizen(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, *groups):
        super().__init__(*groups)

        # Carrega o spritesheet
        citizen_sheet = pygame.image.load(path.join(img_dir, 'characters.png')).convert_alpha()

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        citizen_sheet = pygame.transform.scale(citizen_sheet, (288, 288))

        # Define sequências de sprites de cada animação
        spritesheet = load_spritesheet(citizen_sheet, 4, 4)
        self.animations = {
            INFECTED: spritesheet[4:8],
            HEALED: spritesheet[8:12],
        }
        # Define estado atual (define qual animação mostrar)
        self.state = INFECTED
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Armazena as posições em que o herói surge na tela.
        self.rect.x = 1024 + randint(1, 400)
        self.rect.y = 637

        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Define a velocidade de movimento
        self.speedy = 5 + random() * 2

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 150

    # Metodo que atualiza a posição do personagem
    def update(self, *args):

        # Define a velocidade de movimento no eixo X
        self.rect.x -= self.speedy

        # ------------ VERIFICAR CÓDIGO NÃO FUNCIONAL -----------------------
        # Verifica se o citizen saiu do campo de visão e elimina o spritesheet
        '''if self.rect.right < 0:
            self.kill()'''

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
