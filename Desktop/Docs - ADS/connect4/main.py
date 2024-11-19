import pygame
import sys
import time  # Para calcular tempos
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

        title_text = font.render("Escolha o algoritmo que deseja desafiar", True, (255, 255, 255))
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
            ply_text = font.render("Escolha o nível de dificuldade (Ply)", True, (255, 255, 255))
            screen.blit(ply_text, (screen.get_width() // 2 - ply_text.get_width() // 2, 350))
            for i, level in enumerate(ply_levels):
                x, y = screen.get_width() // 2 - 100, 400 + i * 60
                width, height = 200, 50
                color = (0, 128, 255) if selected_ply != level else (0, 200, 100)
                pygame.draw.rect(screen, color, (x, y, width, height))
                text = font.render(f"Nivel {level}", True, (255, 255, 255))
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

def display_message(screen, message):
    font = pygame.font.SysFont("Arial", 36)
    pygame.draw.rect(screen, COLORS["BLACK"], (0, 0, screen.get_width(), TILE_SIZE))
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (10, 10))
    pygame.display.update()

def show_game_over_menu(screen, winner, elapsed_time):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 36)
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))

        winner_text = font.render(f"{winner} venceu!", True, (255, 255, 255))
        time_text = font.render(f"Duração: {elapsed_time:.2f} segundos", True, (255, 255, 255))

        screen.blit(winner_text, (screen.get_width() // 2 - winner_text.get_width() // 2, 100))
        screen.blit(time_text, (screen.get_width() // 2 - time_text.get_width() // 2, 160))

        menu_text = font.render("Voltar ao menu inicial", True, (255, 255, 255))
        quit_text = font.render("Sair", True, (255, 255, 255))

        menu_button = pygame.Rect(screen.get_width() // 2 - 150, 250, 300, 50)
        quit_button = pygame.Rect(screen.get_width() // 2 - 150, 350, 300, 50)

        pygame.draw.rect(screen, (0, 128, 255), menu_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)

        screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, menu_button.centery - menu_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_button.collidepoint(mouse_pos):
                    return "menu"
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

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
    font = pygame.font.SysFont("Arial", 36)

    start_time = time.time()  # Início do cronômetro

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
                        display_message(screen, "Você venceu!")
                        game_over = True
                        winner = "Você"

                    turn = 1
                    board.draw(screen)
                    pygame.display.update()
                    pygame.time.wait(500)

        if turn == 1 and not game_over:
            display_message(screen, "Vez da IA...")
            
            # Calcula o tempo para o movimento da IA
            start_move_time = time.time()
            col = ai.get_best_move(board, 2)
            end_move_time = time.time()
            move_duration = end_move_time - start_move_time
            print(f"Tempo de execução da IA: {move_duration:.4f} segundos")

            if board.is_valid_location(col):
                row = board.get_next_open_row(col)
                board.drop_piece(row, col, 2)

                if board.check_victory(2):
                    display_message(screen, "IA venceu!")
                    game_over = True
                    winner = "IA"

                turn = 0
                board.draw(screen)
                pygame.display.update()

        board.draw(screen)
        pygame.display.update()

    if game_over:
        elapsed_time = time.time() - start_time  # Calcula o tempo total
        pygame.time.wait(3000)
        next_action = show_game_over_menu(screen, winner, elapsed_time)
        if next_action == "menu":
            main()

if __name__ == "__main__":
    main()
