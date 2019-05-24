"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import user39_CjYkfB57FI_15 as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

#def conv_player(player):
#    """
#    Takes a player in poc_ttt_provided form and returns a player
#    as specified in SCORES.
#    """
#    if player == provided.PLAYERX:
#        return SCORES[

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner == None: # game still in progress
        moves, scores = [], []
        squares = board.get_empty_squares()
        for square in squares:
            brd = board.clone()
            brd.move(square[0], square[1], player)
            result = mm_move(brd, provided.switch_player(player))
            if result[0] * SCORES[player] == 1: # found a winning move
                return result[0], square
            scores.append(result[0])
            moves.append(square)
        max_score, move = scores[0], moves[0]
        for idx in range(1, len(scores)):
            if scores[idx] * SCORES[player] > max_score * SCORES[player]:
                max_score, move = scores[idx] * SCORES[player], moves[idx]
        return max_score, move
    else: # game over
        return SCORES[winner], (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    print "Initial board:\n", board
    print "Player", ("X" if player == provided.PLAYERX else "O"), "moves first"
    print
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
