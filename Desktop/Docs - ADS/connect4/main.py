import pygame
import sys
import time  # Para adicionar o atraso
from board import Board
from ai import MinimaxAI, AlphaBetaAI
from settings import TILE_SIZE, ROWS, COLUMNS, COLORS

def show_menu(screen):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    options = ["Minimax", "Alpha-Beta"]
    ply_levels = [1, 2, 3, 4]
    selected_algorithm = None
    selected_ply = None

    while True:
        screen.fill((0, 0, 0))

        title_text = font.render("Escolha o algoritmo", True, (255, 255, 255))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        algo_buttons = []
        for i, option in enumerate(options):
            x, y = screen.get_width() // 2 - 100, 150 + i * 80
            width, height = 200, 50
            color = (0, 128, 255) if selected_algorithm != i else (0, 200, 100)
            pygame.draw.rect(screen, color, (x, y, width, height))
            text = font.render(option, True, (255, 255, 255))
            screen.blit(text, (x + width // 2 - text.get_width() // 2, y + height // 2 - text.get_height() // 2))
            algo_buttons.append((x, y, width, height, i))

        ply_buttons = []
        if selected_algorithm is not None:
            ply_text = font.render("Escolha o nível do Ply", True, (255, 255, 255))
            screen.blit(ply_text, (screen.get_width() // 2 - ply_text.get_width() // 2, 350))
            for i, level in enumerate(ply_levels):
                x, y = screen.get_width() // 2 - 100, 400 + i * 60
                width, height = 200, 50
                color = (0, 128, 255) if selected_ply != level else (0, 200, 100)
                pygame.draw.rect(screen, color, (x, y, width, height))
                text = font.render(f"Ply {level}", True, (255, 255, 255))
                screen.blit(text, (x + width // 2 - text.get_width() // 2, y + height // 2 - text.get_height() // 2))
                ply_buttons.append((x, y, width, height, level))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for x, y, w, h, index in algo_buttons:
                    if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                        selected_algorithm = index
                for x, y, w, h, level in ply_buttons:
                    if x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h:
                        selected_ply = level

        if selected_algorithm is not None and selected_ply is not None:
            return options[selected_algorithm], selected_ply

        clock.tick(30)


def main():
    pygame.init()
    width = COLUMNS * TILE_SIZE
    height = (ROWS + 1) * TILE_SIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect4 com IA")

    algorithm, ply = show_menu(screen)

    if algorithm == "Minimax":
        ai = MinimaxAI(ply)
    elif algorithm == "Alpha-Beta":
        ai = AlphaBetaAI(ply)

    board = Board(ROWS, COLUMNS)
    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, COLORS["BLACK"], (0, 0, width, TILE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, COLORS["RED"], (posx, TILE_SIZE // 2), TILE_SIZE // 2 - 5)

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                pygame.draw.rect(screen, COLORS["BLACK"], (0, 0, width, TILE_SIZE))
                posx = event.pos[0]
                col = posx // TILE_SIZE

                if board.is_valid_location(col):
                    row = board.get_next_open_row(col)
                    board.drop_piece(row, col, 1)

                    if board.check_victory(1):
                        print("Jogador 1 venceu!")
                        game_over = True

                    turn = 1
                    # Exibe a bola do jogador humano (vermelha) na tela
                    board.draw(screen)
                    pygame.display.update()

                    # Atraso após a jogada do humano
                    pygame.time.wait(500)  # Aguarda 500 milissegundos (meio segundo)

                else:
                    print(f"Jogada inválida na coluna {col}")

        # Agora a IA faz a jogada
        if turn == 1 and not game_over:
            print("Turno da IA...")
            col = ai.get_best_move(board, 2)
            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, 2)

                if board.check_victory(2):
                    print("Jogador 2 (IA) venceu!")
                    game_over = True

                turn = 0
                # Exibe a bola da IA (amarela) na tela
                board.draw(screen)
                pygame.display.update()

        board.draw(screen)
        pygame.display.update()

    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
