# classes/player.py

import pygame
from classes.bomb import Bomb

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, color, keys, name):
        super().__init__()
        self.game = game
        self.name = name
        self.tile_size = game.tile_size
        self.image = pygame.Surface((self.tile_size * 0.9, self.tile_size * 0.9))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect()
        
        # Posição vetorial para movimento suave (float)
        self.pos = pygame.math.Vector2(x, y) * self.tile_size
        # Posição do retângulo para renderização e colisão (int)
        self.rect.topleft = self.pos

        self.keys = keys
        self.speed = 200
        self.vel = pygame.math.Vector2(0, 0) # Vetor de velocidade

        self.bomb_limit = 1
        self.bomb_range = 2
        self.alive = True

    def plant_bomb(self):
        if self.bomb_limit > 0:
            grid_x = self.rect.centerx // self.tile_size
            grid_y = self.rect.centery // self.tile_size

            bomb = Bomb(self.game, grid_x, grid_y, self.bomb_range, self)
            self.game.all_sprites.add(bomb)
            self.game.bombs.add(bomb)
            
            self.bomb_limit -= 1

    def kill(self):
        self.alive = False
        super().kill()

    def handle_input(self):
        """
        Calcula o vetor de velocidade com base nas teclas pressionadas.
        """
        if not self.alive:
            self.vel = pygame.math.Vector2(0, 0)
            return

        self.vel = pygame.math.Vector2(0, 0)
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[self.keys["left"]]:
            self.vel.x = -1
        if keys_pressed[self.keys["right"]]:
            self.vel.x = 1
        if keys_pressed[self.keys["up"]]:
            self.vel.y = -1
        if keys_pressed[self.keys["down"]]:
            self.vel.y = 1
        
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

    def update(self):
        """
        Atualiza o estado do jogador: processa input, move e checa colisões.
        """
        self.handle_input()
        
        # Move e checa colisão no eixo X
        self.pos.x += self.vel.x * self.game.dt
        self.rect.x = round(self.pos.x)
        self.check_collision('x')

        # Move e checa colisão no eixo Y
        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = round(self.pos.y)
        self.check_collision('y')

    def check_collision(self, direction):
        """
        Verifica e resolve colisões com obstáculos sólidos.
        A resolução depende da direção do movimento do jogador.
        """
        hits = pygame.sprite.spritecollide(self, self.game.solid_obstacles, False)
        
        if direction == 'x':
            for hit in hits:
                # Se estava se movendo para a direita na colisão
                if self.vel.x > 0:
                    self.rect.right = hit.rect.left
                # Se estava se movendo para a esquerda na colisão
                elif self.vel.x < 0:
                    self.rect.left = hit.rect.right
                # Atualiza a posição vetorial (float) com base na posição do rect (int)
                self.pos.x = self.rect.x

        if direction == 'y':
            for hit in hits:
                # Se estava se movendo para baixo na colisão
                if self.vel.y > 0:
                    self.rect.bottom = hit.rect.top
                # Se estava se movendo para cima na colisão
                elif self.vel.y < 0:
                    self.rect.top = hit.rect.bottom
                # Atualiza a posição vetorial (float) com base na posição do rect (int)
                self.pos.y = self.rect.y
    
    def collect_power_up(self, power_up_type):
        """
        Aplica o efeito de um power-up ao jogador.
        """
        if power_up_type == 'bomb_up':
            self.bomb_limit += 1
            print(f"Jogador coletou BOMBA EXTRA! Limite atual: {self.bomb_limit}")
        elif power_up_type == 'fire_up':
            self.bomb_range += 1
            print(f"Jogador coletou FOGO EXTRA! Alcance atual: {self.bomb_range}")