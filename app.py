import copy


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
        self.black_castle = (True, True)  # (queen_side, king_side)
        self.white_castle = (True, True)

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
            "K": "\u2658",
        }
        for row in board:
            row_str = " ".join(
                [
                    ascii_figures[row[i]] if row[i] != "." else row[i]
                    for i in range(len(row))
                ]
            )
            print(row_str)

    def main(self):
        """Main logic"""

        while not self.close:
            self.print_board(self.board)
            possible = self.all_possible_moves()
            filtered_moves = self.filter_illegal_moves(possible)
            # move = self.get_move()
            # print(move)
            # update turn
            break

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
        moves = []
        direction = 1 if self.player == "w" and fig.isupper() else -1
        start_rank = 1 if self.player == "w" and fig.isupper() else 6
        promotion_rank = 7 if self.player == "w" and fig.isupper() else 0
        promotion_pieces = (
            ["Q", "R", "B", "K"] if fig.isupper() else ["q", "r", "b", "k"]
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
        filtered = []
        for move in moves:
            temp = copy.deepcopy(self.board)
            temp[move[2]][move[3]] = temp[move[0]][move[1]]
            temp[move[0]][move[1]] = "."
            self.print_board(temp)

    def is_king_attacked(self, board):
        # generate all capture virtual moves as king was a different piece, store move and piece type
        pass


if __name__ == "__main__":
    chess_obj = Chess()
    chess_obj.main()
