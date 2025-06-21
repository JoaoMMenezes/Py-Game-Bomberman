# main.py

import pygame
from classes.menu import Menu # Alterado de GameManager para Menu

def main():
    """
    Função principal que inicializa e executa o jogo.
    """
    pygame.init()

    # Define o tamanho da tela e o título da janela
    tile_size = 48
    grid_width = 13
    grid_height = 13
    screen_size = (grid_width * tile_size, grid_height * tile_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Bomberman - Menu")

    # Cria uma instância do Menu e inicia seu loop principal
    menu = Menu(screen)
    menu.run()

    pygame.quit()

if __name__ == '__main__':
    main()