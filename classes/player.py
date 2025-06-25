# classes/player.py

import pygame
from classes.bomb import Bomb

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, keys, icon_path=None):
        """
        :param game: instância de GameManager
        :param x, y: posição inicial em células do grid
        :param name: nome do jogador
        :param keys: dict mapeando ações para teclas ({'up', 'down', 'left', 'right', 'bomb'})
        :param icon_path: caminho opcional para imagem de ícone (PNG/JPG)
        """
        super().__init__()
        self.game = game
        self.name = name
        self.tile_size = game.tile_size

        # Tenta carregar ícone customizado
        surf = None
        if icon_path:
            try:
                surf = pygame.image.load(icon_path).convert_alpha()
            except Exception as e:
                print(f"Falha ao carregar ícone '{icon_path}': {e}")

        # Se carregou corretamente, escala para 48×48px
        if surf:
            self.image = pygame.transform.smoothscale(surf, (48, 48))
        else:
            # Fallback: círculo azul
            size = int(self.tile_size * 0.9)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            center = (size // 2, size // 2)
            pygame.draw.circle(self.image, pygame.Color('blue'), center, size // 2)

        # Rect e posição vetorial para movimento
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y) * self.tile_size
        self.rect.topleft = (self.pos.x, self.pos.y)

        self.keys = keys
        self.speed = 200
        self.vel = pygame.math.Vector2(0, 0)

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
        Calcula vetor de velocidade a partir das teclas pressionadas.
        """
        if not self.alive:
            self.vel = pygame.math.Vector2(0, 0)
            return

        keys = pygame.key.get_pressed()
        self.vel = pygame.math.Vector2(0, 0)
        if keys[self.keys['left']]:
            self.vel.x = -1
        if keys[self.keys['right']]:
            self.vel.x = 1
        if keys[self.keys['up']]:
            self.vel.y = -1
        if keys[self.keys['down']]:
            self.vel.y = 1

        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

    def update(self):
        """
        Atualiza movimento e checa colisões.
        """
        self.handle_input()
        # Movimento no eixo X
        self.pos.x += self.vel.x * self.game.dt
        self.rect.x = round(self.pos.x)
        self.check_collision('x')
        # Movimento no eixo Y
        self.pos.y += self.vel.y * self.game.dt
        self.rect.y = round(self.pos.y)
        self.check_collision('y')

    def check_collision(self, direction):
        """
        Resolve colisões com obstáculos sólidos.
        """
        hits = pygame.sprite.spritecollide(self, self.game.solid_obstacles, False)
        for hit in hits:
            if direction == 'x':
                if self.vel.x > 0:
                    self.rect.right = hit.rect.left
                elif self.vel.x < 0:
                    self.rect.left = hit.rect.right
                self.pos.x = self.rect.x
            elif direction == 'y':
                if self.vel.y > 0:
                    self.rect.bottom = hit.rect.top
                elif self.vel.y < 0:
                    self.rect.top = hit.rect.bottom
                self.pos.y = self.rect.y

    def collect_power_up(self, power_up_type):
        """
        Aplica efeito de power-up.
        """
        if power_up_type == 'bomb_up':
            self.bomb_limit += 1
        elif power_up_type == 'fire_up':
            self.bomb_range += 1
