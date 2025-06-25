# classes/power_up.py

import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, x, y, power_up_type):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.type = power_up_type

        # Seleciona a sprite certa pelo tipo
        if self.type == 'bomb_up':
            key = 'power_bomb'
        else:  # 'fire_up'
            key = 'power_fire'

        self.image = self.game.images[key]
        self.rect = self.image.get_rect(topleft=(x * self.tile_size, y * self.tile_size))
