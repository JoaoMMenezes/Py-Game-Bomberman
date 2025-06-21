# classes/destructible_box.py

import pygame
import random
from classes.power_up import PowerUp

class DestructibleBox(pygame.sprite.Sprite):
    """
    Representa uma caixa destrutível que pode dropar um power-up.
    """
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill(pygame.Color('saddlebrown')) # Uma cor diferente para a caixa
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.tile_size, y * self.tile_size)
        self.grid_pos = (x, y) # Salva a posição no grid

    def kill(self):
        """
        Sobrescreve o método kill para ter a chance de criar um power-up.
        """
        # Chance de 20% de dropar um power-up
        if random.random() < 0.2:
            # Escolhe aleatoriamente entre os dois tipos de power-up
            power_up_type = random.choice(['bomb_up', 'fire_up'])
            
            # 1. CRIA A INSTÂNCIA DO POWER-UP na posição da caixa
            power_up = PowerUp(self.game, self.grid_pos[0], self.grid_pos[1], power_up_type)
            
            # 2. ADICIONA O POWER-UP AOS GRUPOS DE SPRITES
            # Ao adicionar em 'all_sprites', ele passa a ser desenhado na tela
            self.game.all_sprites.add(power_up)
            # Ao adicionar em 'power_ups', ele pode ser detectado para colisão
            self.game.power_ups.add(power_up)

        # Remove a caixa do grid de obstáculos
        self.game.grid[self.grid_pos[1]][self.grid_pos[0]] = 0
        super().kill()