# classes/power_up.py

import pygame

class PowerUp(pygame.sprite.Sprite):
    """
    Representa um item de power-up que pode aparecer no mapa.
    """
    def __init__(self, game, x, y, power_up_type):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.type = power_up_type

        # Cria uma superfície transparente para a imagem do power-up
        self.image = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.tile_size, y * self.tile_size)

        # Pega o ponto central da *superfície da imagem* para o desenho
        center_point = self.image.get_rect().center

        # Define a cor com base no tipo de power-up para diferenciação visual
        if self.type == 'bomb_up':
            # Power-up de Bomba: um círculo verde
            pygame.draw.circle(self.image, pygame.Color('green'), center_point, int(self.tile_size * 0.4))
            pygame.draw.circle(self.image, pygame.Color('darkgreen'), center_point, int(self.tile_size * 0.4), 3) # Adiciona uma borda
        elif self.type == 'fire_up':
            # Power-up de Fogo: um círculo vermelho
            pygame.draw.circle(self.image, pygame.Color('orange'), center_point, int(self.tile_size * 0.4))
            pygame.draw.circle(self.image, pygame.Color('red'), center_point, int(self.tile_size * 0.4), 3) # Adiciona uma borda