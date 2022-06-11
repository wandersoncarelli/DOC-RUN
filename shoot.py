import pygame
from os import path


# Estabelece a pasta que contem as imagens.
img_dir = path.join(path.dirname(__file__), 'img')


class Shoot(pygame.sprite.Sprite):

    def __init__(self):
        super(Shoot, self).__init__()

        # Carrega o spritesheet
        self.image = pygame.image.load(path.join(img_dir, 'shoot.png')).convert_alpha()

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Redimensiona o tamanho do spritesheet para ficar mais fácil de ver
        self.image = pygame.transform.scale(self.image, (16, 16))

        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Define a velocidade do tiro
        self.speedy = 3

    def update(self, *args):
        self.rect.x += self.speedy

        if self.rect.x > 1024:
            self.kill()
