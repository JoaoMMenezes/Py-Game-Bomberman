# classes/menu.py

import pygame
import pygame_menu
from manager.db_manager import DBManager
from manager.game_manager import GameManager

class Menu:
    """
    Gerencia a exibição e a lógica do menu principal do jogo.
    """
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.player_names = {'player1': 'Jogador 1', 'player2': 'Jogador 2'}
        self.db_manager = DBManager()

        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font = pygame_menu.font.FONT_HELVETICA
        theme.title_font = pygame_menu.font.FONT_HELVETICA
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        theme.background_color = (20, 80, 20)

        # Inicializa os menus
        self.main_menu = pygame_menu.Menu(
            title='Bomberman',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.instructions_menu = pygame_menu.Menu(
            title='Instrucoes',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.name_input_menu = pygame_menu.Menu(
            title='Insira os Nomes',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.ranking_menu = pygame_menu.Menu(
            title='Ranking de Vitorias',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )

        # Popula os menus com seus widgets
        self.setup_instructions_menu()
        self.setup_name_input_menu()
        self.setup_ranking_menu() # Configura uma vez para o primeiro acesso
        self.setup_main_menu()

    def setup_main_menu(self):
        """ Configura os botões do menu principal. """
        self.main_menu.add.button('Jogar', self.name_input_menu)
        self.main_menu.add.button('Instrucoes', self.instructions_menu)
        self.main_menu.add.button('Ranking', self.ranking_menu)
        self.main_menu.add.button('Sair', pygame_menu.events.EXIT)

    def setup_name_input_menu(self):
        """ Configura os campos de texto para os nomes dos jogadores. """
        self.name_input_menu.add.text_input('Jogador 1: ', default=self.player_names['player1'], onchange=lambda value: self.player_names.update({'player1': value}))
        self.name_input_menu.add.text_input('Jogador 2: ', default=self.player_names['player2'], onchange=lambda value: self.player_names.update({'player2': value}))
        self.name_input_menu.add.vertical_margin(30)
        self.name_input_menu.add.button('Iniciar Jogo', self.start_game)
        self.name_input_menu.add.button('Voltar', pygame_menu.events.BACK)

    def setup_ranking_menu(self):
        """ Popula a tela de ranking com os dados do arquivo JSON. """
        self.ranking_menu.clear()
        self.ranking_menu.add.label('Top 5 Jogadores', font_size=35)
        self.ranking_menu.add.vertical_margin(25)
        ranking_data = self.db_manager.load_ranking()
        if not ranking_data:
            self.ranking_menu.add.label('Nenhuma vitoria registrada.', font_size=24)
        else:
            for i, entry in enumerate(ranking_data):
                text = f'{i+1}. {entry["name"]} - {entry["wins"]} Vitorias'
                self.ranking_menu.add.label(text, font_size=24, margin=(0, 5))
        self.ranking_menu.add.vertical_margin(40)
        self.ranking_menu.add.button('Voltar', self.ranking_menu.disable)

    def setup_instructions_menu(self):
        """ Configura o conteúdo do menu de instruções. """
        instructions = ("Use suas bombas para destruir caixas e derrotar seu oponente!\n\n"
                        "Jogador 1 (Azul):\n - Mover: Setas do Teclado\n - Plantar Bomba: Barra de Espaco\n\n"
                        "Jogador 2 (Vermelho):\n - Mover: Teclas W, A, S, D\n - Plantar Bomba: Tecla E\n\n"
                        "Power-ups:\n - Fogo: Aumenta o alcance da explosao\n - Bomba: Aumenta o numero de bombas que voce pode plantar")
        self.instructions_menu.add.label(instructions, wordwrap=True, font_size=20)
        self.instructions_menu.add.vertical_margin(30)
        self.instructions_menu.add.button('Voltar', pygame_menu.events.BACK)

    def start_game(self):
        """ Inicia a partida e, ao final, desabilita os menus para passar o controle. """
        tile_size = self.screen_width // 13
        game = GameManager(self.screen, tile_size, self.player_names['player1'], self.player_names['player2'])
        game.run()
        # ATUALIZADO: Desabilita os menus para quebrar seus loops e o controle voltar para o método 'run'
        self.name_input_menu.disable()
        self.main_menu.disable()

    def run(self):
        """
        CORRIGIDO: Controla a exibição sequencial dos menus, gerenciando o fluxo.
        """
        while True:
            # Garante que os menus estejam reativados a cada volta no loop
            self.main_menu.enable()
            self.name_input_menu.enable()

            # 1. Exibe o menu principal. O loop aqui é quebrado pela ação do método 'start_game'.
            self.main_menu.mainloop(self.screen)

            # Se o usuário clicou no botão 'Sair', a flag _exit será verdadeira.
            if self.main_menu.get_current()._exit:
                break # Encerra o loop 'while True' e o programa.

            # 2. Após o jogo, o loop do main_menu foi quebrado. Agora, atualizamos e mostramos o ranking.
            self.setup_ranking_menu() # Recarrega os dados do ranking
            self.ranking_menu.enable()
            self.ranking_menu.mainloop(self.screen) # Este loop é quebrado pelo botão 'Voltar'.

            # 3. Após sair do ranking, o loop 'while True' recomeça, exibindo o menu principal novamente.