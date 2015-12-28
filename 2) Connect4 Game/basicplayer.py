from util import memoize, run_search_function
import random
import connectfour

global expandedNodesGlobal
expandedNodesGlobal = 0


def basic_evaluate(board):
    # return random.randint(0,1000)
    # """
    # The original focused-evaluate function from the lab.
    # The original is kept because the lab expects the code in the lab to be modified.

    if board.is_game_over():
        #     # If the game has been won, we know that it must have been
        #     # won or ended by the previous move.
        #     # The previous move was made by our opponent.
        #     # Therefore, we can't have won, so return -1000.
        #     # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)
                    #     score=random.randint(0,1000)
    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


########    https://en.wikipedia.org/wiki/Negamax     #########
def minimax_nega_value(board, depth, eval_fn): #implementing the negamax algorithm for minimax using recursion
    if is_terminal(depth, board):              #checking if the depth is zero or is terminal state reached
        # print "is_terminal reached"
        return (eval_fn(board), 1)              #evaluating the board position and returning tuple with (score,no of nodes expanded)

    max_value = -9999999                        #using a high integer value instead of float("int")
    expandedNodes = 1                           #initially nodes expanded ==1
    col = 0
    for moves in get_all_next_moves(board):     # for all moves in board position do so
        return_value_tuple = minimax_nega_value(moves[1], depth - 1, eval_fn) # return_value_tuple returns (move,board)
        expandedNodes = expandedNodes + return_value_tuple[1]          # increase the exapnded nodes by 1
        return_value = return_value_tuple[0] * -1                       #since it is negamax, we inverse the value returned by minimax_nega for next recursive call
        if max_value != max(max_value, return_value):                   #make max_value as the max(max_value,return_value)
            max_value = max(max_value, return_value)
            # col = moves[0]

    tuple = (max_value, expandedNodes)          # return tuple with maximum heuristic calculated with expansion
    return tuple


def minimax(board, depth, eval_fn,   # main function which calls the recursive function for evaluation calculation above.
            get_next_moves_fn=get_all_next_moves,
            is_terminal_fn=is_terminal,
            verbose=True):
    max_value = -9999999
    expandedNodes = 0
    move_made = 0
    for moves in get_all_next_moves(board):
        return_value_tuple = minimax_nega_value(moves[1], depth - 1, eval_fn)
        expandedNodes = expandedNodes + return_value_tuple[1]
        return_value = -1 * return_value_tuple[0]

        if max_value != max(max_value, return_value):
            max_value = max(max_value, return_value)
            move_made = moves[0]
    setnodesExpanded(expandedNodes)
    # print "total expanded nodes ", expandedNodes
    return move_made


def setnodesExpanded(expandedNodesLocalReceived):
    global expandedNodesGlobal
    expandedNodesGlobal = expandedNodesGlobal + expandedNodesLocalReceived


def getnodesExpanded():
    return expandedNodesGlobal


def setnodesExpandedToZeroB4NewGame():
    global expandedNodesGlobal
    expandedNodesGlobal = 0


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


#########################---------- NEW EVALUATE FUNCTION---------------------#####################

def new_evaluate(board):
    if board.is_game_over():
        score = -1000
    else:
        score1 = board.longest_chain(board.get_current_player_id())  # calculating the length of the longest chain of the current player

        score2 = board.longest_chain(board.get_current_player_id())  # calulating the length of the other player
        score=(score1*score1*10)-(score2*score2)                     # getting the weighted square of the current player's moves and subtracting the other players weighted length
        # Prefer having your pieces in the center of the board.
        for row in range(6):                                        # calculating the normal distribution of the board positions making center preferred
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3 - col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3 - col)
    return score


#########################---------- NEW EVALUATE FUNCTION---------------------#####################

random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
