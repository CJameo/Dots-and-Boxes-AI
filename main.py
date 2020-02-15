##############################################
###
### Runs the dots and boxes game
### May be replaced with dotsandboxes class
###
########################

from minimax import Minimax
from board import Board
import random

if __name__ == "__main__":

    starting_player = int(input("Which player would like to start the game?\n\nHuman: 1\nAI: -1\nRandom: 0\n\nEnter your choice: "))
    if starting_player not in [1,0,-1]:
        print("Invalid choice...Goodbye!")
        quit()
    if starting_player == 0:
        choices = [-1, 1] 
        starting_player = random.choice(choices)
    if starting_player == 1:
        print("Human goes first!")
    else:
        print("AI goes first!")

    difficulty = int(input("How unbeatable would you like the AI to be?\nEnter a number between 1 and 10: "))
    if difficulty not in [1,2,3,4,5, 6, 7, 8, 9, 10]:
        print("Invalid choice...Goodbye!")
        quit()
    algo = Minimax() # Pass in algo for AI move selection
    game_board = Board(starting_player)
    while not game_board.isOver():
        if game_board.player == 1:
            game_board.display()
            print("Choose an open edge to connect.\nType 'e' in row or col to end the game")
            r = int(input("row: "))
            c = int(input("col: "))
            game_board.makeMove(r, c)
        elif game_board.player == -1:
            game_board.display()
            r, c = algo.bestMove(root=game_board, search_depth=difficulty)
            game_board.makeMove(r, c)
            print("AI chose ({}, {})".format(r, c))

    if game_board.score > 0:
        game_board.display()
        print("Human wins! ... Wait what?")
    elif game_board.score < 0:
        game_board.display()
        print("AI wins! Better luck net time...")
    else:
        game_board.display()
        print("It's a draw!")  
    
