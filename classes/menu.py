# classes/menu.py

import pygame
import pygame_menu
from manager.game_manager import GameManager

class Menu:
    """
    Gerencia a exibição e a lógica do menu principal do jogo.
    """
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Tema customizado para o menu
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.widget_font = pygame_menu.font.FONT_HELVETICA
        theme.title_font = pygame_menu.font.FONT_HELVETICA
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        theme.background_color = (20, 80, 20) # Fundo verde escuro

        # Menu de Instruções
        self.instructions_menu = pygame_menu.Menu(
            title='Instrucoes',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.setup_instructions_menu()

        # Menu Principal
        self.main_menu = pygame_menu.Menu(
            title='Bomberman',
            width=self.screen_width,
            height=self.screen_height,
            theme=theme
        )
        self.setup_main_menu()

    def setup_main_menu(self):
        """ Configura os botões do menu principal. """
        self.main_menu.add.button('Jogar', self.start_game)
        self.main_menu.add.button('Instrucoes', self.instructions_menu)
        self.main_menu.add.button('Ranking', self.show_ranking) # Placeholder
        self.main_menu.add.button('Sair', pygame_menu.events.EXIT)

    def setup_instructions_menu(self):
        """ Configura o conteúdo do menu de instruções. """
        instructions = (
            "Use suas bombas para destruir caixas e derrotar seu oponente!\n\n"
            "Jogador 1 (Azul):\n"
            " - Mover: Setas do Teclado\n"
            " - Plantar Bomba: Barra de Espaco\n\n"
            "Jogador 2 (Vermelho):\n"
            " - Mover: Teclas W, A, S, D\n"
            " - Plantar Bomba: Tecla E\n\n"
            "Power-ups:\n"
            " - Fogo: Aumenta o alcance da explosao\n"
            " - Bomba: Aumenta o numero de bombas que voce pode plantar"
        )
        
        # CORREÇÃO: Trocado max_char=' ' por wordwrap=True
        self.instructions_menu.add.label(instructions, wordwrap=True, font_size=20)
        
        self.instructions_menu.add.vertical_margin(30)
        self.instructions_menu.add.button('Voltar', pygame_menu.events.BACK)

    def start_game(self):
        """ Inicia a partida do jogo. """
        # O tile_size é necessário para o GameManager, passamos ele aqui
        tile_size = self.screen_width // 13 
        game = GameManager(self.screen, tile_size)
        game.run()

        # Após o jogo terminar, desabilita o menu do jogo para voltar ao principal
        if self.main_menu.is_enabled():
            self.main_menu.disable()

    def show_ranking(self):
        """ Função placeholder para o ranking. """
        print("Funcionalidade de Ranking a ser implementada!")
        # Você pode fazer o menu piscar para indicar que o botão foi pressionado
        self.main_menu.get_current().get_selected_widget()._sound.play()


    def run(self):
        """ Inicia o loop do menu. """
        self.main_menu.mainloop(self.screen)