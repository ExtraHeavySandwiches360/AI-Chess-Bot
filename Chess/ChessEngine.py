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
        # The 1st character represents the color of the piece, 'b' or 'w'
        # The 2nd character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'P'
        # "--" - represents an empty space with no piece
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
        self.moveFunctions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}

        self.whiteToMove = True
        self.moveLog = []
    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''
    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # Log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # Swap players

    '''
    Undo the last move make
    '''
    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    '''
    All moves considering checks
    '''

    def get_valid_moves(self):
        return self.get_all_possible_moves() # For now, we will not worry about checks

    '''
    All moves without considering checks
    '''

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):          # Number of rows
            for col in range(len(self.board[row])): # Number of cols in given row
                turn = self.board[row][col][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves) # Calls the appropriate move function based on piece type
        return moves



    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''

    def get_pawn_moves(self, row, col, moves):
        if self.whiteToMove: # White pawn moves
            if self.board[row-1][col] == '--': # 1 square pawn advance
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--': # 2 square pawn advance
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col - 1  >= 0: # Captures to the left
                if self.board[row-1][col-1][0] == 'b' : # Enemy place to capture
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col + 1 <= 7: # Captures to the right
                if self.board[row-1][col+1][0] == 'b' :
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else: # Black pawn moves
            if self.board[row + 1][col] == '--':  # 1 square pawn advance
                 moves.append(Move((row, col), (row + 1, col), self.board))
                 if row == 1 and self.board[row + 2][col] == '--':  # 2 square pawn advance
                     moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:  # Captures to the left
                 if self.board[row + 1][col - 1][0] == 'w':  # Enemy place to capture
                     moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:  # Captures to the right
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))




    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): # Rook can move max of 7 squares
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--": # empty space valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color: #empty piece valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break


    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
    '''
    def get_knight_moves(self, row, col, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): # Bishop can move max of 7 squares
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":  # empty space valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:  # empty piece valid
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # Friendly piece invalid
                        break
                else:  # off board
                    break

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def get_king_moves(self, row, col, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

class Move():
    # Maps ranks to rows and files to columns
    RanksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    RowsToRanks = {v: k for k, v in RanksToRows.items()}
    FilesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    ColsToFiles = {v: k for k, v in FilesToCols.items()}

    def __init__(self, start_square, end_square, board):
        self.startRow = start_square[0]
        self.startCol = start_square[1]
        self.endRow = end_square[0]
        self.endCol = end_square[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.move_ID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False


    def get_chess_notation(self):
        # You can add to make this like real chess notation
        return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, row, col):
        return self.ColsToFiles[col] + self.RowsToRanks[row]