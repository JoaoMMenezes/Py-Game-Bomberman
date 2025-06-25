import os
import sys
import pygame
from classes.wall import Wall
from classes.player import Player
from classes.destructible_box import DestructibleBox
from manager.db_manager import DBManager

class GameManager:
    def __init__(self, screen, tile_size, player1_name, player2_name, icons=None):
        """
        Inicializa o jogo, carrega sprites e players com ícones
        :param screen: janela do pygame
        :param tile_size: tamanho de cada célula
        :param player1_name: nome do jogador 1
        :param player2_name: nome do jogador 2
        :param icons: dict {'player1': path1, 'player2': path2}
        """
        self.screen    = screen
        self.tile_size = tile_size
        self.clock     = pygame.time.Clock()
        self.running   = True

        # DB Manager para ranking
        self.db_manager = DBManager()

        # Carrega imagens
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        img_folder = os.path.join(base_path, 'images')
        assets = {
            'wall': 'wall.png',
            'box': 'crate.png',
            'bomb': 'bomb.png',
            'power_bomb': 'powerup_bomb.png',
            'power_fire': 'powerup_fire.png',
            'explosion': 'explosion.png'
        }
        self.images = {}
        for key, fname in assets.items():
            path = os.path.join(img_folder, fname)
            surf = pygame.image.load(path).convert_alpha()
            self.images[key] = pygame.transform.scale(surf, (self.tile_size, self.tile_size))

        # Ícones customizados
        self.icons = icons or {'player1': None, 'player2': None}

        # Define dimensões do grid
        self.grid_width  = 13
        self.grid_height = 13

        # Mapa do jogo (0=vazio, 1=wall, 2=box)
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

        # Garante áreas de spawn limpas
        self.clear_spawn_area(1, 1)
        self.clear_spawn_area(self.grid_width - 2, self.grid_height - 2)

        # Teclas
        player1_keys = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                        "left": pygame.K_LEFT, "right": pygame.K_RIGHT,
                        "bomb": pygame.K_SPACE}
        player2_keys = {"up": pygame.K_w, "down": pygame.K_s,
                        "left": pygame.K_a, "right": pygame.K_d,
                        "bomb": pygame.K_e}

        # Grupos de sprites
        self.all_sprites     = pygame.sprite.Group()
        self.players         = pygame.sprite.Group()
        self.walls           = pygame.sprite.Group()
        self.boxes           = pygame.sprite.Group()
        self.bombs           = pygame.sprite.Group()
        self.explosions      = pygame.sprite.Group()
        self.power_ups       = pygame.sprite.Group()
        self.solid_obstacles = pygame.sprite.Group()

        # Cria o mapa
        self.create_map()

        # Instancia jogadores
        p1_x, p1_y = 1, 1
        p2_x, p2_y = self.grid_width - 2, self.grid_height - 2
        self.player1 = Player(self, p1_x, p1_y, player1_name, player1_keys, icon_path=self.icons.get('player1'))
        self.player2 = Player(self, p2_x, p2_y, player2_name, player2_keys, icon_path=self.icons.get('player2'))
        self.all_sprites.add(self.player1, self.player2)
        self.players.add(self.player1, self.player2)

    def create_map(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    wall = Wall(self, x, y)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                    self.solid_obstacles.add(wall)
                elif cell == 2:
                    box = DestructibleBox(self, x, y)
                    self.all_sprites.add(box)
                    self.boxes.add(box)
                    self.solid_obstacles.add(box)

    def clear_spawn_area(self, x, y):
        """Libera a célula de spawn"""
        if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
            self.grid[y][x] = 0

    def run(self):
        winner = None
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0
            self.events()
            self.update()
            self.draw()

            if len(self.players) <= 1:
                if len(self.players) == 1:
                    winner = self.players.sprites()[0]
                    self.db_manager.update_ranking(winner.name)
                self.running = False

        self.show_winner_screen(winner)


    def show_winner_screen(self, winner):
        """
        Exibe uma tela de fim de jogo com o vencedor ou empate e um botão
        para retornar ao menu principal, sem fechar o programa.
        """
        # Fontes
        font = pygame.font.Font(None, 50)
        button_font = pygame.font.Font(None, 36)
        # Dimensões da tela
        w, h = self.screen.get_size()

        # Texto do resultado
        if winner:
            text = f"Vencedor: {winner.name}!"
        else:
            text = "Empate!"
        text_surf = font.render(text, True, pygame.Color('white'))
        text_rect = text_surf.get_rect(center=(w/2, h/2 - 100))

        # Prepara o botão "Menu Principal"
        btn_text = "Menu Principal"
        btn_surf = button_font.render(btn_text, True, pygame.Color('white'))
        btn_rect = btn_surf.get_rect(center=(w/2, h/2 + 50))
        btn_bg = pygame.Rect(
            btn_rect.left  - 10,
            btn_rect.top   - 10,
            btn_rect.width + 20,
            btn_rect.height+ 20
        )

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Fecha tudo após sair
                    waiting = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Se clicou no botão, volta ao menu
                    if btn_bg.collidepoint(event.pos):
                        waiting = False

            # Desenha a tela de fim
            self.screen.fill(pygame.Color('black'))
            self.screen.blit(text_surf, text_rect)
            pygame.draw.rect(self.screen, pygame.Color('gray'), btn_bg)
            self.screen.blit(btn_surf, btn_rect)
            pygame.display.flip()

        # Limpa eventos pendentes (p.ex. o clique) antes de voltar ao menu
        pygame.event.clear()

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

    def show_winner_screen(self, winner):
        """ Exibe uma tela com o vencedor/empate e um botão para voltar ao menu. """
        font = pygame.font.Font(None, 50)
        button_font = pygame.font.Font(None, 36)
        w, h = self.screen.get_size()

        # Texto do resultado
        if winner:
            text = f"Vencedor: {winner.name}!"
        else:
            text = "Empate!"
        text_surf = font.render(text, True, pygame.Color('white'))
        text_rect = text_surf.get_rect(center=(w/2, h/2 - 100))

        # Botão “Menu Principal”
        btn_text = "Menu Principal"
        btn_surf = button_font.render(btn_text, True, pygame.Color('white'))
        btn_rect = btn_surf.get_rect(center=(w/2, h/2 + 50))
        btn_bg = pygame.Rect(
            btn_rect.left - 10,
            btn_rect.top  - 10,
            btn_rect.width  + 20,
            btn_rect.height + 20
        )

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False  # garante que o loop principal não reinicie
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # se clicou dentro do botão, sai da tela de fim
                    if btn_bg.collidepoint(event.pos):
                        waiting = False

            # Desenho
            self.screen.fill(pygame.Color('black'))
            self.screen.blit(text_surf, text_rect)
            pygame.draw.rect(self.screen, pygame.Color('gray'), btn_bg)
            self.screen.blit(btn_surf, btn_rect)
            pygame.display.flip()