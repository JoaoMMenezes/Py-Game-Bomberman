import pygame
from manager.game_manager import GameManager

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
    pygame.display.set_caption("Bomberman - 2 Players")

    # Cria uma instância do gerenciador do jogo e inicia o loop principal
    game_manager = GameManager(screen, tile_size)
    game_manager.run()

    pygame.quit()

if __name__ == '__main__':
    main()