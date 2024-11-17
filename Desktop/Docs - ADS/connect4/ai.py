import numpy as np
import math
from board import Board  # Certifique-se de que o arquivo board.py está correto e importado

class BaseAI:
    def __init__(self, ply):
        self.ply = ply

    def evaluate_board(self, board, piece):
        """
        Avaliação do estado do tabuleiro baseada em padrões estratégicos:
        - Alinhamentos de 2, 3 ou 4 peças.
        - Bloqueios ao adversário.
        """
        score = 0
        opponent_piece = 3 - piece

        # Padrões estratégicos: Avaliar alinhamentos
        for row in range(board.rows):
            for col in range(board.columns):
                # Verificar alinhamentos horizontais, verticais e diagonais
                if col + 3 < board.columns:  # Horizontal
                    window = board.board[row, col:col + 4]
                    score += self.score_window(window, piece, opponent_piece)
                if row + 3 < board.rows:  # Vertical
                    window = board.board[row:row + 4, col]
                    score += self.score_window(window, piece, opponent_piece)
                if col + 3 < board.columns and row + 3 < board.rows:  # Diagonal (↘)
                    window = [board.board[row + i, col + i] for i in range(4)]
                    score += self.score_window(window, piece, opponent_piece)
                if col - 3 >= 0 and row + 3 < board.rows:  # Diagonal (↙)
                    window = [board.board[row + i, col - i] for i in range(4)]
                    score += self.score_window(window, piece, opponent_piece)

        return score

    def score_window(self, window, piece, opponent_piece):
        """
        Avalia uma janela específica (4 posições consecutivas) no tabuleiro.
        """
        score = 0
        piece_count = np.count_nonzero(window == piece)  # Conta as peças do jogador
        opponent_count = np.count_nonzero(window == opponent_piece)  # Conta as peças do oponente
        empty_count = np.count_nonzero(window == 0)  # Conta os espaços vazios

        if piece_count == 4:
            score += 100  # Vitória garantida
        elif piece_count == 3 and empty_count == 1:
            score += 10  # Boa oportunidade de vitória
        elif piece_count == 2 and empty_count == 2:
            score += 5  # Potencial estratégico

        if opponent_count == 3 and empty_count == 1:
            score -= 80  # Bloquear o oponente é prioritário

        return score

class MinimaxAI(BaseAI):
    def minimax(self, board, depth, maximizing_player, piece):
        valid_locations = [c for c in range(board.columns) if board.is_valid_location(c)]
        is_terminal = board.check_victory(1) or board.check_victory(2) or len(valid_locations) == 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_victory(piece):
                    return (None, 1000000)
                elif board.check_victory(3 - piece):
                    return (None, -1000000)
                else:
                    return (None, 0)
            else:
                return (None, self.evaluate_board(board, piece))

        if maximizing_player:
            value = -math.inf
            best_column = None
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = Board(board.rows, board.columns)
                temp_board.board = board.board.copy()
                temp_board.drop_piece(row, col, piece)

                new_score = self.minimax(temp_board, depth - 1, False, piece)[1]
                if new_score > value:
                    value = new_score
                    best_column = col
            return best_column, value
        else:
            value = math.inf
            best_column = None
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = Board(board.rows, board.columns)
                temp_board.board = board.board.copy()
                temp_board.drop_piece(row, col, 3 - piece)

                new_score = self.minimax(temp_board, depth - 1, True, piece)[1]
                if new_score < value:
                    value = new_score
                    best_column = col
            return best_column, value

    def get_best_move(self, board, piece):
        return self.minimax(board, self.ply, True, piece)[0]


class AlphaBetaAI(BaseAI):
    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, piece):
        valid_locations = [c for c in range(board.columns) if board.is_valid_location(c)]
        is_terminal = board.check_victory(1) or board.check_victory(2) or len(valid_locations) == 0

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_victory(piece):
                    return (None, 1000000)
                elif board.check_victory(3 - piece):
                    return (None, -1000000)
                else:
                    return (None, 0)
            else:
                return (None, self.evaluate_board(board, piece))

        if maximizing_player:
            value = -math.inf
            best_column = None
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = Board(board.rows, board.columns)
                temp_board.board = board.board.copy()
                temp_board.drop_piece(row, col, piece)

                new_score = self.alpha_beta(temp_board, depth - 1, alpha, beta, False, piece)[1]
                if new_score > value:
                    value = new_score
                    best_column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_column, value
        else:
            value = math.inf
            best_column = None
            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = Board(board.rows, board.columns)
                temp_board.board = board.board.copy()
                temp_board.drop_piece(row, col, 3 - piece)

                new_score = self.alpha_beta(temp_board, depth - 1, alpha, beta, True, piece)[1]
                if new_score < value:
                    value = new_score
                    best_column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_column, value

    def get_best_move(self, board, piece):
        return self.alpha_beta(board, self.ply, -math.inf, math.inf, True, piece)[0]
