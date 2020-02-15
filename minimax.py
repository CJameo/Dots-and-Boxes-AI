###################################
### 
### Minimax class to create Minimax() objects
### Used by AI to determine next move
###
################

from board import Board

class Minimax(object):
    
    def minMax(self, root, search_depth, alpha=float("-inf"), beta=float("inf")): # Search depth determines level of AI intelligence
        root.getChildren() # Get direct offspring of parent node (valid moves from initial state)
        if (root.depth >= search_depth) or (len(root.children) == 0): # Bottom of the tree or terminal node
            return root.score # Score at this state will percolate up as value
        if root.player == 1: # Human player (Max)
            bestValue = float("-inf") # Current best is worst possible for (Max)
            for child in root.children: # Check direct offspring for state (percolated from maximum horizon)
                value = self.minMax(child, (search_depth-1), alpha, beta) # Value percolates from score (above)
                if value > bestValue: 
                    bestValue = value # Update bestValue if we've found a better one for (Max)
                if bestValue > alpha:
                    alpha = bestValue # Update alpha for this search
                if beta <= alpha: # Prune remaining nodes on this branch
                    break # No need to continue down this path as solution is guaranteed sub-optimal
            root.value = bestValue # The value of this move will be the best value achieved
            return bestValue # Return this value to minMax (percolation)
        
        elif root.player == -1: # AI player (Min)
            bestValue = float("inf") # Current best is worst possible for (Min)
            for child in root.children: # Check direct offspring for state (percolated from maximum horizon)
                value = self.minMax(child, (search_depth-1), alpha, beta) # Value percolates from score (above)
                if value < bestValue:
                    bestValue = value # Update bestValue if we've found a better one for (Min)
                if bestValue < beta:
                    beta = bestValue # Update alpha for this search
                if beta <= alpha:
                    break # No need to continue down this path as solution is guaranteed sub-optimal
            root.value = bestValue # the value of this move will be the best value achieved
            return bestValue  # Return this value to minMax (percolation)
    
    def bestMove(self, root, search_depth):
        root = root.copy() # Copy to ensure game_board remains unchanged
        best = self.minMax(root, search_depth, float("-inf"), float("inf")) # Begin recursive call to minMax
        for child in root.children: # Direct offspring values will have been computed by minMax at this stage
            if child.value == best: # Finds the child whose value was returned by minMax (The 1st if there are multiple value = best)
                move = child.move # The move that produced the optimal subtree
                return move # Return move to be used by AI
            move = child.move # If there was no best value the remaining move will be used (Stops AI avoiding loss)
        return move # Return move to be used by AI
        
