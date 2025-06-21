# classes/explosion.py

import pygame

class Explosion:
    """
    Cria e gerencia os setores da explosão.
    """
    def __init__(self, game, x, y, fire_range):
        self.game = game
        self.x = x
        self.y = y
        self.fire_range = fire_range
        self.create_explosion_sectors()

    def create_explosion_sectors(self):
        # Vetores de direção: [dx, dy]
        directions = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]] # Centro, Direita, Esquerda, Baixo, Cima

        for dx, dy in directions:
            for i in range(self.fire_range):
                # Para o centro, só executa uma vez
                if dx == 0 and dy == 0 and i > 0:
                    continue
                
                check_x = self.x + i * dx
                check_y = self.y + i * dy
                
                # Para se a explosão encontrar um muro
                if self.game.grid[check_y][check_x] == 1:
                    break

                # Cria o setor da explosão
                sector = ExplosionSector(self.game, check_x, check_y)
                self.game.all_sprites.add(sector)
                self.game.explosions.add(sector)
                
                # Para se a explosão encontrar uma caixa (a caixa é destruída pelo loop de colisão)
                if self.game.grid[check_y][check_x] == 2:
                    break

class ExplosionSector(pygame.sprite.Sprite):
    """
    Representa um único tile de fogo da explosão.
    """
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size
        self.image = pygame.Surface((self.tile_size, self.tile_size))
        self.image.fill(pygame.Color('orange'))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * self.tile_size, y * self.tile_size)
        
        self.duration = 500 # Meio segundo
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.duration:
            self.kill() # O setor da explosão desaparece