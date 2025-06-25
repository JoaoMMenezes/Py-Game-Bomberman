import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size

        self.image = self.game.images['wall']
        self.rect = self.image.get_rect(topleft=(x * self.tile_size, y * self.tile_size))
    