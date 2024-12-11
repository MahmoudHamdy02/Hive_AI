from Game_Logic.Game.GameController import GameController
import time



def ai_play(game_controller, max_time=1.0):  # max_time is in seconds
    orignal_board = game_controller.get_board()
    best_score = float('-inf')
    
    #start_time = time()  # Start the timer
    start_time = time.time()
    depth = 2  # Start with depth 1


    # Progressive deepening: Increase depth until time is up
  

    all_possible_moves =game_controller.get_all_possible_moves()
    for move in all_possible_moves:
        # Check if we've exceeded the allowed time
        # if time.time() - start_time > max_time:
        #     break  # Stop if the time limit is exceeded
        
        simulated_controller = game_controller.clone()

        # print(move[0],move[1])
        #m=move[0]
        # print(simulated_board.getPieceAt(m[0],m[1]))
        #print(move[0],move[1])
        
        simulated_controller.move_piece(move[0], move[1])
        print("what player", simulated_controller.get_current_player())
        score = minimax( depth, False,simulated_controller)
        
        if score > best_score:
            best_score = score
            best_move = move

    depth += 1  # Increase depth after each iteration

    # If the best move is found, execute it
    
    if best_move:
        print('Best move')
        game_controller.move_piece(best_move[0],best_move[1])

    return best_move






def minimax(depth,ismaxmise,game_controller):

    #score=nom of pieces around opposite 's queen - number of pieces around my queen 
    score=game_controller.count_pieces_around_opposite_queen() - game_controller.count_pieces_around_my_queen()
    print('Score=',score)
    #print (score)
    
    
    
    Status=game_controller.get_winner()
    if (Status!= 0 or depth==0 ):
        return score
    

    #itrative depening 

    
    #if maximizing player
    if (ismaxmise):
        bestscore=-10000000
        all_possible_moves =game_controller.get_all_possible_moves()
        for move in all_possible_moves:
            
            simulated_controller=game_controller.clone()
            
            simulated_controller.move_piece(*move)  # Apply the move
            score=minimax(depth-1,False,simulated_controller)
            #undo move #make function
            bestscore=max(score,bestscore)
        return bestscore
    else:
        bestscore=10000000
        #try every single move the opp could do
        all_possible_moves =game_controller.get_all_possible_moves()
        for move in all_possible_moves:
            simulated_controller=game_controller.clone()
            simulated_controller.move_piece(*move)  # Apply the move
            score=minimax(depth-1,True,simulated_controller)
            #undo move #make function
            bestscore=min(score,bestscore)
            print("bestscore from min " , bestscore)
        
        return bestscore

