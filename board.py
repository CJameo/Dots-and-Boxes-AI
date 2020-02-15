#########################################################
###
### Board class used to create Board() objects
### Used to hold the game_board, represent child states
###
#########################
import copy
from random import randint

class Board(object):
    
    def __init__(self, player=1, score=0, board=[], parent=None, move=None, value=None, depth=0):
        self.player = player # player = 1 or player = -1 -> player =  (Min) or player = (Max) respectivley
        self.score = score # Begin game at zero score, if negative winner(Min) else winner(Max)
        self.board = copy.deepcopy(board) # To avoid unintentional game_board mutation
        self.parent = parent # Not actually used for much...May implement undo() fucntionality
        self.move = move # The move which took us to this state (Used to determine AI next move)
        self.value = value # The value of this node when evaluated against it's worst case subtree
        self.depth = depth # The depth the node sits at (game_board always sits at zero)
        self.moves_remaining = float("inf") # Used to determine game over (num_possible_moves = 2*n*(n-1) for square game_board)
        self.children = [] # Holds the output of board.getChildren()
        
        if board == []: # game_board has not been created yet
            size = int(input("How large would you like the board to be (N x N)? \n Enter an integer: ")) # Produces only square game_board
            if type(size) != type(0): # Non integer argum,ent supplied
                print("Invalid argument, default to size 3") # Default size(game_board) = 3
                self.createBoard() # Default Constructor
            self.createBoard(size) # arg(size) passed in if size was valid

    def createBoard(self, size=3):
        self.moves_remaining = 2*size*(size-1) # (num_possible_moves = 2*n*(n-1) for square game_board)
        if self.board == []: # Double check game board has not been created
            for row in range(0, size*2 - 1): 
                self.board.append([]) # Each row will be represented by a list
                for col in range(0, size*2 - 1):
                    try:
                        if (row%2 == 0 and col%2 == 0): # Even tuples correspond to vertices
                            self.board[row].append("*")
                        elif (row%2 == 1 and col%2 == 1): # Odd tuples correspond to spaces
                            self.board[row].append(randint(1, 9)) # Assign random value to space
                        elif ((row%2 == 0) ^ (col%2 == 0)): # (even, odd) and (odd, even) tuples exist between vertices
                            if row%2 == 0:
                                self.board[row].append("   ") # Even rows are horizontal
                            else:
                                self.board[row].append(" ") # Even cols are vertical
                    except:
                        print("Unexpected Error When Creating Game Board") 
                   
    def makeMove(self, row=0, col=0):
        if ((row < 0) or (row > len(self.board))) or ((col < 0) or (col > len(self.board[0]))): # Beyond game_board indices
            return "Out Of Bounds"
        if not ((row%2 == 0) ^ (col%2 == 0)): # A space or a vertex not valid for line drawing
            return "Not A Valid Move"
        elif ((self.board[row][col] != " ") and (self.board[row][col] != "   ")): # If not whitespace...Edge is filled
            return "Edge Already Filled"
        elif row%2 == 0: 
            self.board[row][col] = "---"  # Horizontal line can complete top or bottom squares
            if (self.completeSquare(row-1, col)): # Check if top square complete
                self.score += (self.player * self.board[row-1][col]) # Adjust score based on player = (Min) or player = (Max)
            if (self.completeSquare(row+1, col)): # Check if bottom square complete
                self.score += (self.player * self.board[row+1][col]) # Adjust score based on player = (Min) or player = (Max)
            self.player = (-1 * self.player) # Switch players
        else:
            self.board[row][col] = "|" # Vertical line can complete left or right squares
            if (self.completeSquare(row, col-1)): # Check if left square complete
                self.score += (self.player * self.board[row][col-1]) # Adjust score based on player = (Min) or player = (Max)
            if (self.completeSquare(row, col+1)): # Check if right square complete
                self.score += (self.player * self.board[row][col+1]) # Adjust score based on player = (Min) or player = (Max)
            self.player = (-1 * self.player) # Switch players
        self.moves_remaining -= 1 # Number of possible edges = moves_remaining
        
    def completeSquare(self, row, col): # Row col correspond to indices of a square
            if ((row > 0) and (col > 0) and\ 
                (row < len(self.board) - 1) and\
                (col < len(self.board[0]) - 1)): # Do not exceed game boundaries
                return ((self.board[row-1][col] == "---") and\
                        (self.board[row+1][col] == "---") and\
                        (self.board[row][col-1] == "|") and\
                        (self.board[row][col+1] == "|")) # Check top, bottom, left, right for filled edges
                
    def getChildren(self):
        p, s, b, pr, d = self.player, copy.deepcopy(self.score), copy.deepcopy(self.board), self, (self.depth+1) # Copy attrs of parent
        for row in range(0, len(self.board)): # Iterate over game_board
            if row%2 == 0: # Row is even
                for col in range(1, len(self.board[0]), 2): # Col must be odd if valid move
                    if self.board[row][col] != "---": # Odd cols = horizontal lines...If not filled then is a valid move
                        child = Board(player=p, score=s, board=b, parent=pr, move=(row, col), depth=d) # Child starts with parent attrs
                        child.makeMove(row, col) # makeMove changes only child configuration
                        self.children.append(child) # Append mutated child to list of children
            else:
                for col in range(0, len(self.board[0]), 2): # If row not even col must be even 
                    if self.board[row][col] != "|": # Even cols = vertical lines...If not filled then is a valid move 
                        child = Board(player=p, score=s, board=b, parent=pr, move=(row, col), depth=d) # Child starts with Parent attrs
                        child.makeMove(row, col) # makeMove changes only child configuration
                        self.children.append(child) # Append mutated child to list of children
               
    def isOver(self): # Boolean to check game status
        if self.moves_remaining <= 0:
            return True
        return False
        

    def display(self): # Display method for gameplay (could have overrode print but thought it more useful to maintain built in functionality)
        board = self.board
        print("  ", end='')
        for idx in range(0, len(board[0])): # print indices on edges
            if idx%2 == 1:
                print(" {} ".format(idx), end='')
            else:
                print(idx, end='')
        print("\n")
        for row in range (0, (len(board))):
            print("{} ".format(row), end='')
            for col in range(0, (len(board[0]))):
                if (row%2 ==0) and (col%2 ==0):
                    print(board[row][col], end='')
                elif row%2 == 0:
                    print(board[row][col], end='')
                elif col%2 == 0:
                    print(board[row][col], end='')
                else:
                    print(" {} ".format(board[row][col]), end='')
            print("\n")
        print("\n")
        print(self.score)
                        
    def copy(self): # Copy method to avoid unintentoinal mutation
        p, s, b, pr, m, d = self.player, copy.deepcopy(self.score), copy.deepcopy(self.board), self, self.move, self.depth
        return Board(p, s, b, pr, m, d)
    
    def getScore(self): # Avoids score mutation
        return copy.deepcopy(self.score)   
