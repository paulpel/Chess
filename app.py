import pygame
import os
import numpy as np


class Chess:
    def __init__(self, player="w") -> None:

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p" for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["." for i in range(8)],
            ["P" for i in range(8)],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        
        if player not in ["w", "b"]:
            raise ValueError("Invalid starting color")
        elif player == "w":
            self.board = self.board[::-1]

        self.player = player
        self.white_turn = True
        self.game_history = []
        self.last_move= [] # (from_x, from_y, to_x, to_y , figure)

        self.close = False
        
    def print_board(self):
        """Function to print current board state
        """
        ascii_figures = {
            "p": "\u265F", # white
            "r": "\u265C",
            "n": "\u265E",
            "b": "\u265D",
            "q": "\u265B",
            "k": "\u265A",
            "P": "\u2659", # black
            "R": "\u2656",
            "N": "\u2658",
            "B": "\u2657",
            "Q": "\u2655",
            "K": "\u2658"
        }
        for row in self.board:
            row_str = ' '.join([ascii_figures[row[i]] if row[i] != "." else row[i] for i in range(len(row))])
            print(row_str)

    def main(self):
        """Main logic
        """
        self.print_board()
        while not self.close:
            move = self.get_move()
            print(move)
            break

    def get_move(self):
        """Get move from user

        :return: (x_from, y_from, x_to, y_to, figure)
        :rtype: tuple
        """
        while True:
            start = [i for i in input("Choose starting x and y (XY): ")]
            if self.check_input(start):
                x_start, y_start = int(start[0]), int(start[1])
                break

        while True:
            end = [i for i in input("Choose destination x and y (XY): ")]
            if self.check_input(end, False):
                x_end, y_end = int(end[0]), int(end[1])
                break
        return (x_start, y_start, x_end, y_end, self.board[x_start][y_start])
    
    def check_input(self, inp, start=True):
        """Check if provided input is valid

        :param inp: input (x, y cords)
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

        x, y = int(inp[0]), int(inp[1])

        if x not in acceptable or y not in acceptable:
            print("Wrong input! Indexes must be in range 0-7. (ex. '73')")
            return False

        if start:
            if self.board[x][y] == ".":
                print("Wrong input! There is no figure at that location!")
                return False

            if self.board[x][y].isupper() and self.player == "w":
                print("Wrong input! Please choose white figure!")
                return False
            elif self.board[x][y].islower() and self.player == "b":
                print("Wrong input! Please choose black figure!")
                return False
        else:
            if self.board[x][y].isupper() and self.player == "b" or self.board[x][y].islower() and self.player == "w":
                print("Wrong input! Wrong move!")
                return False
        return True
    
            
if __name__ == "__main__":
    chess_obj = Chess()
    chess_obj.main()
