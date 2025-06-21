# manager/game_manager.py

import pygame
import sys
from classes.wall import Wall
from classes.player import Player
from manager.db_manager import DBManager
from classes.destructible_box import DestructibleBox

class GameManager:
    def __init__(self, screen, tile_size, player1_name, player2_name):
        self.screen = screen
        self.tile_size = tile_size
        self.clock = pygame.time.Clock()
        self.running = True

        # Define as dimensões do grid para fácil referência
        self.grid_width = 13
        self.grid_height = 13
        
        # Mapa do jogo (0=vazio, 1=muro, 2=caixa destrutível)
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
            [1, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
            [1, 0, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 1],
            [1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # Garante que as áreas de spawn estejam limpas (valor 0)
        self.clear_spawn_area(1, 1)
        self.clear_spawn_area(self.grid_width - 2, self.grid_height - 2)

        # Controles dos jogadores
        player1_keys = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "bomb": pygame.K_SPACE}
        player2_keys = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "bomb": pygame.K_e}

         # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        self.solid_obstacles = pygame.sprite.Group()

        self.create_map()

        # Posição inicial do Jogador 1
        p1_x, p1_y = 1, 1
        # Posição inicial do Jogador 2 (canto oposto)
        p2_x, p2_y = self.grid_width - 2, self.grid_height - 2

        self.player1 = Player(self, p1_x, p1_y, 'blue', player1_keys, player1_name)
        self.player2 = Player(self, p2_x, p2_y, 'red', player2_keys, player2_name)
        
        self.all_sprites.add(self.player1, self.player2)
        self.players.add(self.player1, self.player2)

    def clear_spawn_area(self, x, y):
        """Define os quadrados ao redor de (x, y) como vazios (0)."""
        self.grid[y][x] = 0
        if x + 1 < self.grid_width - 1:
            self.grid[y][x+1] = 0
        if y + 1 < self.grid_height - 1:
            self.grid[y+1][x] = 0

    def create_map(self):
        for j, row in enumerate(self.grid):
            for i, tile in enumerate(row):
                if tile == 1:
                    wall = Wall(self, i, j)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                    self.solid_obstacles.add(wall)
                elif tile == 2:
                    box = DestructibleBox(self, i, j)
                    self.all_sprites.add(box)
                    self.boxes.add(box)
                    self.solid_obstacles.add(box)

    def run(self):
        """ Loop principal do jogo. Encerra quando resta um ou nenhum jogador. """
        winner = None
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0
            self.events()
            self.update()
            self.draw()

            # CONDIÇÃO DE FIM DE JOGO
            if len(self.players) <= 1:
                if len(self.players) == 1:
                    winner = self.players.sprites()[0]
                    # NOVO: Atualiza o ranking quando há um vencedor
                    db = DBManager()
                    db.update_ranking(winner.name)
                self.running = False
        
        # Após o loop do jogo, exibe a tela de vencedor
        self.show_winner_screen(winner)

    def show_winner_screen(self, winner):
        """ Exibe uma tela anunciando o vencedor e aguarda um input para voltar ao menu. """
        # ... (código para criar as fontes e textos continua o mesmo)
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
        small_font = pygame.font.Font(pygame.font.get_default_font(), 24)

        if winner:
            text = f"Vencedor: {winner.name}!"
        else:
            text = "Empate!"
        
        text_surface = font.render(text, True, pygame.Color('white'))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
        
        prompt_surface = small_font.render("Pressione qualquer tecla para voltar ao menu", True, pygame.Color('white'))
        prompt_rect = prompt_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 50))

        # Loop da tela de vencedor
        waiting = True
        while waiting:
            for event in pygame.event.get():
                # Se o usuário fechar a janela, o jogo deve parar completamente
                if event.type == pygame.QUIT:
                    # CORREÇÃO: Apenas encerra todos os loops
                    waiting = False
                    self.running = False # Garante que o loop anterior não continue
                    # Removemos pygame.quit() e sys.exit() daqui
                    
                # Se o usuário pressionar uma tecla, apenas o loop da tela de vencedor para
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            
            self.screen.fill(pygame.Color('black'))
            self.screen.blit(text_surface, text_rect)
            self.screen.blit(prompt_surface, prompt_rect)
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.player1.alive:
                    if event.key == self.player1.keys["bomb"]:
                        self.player1.plant_bomb()
                if self.player2.alive:
                    if event.key == self.player2.keys["bomb"]:
                        self.player2.plant_bomb()

    def update(self):
        self.all_sprites.update()
        
        # Colisão entre explosões e caixas (destrói as caixas)
        # CORREÇÃO APLICADA AQUI: troquei explosions por boxes, e vice-versa, para melhor legibilidade
        pygame.sprite.groupcollide(self.boxes, self.explosions, True, False)
        
        # Colisão entre explosões e jogadores (mata os jogadores)
        for player in self.players:
            hits = pygame.sprite.spritecollide(player, self.explosions, False)
            if hits:
                player.kill()

        # Colisão entre jogadores e power-ups
        # AQUI ESTÁ A CORREÇÃO PRINCIPAL: trocado self.game.power_ups por self.power_ups
        player_powerup_hits = pygame.sprite.groupcollide(self.players, self.power_ups, False, True)
        for player, powerup_list in player_powerup_hits.items():
            for powerup in powerup_list:
                player.collect_power_up(powerup.type)

    def draw(self):
        self.screen.fill((107, 142, 35))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()