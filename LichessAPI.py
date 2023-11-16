import lichess.api
import lichess.pgn
import chess.pgn
import random
import io
import numpy as np

class ChessPositionRepresentation:
    def __init__(self, fen):
        # Initialize boards for each piece type
        self.white_pawns = np.zeros((8, 8), dtype=int)
        self.white_rooks = np.zeros((8, 8), dtype=int)
        self.white_knights = np.zeros((8, 8), dtype=int)
        self.white_bishops = np.zeros((8, 8), dtype=int)
        self.white_queens = np.zeros((8, 8), dtype=int)
        self.white_king = np.zeros((8, 8), dtype=int)

        self.black_pawns = np.zeros((8, 8), dtype=int)
        self.black_rooks = np.zeros((8, 8), dtype=int)
        self.black_knights = np.zeros((8, 8), dtype=int)
        self.black_bishops = np.zeros((8, 8), dtype=int)
        self.black_queens = np.zeros((8, 8), dtype=int)
        self.black_king = np.zeros((8, 8), dtype=int)

        self.set_positions(fen)

    def set_positions(self, fen):
        # Parse the FEN string and update the boards
        board = chess.Board(fen)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Convert chess square index to 2D array indices
                row, col = divmod(square, 8)
                # Set 1 in the corresponding board based on piece type and color
                if piece.color == chess.WHITE:
                    if piece.piece_type == chess.PAWN:
                        self.white_pawns[row, col] = 1
                    elif piece.piece_type == chess.ROOK:
                        self.white_rooks[row, col] = 1
                    elif piece.piece_type == chess.KNIGHT:
                        self.white_knights[row, col] = 1
                    elif piece.piece_type == chess.BISHOP:
                        self.white_bishops[row, col] = 1
                    elif piece.piece_type == chess.QUEEN:
                        self.white_queens[row, col] = 1
                    elif piece.piece_type == chess.KING:
                        self.white_king[row, col] = 1
                else:
                    if piece.piece_type == chess.PAWN:
                        self.black_pawns[row, col] = 1
                    elif piece.piece_type == chess.ROOK:
                        self.black_rooks[row, col] = 1
                    elif piece.piece_type == chess.KNIGHT:
                        self.black_knights[row, col] = 1
                    elif piece.piece_type == chess.BISHOP:
                        self.black_bishops[row, col] = 1
                    elif piece.piece_type == chess.QUEEN:
                        self.black_queens[row, col] = 1
                    elif piece.piece_type == chess.KING:
                        self.black_king[row, col] = 1

# class NNChessGameStateRepresentation:
    

def get_random_games_from_player(username, num_games=100):
    """Fetch random games of a player from Lichess"""
    games = list(lichess.api.user_games(username, max=num_games))
    return random.sample(games, min(num_games, len(games)))


def extract_all_fens_from_pgn(pgn_text, player_color):
    """Extract random FEN positions from a game's PGN where the specified player is on the move"""
    pgn = chess.pgn.read_game(io.StringIO(pgn_text))
    game_positions = []
    board = pgn.board()
    for move in pgn.mainline_moves():
        if (player_color == 'white' and board.turn) or (player_color == 'black' and not board.turn):
            game_positions.append(board.fen())
        board.push(move)
    return game_positions


def get_all_positions(username, player_color, num_games=100):
    """Get random positions from a user's games"""
    games = get_random_games_from_player(username, num_games)
    all_games = []
    for game in games:
        pgn_text = lichess.pgn.from_game(game)
        positions = extract_all_fens_from_pgn(pgn_text, player_color)
        all_games.append(positions)
    return all_games


# Sample usage
positions = get_all_positions('chesstacion', 'white', 20)
for idx, position in enumerate(positions):
    print(idx, position)

# # Example usage
# fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
# chess_position = ChessPositionRepresentation(fen)
# print("White Pawns:\n", chess_position.white_pawns)