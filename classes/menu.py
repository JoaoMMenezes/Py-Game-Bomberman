# classes/menu.py

import sys
import os
import pygame
import pygame_menu
from manager.db_manager import DBManager
from manager.game_manager import GameManager

class Menu:
    """
    Gerencia todo o fluxo de menus:
      - Menu Principal
      - Instrucoes
      - Insercao de Nomes e Selecao de Icones
      - Partida
      - Ranking
    """
    def __init__(self, screen):
        """
        Inicializa todos os menus do jogo com tema retro anos 80:
          - Menu Principal
          - Menu de Instrucoes
          - Menu de Insercao de Nomes e Selecao de Icones
          - Menu de Ranking
        :param screen: surface principal do Pygame
        """
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        # Dados dos jogadores
        self.player_names = {'player1': 'Jogador 1', 'player2': 'Jogador 2'}
        self.player_icons = {'player1': None, 'player2': None}
        self.db_manager = DBManager()

        # Tema estilo anos 80 neon (tamanhos ajustados)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        fonts_path = os.path.join(base_path, 'images', 'fonts')
        arcade_ttf = os.path.join(fonts_path, 'arcade_font.ttf')
        pixel_font = pygame_menu.font.FONT_8BIT if not os.path.exists(arcade_ttf) else arcade_ttf
        # Imagem de fundo arcade, se existir
        bg_path = os.path.join(base_path, 'images', 'bg_arcade.png')
        background = pygame_menu.BaseImage(image_path=bg_path) if os.path.exists(bg_path) else (0, 0, 0)
        theme = pygame_menu.Theme(
            background_color=background,
            title_background_color=(20, 0, 60),
            title_font=pixel_font,
            title_font_size=48,
            title_font_color=(0, 255, 255),
            widget_font=pixel_font,
            widget_font_size=24,
            widget_font_color=(255, 0, 255),
            widget_selection_effect=pygame_menu.widgets.HighlightSelection(),
            widget_background_color=(10, 10, 10),
            widget_border_color=(255, 0, 255),
            widget_border_width=2,
            widget_margin=(20, 10)
        )
        # Tema secundario menor
        sub_theme = theme.copy()
        sub_theme.title_font_size = 28
        sub_theme.widget_font_size = 18

        # Criação dos menus
        self.main_menu = pygame_menu.Menu(
            title='BOMBERMAN',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.instructions_menu = pygame_menu.Menu(
            title='INSTRUCOES',
            width=self.screen_width,
            height=self.screen_height,
            theme=sub_theme
        )
        self.name_input_menu = pygame_menu.Menu(
            title='INSIRA OS NOMES',
            width=self.screen_width,
            height=self.screen_height,
            theme=sub_theme
        )
        self.ranking_menu = pygame_menu.Menu(
            title='RANKING',
            width=self.screen_width,
            height=self.screen_height,
            theme=sub_theme
        )

        # Configuração dos menus
        self._setup_main_menu()
        self._setup_instructions_menu()
        self._setup_name_input_menu()
        self._setup_ranking_menu()

    def _setup_main_menu(self):
        """Configura o menu principal"""
        self.main_menu.add.button('Jogar', self.name_input_menu)
        self.main_menu.add.button('Instrucoes', self.instructions_menu)
        self.main_menu.add.button('Ranking', self.ranking_menu)
        self.main_menu.add.button('Sair', pygame_menu.events.EXIT)

    def _setup_instructions_menu(self):
        """Configura o menu de instrucoes"""
        text = (
            "Use suas bombas para destruir caixas e derrotar seu oponente!\n\n"
            "Jogador 1 (Azul):\n  Mover: Setas do Teclado\n  Plantar Bomba: Barra de Espaco\n\n"
            "Jogador 2 (Vermelho):\n  Mover: W, A, S, D\n  Plantar Bomba: Tecla E\n\n"
            "Power-ups:\n  Fogo: Aumenta o alcance da explosao\n  Bomba: Aumenta o numero de bombas que voce pode plantar"
        )
        self.instructions_menu.add.label(text, wordwrap=True, font_size=16)
        self.instructions_menu.add.vertical_margin(30)
        self.instructions_menu.add.button('Voltar', pygame_menu.events.BACK)

    def _setup_name_input_menu(self):
        """Configura menu de insercao de nomes e selecao de icones"""
        # Campos de texto para nomes
        self.name_input_menu.add.text_input(
            'Jogador 1: ', default=self.player_names['player1'],
            onchange=lambda v: self.player_names.update({'player1': v}),
            maxchar=20
        )
        self.name_input_menu.add.text_input(
            'Jogador 2: ', default=self.player_names['player2'],
            onchange=lambda v: self.player_names.update({'player2': v}),
            maxchar=20
        )
        self.name_input_menu.add.vertical_margin(20)

        # Diretorio de icones
        icon_dir = os.path.join(os.path.dirname(__file__), '..', 'images', 'icons')
        try:
            files = [f for f in os.listdir(icon_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        except Exception:
            files = []
        items = [(os.path.splitext(f)[0], os.path.join(icon_dir, f)) for f in files]

        if items:
            # Dropdown para Jogador 1
            self.name_input_menu.add.label('Icone do Jogador 1:', font_size=16)
            self.name_input_menu.add.dropselect(
                title='',
                items=items,
                default=0,
                onchange=lambda label, value: self.player_icons.update({'player1': value})
            )
            self.name_input_menu.add.vertical_margin(10)
            # Dropdown para Jogador 2
            self.name_input_menu.add.label('Icone do Jogador 2:', font_size=16)
            self.name_input_menu.add.dropselect(
                title='',
                items=items,
                default=0,
                onchange=lambda label, value: self.player_icons.update({'player2': value})
            )
        else:
            self.name_input_menu.add.label('Nenhum icone encontrado em images/icons', font_size=16)

        self.name_input_menu.add.vertical_margin(20)
        self.name_input_menu.add.button('Iniciar Jogo', self._start_game)
        self.name_input_menu.add.button('Voltar', pygame_menu.events.BACK)

    def _setup_ranking_menu(self):
        """Configura o menu de ranking"""
        self.ranking_menu.clear()
        self.ranking_menu.add.label('Ranking de Vitorias', font_size=32)
        self.ranking_menu.add.vertical_margin(20)
        data = self.db_manager.load_ranking()
        if not data:
            self.ranking_menu.add.label('Nenhuma vitoria registrada.', font_size=20)
        else:
            for i, entry in enumerate(data, start=1):
                self.ranking_menu.add.label(
                    f"{i}. {entry['name']} — {entry['wins']} vitorias",
                    font_size=20
                )
        self.ranking_menu.add.vertical_margin(20)
        self.ranking_menu.add.button('Menu Principal', pygame_menu.events.BACK)

    def _start_game(self):
        """Inicia o jogo com nomes e icones selecionados"""
        pygame.event.clear()
        tile = self.screen_width // 13
        game = GameManager(
            self.screen,
            tile,
            self.player_names['player1'],
            self.player_names['player2'],
            icons=self.player_icons
        )
        game.run()
        return pygame_menu.events.BACK

    def run(self):
        """Executa o loop principal do menu"""
        self.main_menu.mainloop(self.screen)
        pygame.quit()
        sys.exit()
