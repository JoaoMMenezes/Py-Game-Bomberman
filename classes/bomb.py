# classes/bomb.py


from classes.explosion import Explosion
import pygame

class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, x, y, range, bomber):
        super().__init__()
        self.game = game
        self.tile_size = game.tile_size

        # Usa a sprite em vez de desenhar
        self.image = self.game.images['bomb']
        self.rect = self.image.get_rect(topleft=(x * self.tile_size, y * self.tile_size))

        self.bomber = bomber
        self.range = range
        # … restante igual …

        
        self.fuse_time = 3000
        self.creation_time = pygame.time.get_ticks()

        # Novo: A bomba começa não-sólida
        self.is_solid = False

    def update(self):
        # Lógica para tornar a bomba sólida
        if not self.is_solid:
            # Checa se o jogador que plantou a bomba NÃO está mais colidindo com ela
            if not self.rect.colliderect(self.bomber.rect):
                self.is_solid = True
                self.game.solid_obstacles.add(self)

        # Lógica da explosão (continua a mesma)
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.fuse_time:
            self.explode()

    def explode(self):
        self.bomber.bomb_limit += 1
        Explosion(self.game, self.rect.x // self.tile_size, self.rect.y // self.tile_size, self.range)
        self.kill()