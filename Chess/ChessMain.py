"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
from Chess import ChessEngine
# ********************
# * GLOBAL VARIABLES *
# ********************

WIDTH = HEIGHT = 512 # 512 is Max Resolution, anything bigger will cause the image to blur
DIMENSION = 8 # Dimensions of a chess board is 8x8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15 # Animation, duh?
IMAGES = {}

'''
 Initialize a global dictionary of images. This will be called exactly once in the main
'''
def load_images():
    pieces = ['wp', "wR", "wN", "wB", "wQ", "wK", 'bp', "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE)) # Loading an image of a chess piece
    # Note: we can access an image by saying 'IMAGES ['wp'] '
'''
The main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs =  ChessEngine.GameState()
    print(gs.board)
    load_images() # Only do this once, before the while Loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Responsible for all the graphics within a current game state.
'''
def draw_game_state(screen, gs):
    draw_board(screen, gs.board) # Draw squares on the board
    draw_pieces(screen, gs.board) # Draw pieces on the squares

'''
Draw the squares on the board. The top left square is always light.
'''
def draw_board(screen, board):
    colors = [p.Color("white"), p.Color("grey")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)] # r(Rows) + c(Columns) must not exceed 2
            p.draw.rect(screen, color, p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != "--":  # not empty space
                screen.blit(IMAGES[piece], p.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
'''
Draw the pieces on the board using the current GameState.board
'''
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": #not empty space
                screen.blit(IMAGES[piece], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))





if __name__ == '__main__':
    main()














