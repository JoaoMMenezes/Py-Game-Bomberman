# classes/destructible_box.py

import pygame

class DestructibleBox(pygame.sprite.Sprite):
    """
    Representa uma caixa destrutível no mapa.
    """
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill(pygame.Color('brown'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.tile_size, y * self.tile_size)

    def kill(self):
        # Quando a caixa é destruída, atualiza o grid para 0 (caminho livre)
        grid_x = self.rect.x // self.tile_size
        grid_y = self.rect.y // self.tile_size
        self.game.grid[grid_y][grid_x] = 0
        super().kill()