import numpy as np
import pygame
from settings import TILE_SIZE, COLORS

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns))
        self.winning_positions = []  # Lista para armazenar as posições das bolinhas vencedoras

    def is_valid_location(self, col):
        return self.board[self.rows - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def check_victory(self, piece):
        # Limpa as posições vencedoras anteriores
        self.winning_positions = []

        # Horizontal
        for r in range(self.rows):
            for c in range(self.columns - 3):
                if all(self.board[r, c + i] == piece for i in range(4)):
                    self.winning_positions = [(r, c + i) for i in range(4)]  # Armazena as posições
                    return True

        # Vertical
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if all(self.board[r + i, c] == piece for i in range(4)):
                    self.winning_positions = [(r + i, c) for i in range(4)]  # Armazena as posições
                    return True

        # Positive Diagonal
        for r in range(self.rows - 3):
            for c in range(self.columns - 3):
                if all(self.board[r + i, c + i] == piece for i in range(4)):
                    self.winning_positions = [(r + i, c + i) for i in range(4)]  # Armazena as posições
                    return True

        # Negative Diagonal
        for r in range(3, self.rows):
            for c in range(self.columns - 3):
                if all(self.board[r - i, c + i] == piece for i in range(4)):
                    self.winning_positions = [(r - i, c + i) for i in range(4)]  # Armazena as posições
                    return True
        
        return False

    def draw(self, screen):
        for c in range(self.columns):
            for r in range(self.rows):
                # Desenha o fundo do tabuleiro
                pygame.draw.rect(screen, COLORS["BLUE"], 
                                (c * TILE_SIZE, r * TILE_SIZE + TILE_SIZE, TILE_SIZE, TILE_SIZE))
                # Desenha os círculos vazios
                pygame.draw.circle(screen, COLORS["BLACK"], 
                                (c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + TILE_SIZE + TILE_SIZE // 2), 
                                TILE_SIZE // 2 - 5)

        # Desenha as peças no tabuleiro
        for c in range(self.columns):
            for r in range(self.rows):
                # Verifica se a posição faz parte da vitória
                if (r, c) in self.winning_positions:
                    # Se a posição for parte da vitória, desenha em verde
                    color = COLORS["GREEN"]
                elif self.board[r][c] == 1:
                    color = COLORS["RED"]
                elif self.board[r][c] == 2:
                    color = COLORS["YELLOW"]
                else:
                    continue

                # Desenha a peça com a cor determinada
                pygame.draw.circle(screen, color, 
                                   (c * TILE_SIZE + TILE_SIZE // 2, 
                                    screen.get_height() - (r * TILE_SIZE + TILE_SIZE // 2)), 
                                   TILE_SIZE // 2 - 5)

        pygame.display.update()
