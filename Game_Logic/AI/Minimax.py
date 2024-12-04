# A simple Python3 program to find
# maximum score that
# maximizing player can get
import math


def AIturn(self):
    #try every single move he could do
    score=minimax()
    #undo the move
    if (score>bestscore):
        bestscore = score
        bestmove = move



def minimax(board,depth,ismaxmise)->score:
    #score=nom of pieces around opposite 's queen - number of pieces around my queen 
    score=board.count_pieces_around_opposite_queen() - board.count_pieces_around_my_queen()
    #if it's a leaf node, return the score
    Status=check_victory()
    if (Status==):
          return score

    
    #if maximizing player
    if (ismaxmise):
        bestscore=-10000000
        #try every single move he could do
        score=minimax(board,depth+1,False)
        #undo move
        bestscore=max(score,bestscore)
        return bestscore
    else:
        bestscore=10000000
        #try every single move the opp could do
        score=minimax(board,depth+1,True)
        #undo move
        bestscore=min(score,bestscore)
        
        return bestscore
