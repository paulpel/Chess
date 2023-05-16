import copy
import random


class Chess:
    def __init__(self, player="w") -> None:
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

        if player not in ["w", "b"]:
            raise ValueError("Invalid starting color")
        elif player == "w":
            self.board = self.board[::-1]

        self.player = player
        self.white_turn = True
        self.game_history = []
        self.last_move = None  # (from_x, from_y, to_x, to_y , figure)
        self.black_castle = [True, True]  # (queen_side, king_side)
        self.white_castle = [True, True]

        self.close = False

    def print_board(self, board):
        """Function to print current board state"""
        ascii_figures = {
            "p": "\u265F",  # white
            "r": "\u265C",
            "n": "\u265E",
            "b": "\u265D",
            "q": "\u265B",
            "k": "\u265A",
            "P": "\u2659",  # black
            "R": "\u2656",
            "N": "\u2658",
            "B": "\u2657",
            "Q": "\u2655",
            "K": "\u2654",
        }
        ids = ["X"] + [str(i) for i in range(8)]
        ids_row = " ".join(ids)
        print('\n', ids_row)
        count = 0
        for row in board:
            row_str = " ".join(
                [
                    ascii_figures[row[i]] if row[i] != "." else row[i]
                    for i in range(len(row))
                ]
            )
            print(str(count), row_str)
            count += 1
        print('\n')

    def main(self):
        """Main logic"""
        self.print_board(self.board)
        while not self.close:
            possible = self.all_possible_moves()
            filtered_moves = self.filter_illegal_moves(possible)
            filtered_moves.extend(self.generate_castle_moves())
            # append with castle moves if possible
            # move = self.get_move()
            # logic with player movement

            # random moves
            if len(filtered_moves) >= 1:
                random_move = random.choice(filtered_moves)
                if isinstance(random_move[0], tuple):
                    for move in random_move:
                        self.move(move)
                else:
                    if isinstance(random_move[-1], str):
                        self.move(random_move, random_move[-1])
                    else:
                        self.move(random_move)
                self.update_castle()
                input()
                print("Possible moves(from_row, from_col, to_row, to_col):")
                print('\n'.join([str(item) for item in filtered_moves]))
                print("Random move choosen:", random_move)
                print("\nWhite turn!" if self.white_turn else "\nBlack turn!")
                self.print_board(self.board)
            else:
                print("Game over")
                self.close = True

    def get_move(self):
        """Get move from user

        :return: (row_from, col_from, row_to, col_to, figure)
        :rtype: tuple
        """
        while True:
            start = [i for i in input("Choose starting row and col (XY): ")]
            if self.check_input(start):
                row_start, col_start = int(start[0]), int(start[1])
                break

        while True:
            end = [i for i in input("Choose destination row and col (XY): ")]
            if self.check_input(end, False):
                row_end, col_end = int(end[0]), int(end[1])
                break
        return (
            row_start,
            col_start,
            row_end,
            col_end,
            self.board[row_start][col_start],
        )

    def move(self, move, upgrade=False):
        from_row, to_row = move[0], move[2]
        from_col, to_col = move[1], move[3]
        fig = self.board[from_row][from_col]
        if upgrade:
            fig = upgrade
        self.board[to_row][to_col] = fig
        self.board[from_row][from_col] = "."
        self.white_turn = not self.white_turn  # update turn

    def check_input(self, inp, start=True):
        """Check if provided input is valid

        :param inp: input (row, col) cords
        :type inp: list
        :param start: starting or end position
        :type start: bool, optional
        :return: return if input is valid
        :rtype: bool
        """
        acceptable = [i for i in range(8)]
        if len(inp) != 2:
            print("Wrong input! Please provide two indexes in range 0-7. (ex. '73')")
            return False

        row, col = int(inp[0]), int(inp[1])

        if row not in acceptable or col not in acceptable:
            print("Wrong input! Indexes must be in range 0-7. (ex. '73')")
            return False

        if start:
            if self.board[row][col] == ".":
                print("Wrong input! There is no figure at that location!")
                return False

            if self.board[row][col].isupper() and self.player == "w":
                print("Wrong input! Please choose white figure!")
                return False
            elif self.board[row][col].islower() and self.player == "b":
                print("Wrong input! Please choose black figure!")
                return False
        else:
            if (
                self.board[row][col].isupper()
                and self.player == "b"
                or self.board[row][col].islower()
                and self.player == "w"
            ):
                print("Wrong input! Wrong move!")
                return False
        return True

    def all_possible_moves(self):
        """Generate all possible moves (no check condition! castles not included)

        :return: generated moves
        :rtype: list
        """
        all_moves = []

        starting_pieces = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] != ".":
                    if self.white_turn and self.board[row][col].islower():
                        starting_pieces.append((row, col, self.board[row][col]))
                    elif not self.white_turn and self.board[row][col].isupper():
                        starting_pieces.append((row, col, self.board[row][col]))

        for piece in starting_pieces:
            if piece[2].lower() == "p":
                all_moves.extend(self.generate_pawn_moves(piece[0], piece[1], piece[2]))
            if piece[2].lower() == "r":
                all_moves.extend(self.generate_rook_moves(piece[0], piece[1], piece[2]))
            if piece[2].lower() == "n":
                all_moves.extend(
                    self.generate_knight_moves(piece[0], piece[1], piece[2])
                )
            if piece[2].lower() == "b":
                all_moves.extend(
                    self.generate_bishop_moves(piece[0], piece[1], piece[2])
                )
            if piece[2].lower() == "q":
                all_moves.extend(
                    self.generate_queen_moves(piece[0], piece[1], piece[2])
                )
            if piece[2].lower() == "k":
                all_moves.extend(self.generate_king_moves(piece[0], piece[1], piece[2]))

        return all_moves

    def generate_pawn_moves(self, row, col, fig):
        """Generate pawn moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved ('p' or 'P')
        :type fig: string
        :return: all possible pawn moves
        :rtype: list
        """
        moves = []
        direction = 1 if self.player == "w" and fig.isupper() else -1
        start_rank = 1 if self.player == "w" and fig.isupper() else 6
        promotion_rank = 7 if self.player == "w" and fig.isupper() else 0
        promotion_pieces = (
            ["Q", "R", "B", "N"] if fig.isupper() else ["q", "r", "b", "n"]
        )

        # Move forward
        if 0 <= row + direction < 8 and self.board[row + direction][col] == ".":
            # Check for promotion
            if row + direction == promotion_rank:
                moves.extend(
                    [
                        (row, col, row + direction, col, promotion_piece)
                        for promotion_piece in promotion_pieces
                    ]
                )
            else:
                moves.append((row, col, row + direction, col))

        # Double move from the starting rank
        if (
            row == start_rank
            and self.board[row + direction][col] == "."
            and self.board[row + 2 * direction][col] == "."
        ):
            moves.append((row, col, row + 2 * direction, col))

        # Captures
        for dy in (-1, 1):
            if 0 <= col + dy < 8 and 0 <= row + direction < 8:
                target_piece = self.board[row + direction][col + dy]
                if target_piece != "." and (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    # Check for promotion
                    if row + direction == promotion_rank:
                        moves.extend(
                            [
                                (row, col, row + direction, col + dy, promotion_piece)
                                for promotion_piece in promotion_pieces
                            ]
                        )
                    else:
                        moves.append((row, col, row + direction, col + dy))

        # En passant (assuming the last move is stored as a tuple (from_x, from_y, to_x, to_y))
        last_move = self.last_move
        if last_move:
            from_row, from_col, to_row, to_col, fig_last = last_move
            if (
                fig_last.lower() == "p"
                and abs(from_row - to_row) == 2
                and row == to_row
            ):
                if col + 1 == to_col:
                    moves.append((row, col, row + direction, col + 1))
                elif col - 1 == to_col:
                    moves.append((row, col, row + direction, col - 1))
        return moves

    def generate_rook_moves(self, row, col, fig):
        """Generate rook moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved (ex. 'r' or 'R')
        :type fig: string
        :return: all possible rook moves (castles not included)
        :rtype: list
        """
        moves = []

        # Define directions for the rook moves: up, down, left, and right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Continue moving in the same direction until an obstacle is encountered or the board edge is reached
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]

                # If the square is empty, add the move and continue to the next square in the direction
                if target_piece == ".":
                    moves.append((row, col, new_row, new_col))

                # If there's an enemy piece, capture it and break the loop for this direction
                elif (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    moves.append((row, col, new_row, new_col))
                    break

                # If there's a friendly piece, break the loop for this direction
                else:
                    break

                new_row += dr
                new_col += dc

        return moves

    def generate_knight_moves(self, row, col, fig):
        """Generate knight moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved (ex. 'n' or 'N')
        :type fig: string
        :return: all possible knight moves
        :rtype: list
        """
        moves = []

        # Define possible knight moves: combinations of two squares in one direction and one square in the other direction
        knight_moves = [
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1),
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc

            # Check if the new position is inside the board
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]

                # If the square is empty or contains an enemy piece, the move is valid
                if target_piece == "." or (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    moves.append((row, col, new_row, new_col))

        return moves

    def generate_bishop_moves(self, row, col, fig):
        """Generate bishop moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved (ex. 'b' or 'B')
        :type fig: string
        :return: all possible bishop moves
        :rtype: list
        """
        moves = []

        # Define directions for the bishop moves: diagonally up-left, up-right, down-left, and down-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Continue moving in the same direction until an obstacle is encountered or the board edge is reached
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]

                # If the square is empty, add the move and continue to the next square in the direction
                if target_piece == ".":
                    moves.append((row, col, new_row, new_col))

                # If there's an enemy piece, capture it and break the loop for this direction
                elif (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    moves.append((row, col, new_row, new_col))
                    break

                # If there's a friendly piece, break the loop for this direction
                else:
                    break

                new_row += dr
                new_col += dc

        return moves

    def generate_queen_moves(self, row, col, fig):
        """Generate queen moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved (ex. 'q' or 'Q')
        :type fig: string
        :return: all possible queen moves
        :rtype: list
        """
        moves = []

        # Define directions for the queen moves: horizontally, vertically, and diagonally
        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Continue moving in the same direction until an obstacle is encountered or the board edge is reached
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]

                # If the square is empty, add the move and continue to the next square in the direction
                if target_piece == ".":
                    moves.append((row, col, new_row, new_col))

                # If there's an enemy piece, capture it and break the loop for this direction
                elif (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    moves.append((row, col, new_row, new_col))
                    break

                # If there's a friendly piece, break the loop for this direction
                else:
                    break

                new_row += dr
                new_col += dc

        return moves

    def generate_king_moves(self, row, col, fig):
        """Generate king moves

        :param row: row of figure to generate moves for
        :type row: int
        :param col: column of figure to generate moves for
        :type col: int
        :param fig: figure to be moved (ex. 'k' or 'K')
        :type fig: string
        :return: all possible king moves
        :rtype: list
        """
        moves = []

        # Define possible king moves: horizontally, vertically, and diagonally (one square)
        king_moves = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc

            # Check if the new position is inside the board
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target_piece = self.board[new_row][new_col]

                # If the square is empty or contains an enemy piece, the move is valid
                if target_piece == "." or (
                    target_piece.islower() if fig.isupper() else target_piece.isupper()
                ):
                    moves.append((row, col, new_row, new_col))

        return moves

    def filter_illegal_moves(self, moves):
        """Filter moves to exlude illegal ones

        :param moves: list of moves (list of tuples)
        :type moves: moves
        """
        filtered = []
        for move in moves:
            temp = copy.deepcopy(self.board)
            fig = temp[move[0]][move[1]]
            temp[move[2]][move[3]] = temp[move[0]][move[1]]
            temp[move[0]][move[1]] = "."
            if not self.is_king_attacked(temp, fig):
                filtered.append(move)
        return filtered

    def is_king_attacked(self, board, fig):
        """Check if king is being attacked

        :param board: potential board state
        :type board: list
        :param fig: figure which was moved
        :type fig: string
        :return: if the king is being attacked
        :rtype: bool
        """
        remaining_enemy_type = set()
        for row in range(len(board)):
            for col in range(len(board[row])):
                if fig.islower() != board[row][col].islower() and board[row][col] != ".":
                    remaining_enemy_type.add(board[row][col].lower())
                if board[row][col].lower() == 'k' and board[row][col].islower() == fig.islower():
                    row_king, col_king = row, col

        remaining_enemy_type = list(remaining_enemy_type)
        if 'p' in remaining_enemy_type:
            direction = 1 if self.player == "w" and fig.isupper() else -1
            for dy in (-1, 1):
                if 0 <= col_king + dy < 8 and 0 <= row_king + direction < 8:
                    if board[row_king + direction][col_king + dy].lower() == 'p' and board[row_king + direction][col_king + dy].islower() != fig.islower():
                        return True
        if 'r' in remaining_enemy_type:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                new_row, new_col = row_king + dr, col_king + dc
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece != '.':
                        if target_piece.lower() == 'r' and target_piece.islower() != fig.islower():
                            return True
                        else:
                            break
                    new_row += dr
                    new_col += dc
        if 'n' in remaining_enemy_type:
            knight_moves = [
                (2, 1),
                (1, 2),
                (-1, 2),
                (-2, 1),
                (-2, -1),
                (-1, -2),
                (1, -2),
                (2, -1),
            ]
            for dr, dc in knight_moves:
                new_row, new_col = row_king + dr, col_king + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece.lower() == 'n' and target_piece.islower() != fig.islower():
                        return True
        if 'b' in remaining_enemy_type:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                new_row, new_col = row_king + dr, col_king + dc
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece != '.':
                        if target_piece.lower() == 'b' and target_piece.islower() != fig.islower():
                            return True
                        else:
                            break
                    new_row += dr
                    new_col += dc
        if 'q' in remaining_enemy_type:
            directions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]
            for dr, dc in directions:
                new_row, new_col = row_king + dr, col_king + dc
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece != '.':
                        if target_piece.lower() == 'q' and target_piece.islower() != fig.islower():
                            return True
                        else :
                            break
                    new_row += dr
                    new_col += dc
        if 'k' in remaining_enemy_type:
            king_moves = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]
            for dr, dc in king_moves:
                new_row, new_col = row_king + dr, col_king + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board[new_row][new_col]
                    if target_piece.islower() != fig.islower() and target_piece.lower() == 'k':
                        return True

        return False

    def generate_castle_moves(self):
        moves = []
        if (self.player == "w" and self.white_turn) or (self.player == 'b' and not self.white_turn):

            fig = self.board[7][4]
            if fig.lower() != 'k':
                return moves

            valid_bot_left = self.check_castle([(7, 2), (7, 3)],  [(7, 2), (7, 3), (7, 4)], fig)
            valid_bot_right = self.check_castle([(7, 5), (7, 6)],  [(7, 4), (7, 5), (7, 6)], fig)

            if self.player == "w" and self.white_castle[0] and valid_bot_left and self.white_turn:
                moves.append(((7, 4, 7, 2), (7, 0, 7, 3)))
            if self.player == "w" and self.white_castle[1] and valid_bot_right and self.white_turn:
                moves.append(((7, 4, 7, 6), (7, 7, 7, 5)))
            if self.player == "b" and self.black_castle[0] and valid_bot_left and not self.white_turn:
                moves.append(((7, 4, 7, 2), (7, 0, 7, 3)))
            if self.player == "b" and self.black_castle[1] and valid_bot_right and not self.white_turn:
                moves.append(((7, 4, 7, 6), (7, 7, 7, 5)))

        else:
            fig = self.board[0][4]
            if fig.lower() != 'k':
                return moves

            valid_up_left = self.check_castle([(0, 2), (0, 3)],  [(0, 2), (0, 3), (0, 4)], fig)
            valid_up_right = self.check_castle([(0, 5), (0, 6)],  [(0, 4), (0, 5), (0, 6)], fig)

            if self.player == "w" and self.white_castle[0] and valid_up_left and not self.white_turn:
                moves.append(((0, 4, 0, 2), (0, 0, 0, 3)))
            if self.player == "w" and self.white_castle[1] and valid_up_right and not self.white_turn:
                moves.append(((0, 4, 0, 6), (0, 7, 0, 5)))
            if self.player == "b" and self.black_castle[0] and valid_up_left and self.white_turn:
                moves.append(((0, 4, 0, 2), (0, 0, 0, 3)))
            if self.player == "b" and self.black_castle[1] and valid_up_right and self.white_turn:
                moves.append(((0, 4, 0, 6), (0, 7, 0, 5)))

        return moves

    def check_castle(self, tiles_b, tiles_to_check, fig):
        is_valid = True
        tiles_between = [self.board[i][j] for i, j in tiles_b]
        if len(set(tiles_between)) == 1 and tiles_between[0] == '.':
            for row, col in tiles_to_check:
                temp_b = copy.deepcopy(self.board)
                temp_b[7][4] = '.'
                temp_b[row][col] = fig
                if self.is_king_attacked(temp_b, fig):
                    is_valid = False
        else:
            is_valid = False

        return is_valid

    def update_castle(self):
        king_bot = self.board[7][4] 
        bot_left = self.board[7][0]
        bot_right = self.board[7][7]

        king_top = self.board[0][4]
        up_left = self.board[0][0]
        up_right = self.board[0][7]


        if king_bot != 'k':
            if self.player == "w":
                self.white_castle = [False, False]
            else:
                self.black_castle = [False, False]
        else:
            if bot_left != 'r':
                if self.player == "w":
                    self.white_castle[0] = False
                else:
                    self.black_castle[0] = False
            if bot_right != 'r':
                if self.player == "w":
                    self.white_castle[1] = False
                else:
                    self.black_castle[1] = False
        
        if king_top != 'k':
            if self.player != "w":
                self.white_castle = [False, False]
            else:
                self.black_castle = [False, False]
        else:
            if up_left != 'r':
                if self.player != "w":
                    self.white_castle[0] = False
                else:
                    self.black_castle[0] = False
            if up_right != 'r':
                if self.player != "w":
                    self.white_castle[1] = False
                else:
                    self.black_castle[1] = False


if __name__ == "__main__":
    chess_obj = Chess()
    chess_obj.main()
