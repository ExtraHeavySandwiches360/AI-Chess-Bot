"""
    How to take notes:
    # (1) Tell us what that function do.
    # (2) What is the input and the output.
    # (3) (Optional)  How fast can it run > (Check on Big-Oh Notation).
"""
"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # Board is a 8x8 2D list, each element of the list has 2 characters
        #The 1st character represents the color of the piece, 'B' or 'W'
        #The 2nd character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        #"--" - represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
