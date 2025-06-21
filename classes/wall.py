import pygame

class Wall(pygame.sprite.Sprite):
    """
    Representa um muro indestrutível no mapa.
    """
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill(pygame.Color('gray'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.tile_size, y * self.tile_size)