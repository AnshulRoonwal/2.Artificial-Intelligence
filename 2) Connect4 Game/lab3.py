# 6.034 Fall 2010 Lab 3: Games
# Name: 1) "ADISINGH": ("SINGH_ADITI", "110285096")
        #2) "AROONWAL": ("ROONWAL_ANSHUL", "110554783")
# Email: <Your Email>

from util import INFINITY
from copy import deepcopy

global expandedNodesGlobal4AlphaBeta
expandedNodesGlobal4AlphaBeta=0

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher
import time

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)
# run_game(human_player, random_player)
## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)



########-----------------play  for MINIMAX------   ####################

tic = time.clock()
print "Running MINIMAX ALGORITHM"
run_game(new_player, basic_player )
toc = time.clock()
timeItr = toc - tic
print "Execution Time: " + str(timeItr)
expandedNodes = getnodesExpanded()
print "Nodes Expanded: " + str(expandedNodes)
setnodesExpandedToZeroB4NewGame()
########-----------------play  for MINIMAX------   ####################

# print '--------------------------------------------------Minimax Ends----------------------------------'

################################################    Part 2 of assignment: Minimax with Better Evaluation Funciton#######################################
# print '--------------------------------------Better Evaluation Minimax Begins----------------------------------'
# tic = time.clock()
# #run_game(basic_player, basic_player)
# run_game(new_player, random_player)
# toc = time.clock()
# timeItr = toc - tic
# print "Execution Time: " + str(timeItr)
# expandedNodes = getnodesExpanded()
# print "Nodes Expanded: " + str(expandedNodes)
# print '--------------------------------------Better Evaluation Minimax Ends----------------------------------'


## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

###---  https://en.wikipedia.org/wiki/Negamax         ---###

def alpha_beta_negamax (board, depth,eval_fn,alpha, beta): # recursion to calculate evaluation function
    if is_terminal(depth,board):
            #print "is_terminal reached"
            return (eval_fn(board),1)

    expandedNodes = 1
    col = 0

    for moves in get_all_next_moves(board):
        return_value_tuple=alpha_beta_negamax(moves[1],depth-1,eval_fn, -1*beta, -1*alpha)#send the reverse of alpha and beta
        expandedNodes = expandedNodes + return_value_tuple[1]        #-1 is required I guess,
        return_value = return_value_tuple[0]*-1
        alpha=max(return_value, alpha)
        if alpha>=beta:
            #col = moves[0]
            return (alpha,expandedNodes)
    return (alpha,expandedNodes)


def alpha_beta_search(board, depth,eval_fn,get_next_moves_fn=get_all_next_moves,is_terminal_fn=is_terminal):

    max_value=-9999999       # main functon which calls recursive evaluation function on top.
    expandedNodes = 0
    move_made=0
    #color=1
    alpha= -9999999
    beta= 9999999

    for moves in get_all_next_moves(board):
        return_value_tuple= alpha_beta_negamax(moves[1], depth-1,eval_fn, alpha, beta)
        expandedNodes = expandedNodes + return_value_tuple[1]
        global expandedNodesGlobal4AlphaBeta
        expandedNodesGlobal4AlphaBeta = expandedNodesGlobal4AlphaBeta + expandedNodes
        return_value=return_value_tuple[0]*-1
        #print "return_value==",return_value
        #print "return_value_tuple[0]==",return_value_tuple[0]

        if max_value==-9999999 or return_value >  max_value:
            #print "max_value",max_value
            max_value= return_value
            #print "max_value",max_value
            move_made=moves[0]
            #print "move_made=",move_made

    #print "total expanded nodes ", expandedNodes
    return move_made
print '--------------------------------------------------AlphaBeta Begins----------------------------------'


alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=basic_evaluate)    #Earlier the depth was 8, but in project2 Update, change was made

print "ALPHA BETA PRUNING...."


tic = time.clock()
run_game(alphabeta_player, basic_player)
toc = time.clock()
timeItr = toc - tic
print "Execution Time: " + str(timeItr)
print "Nodes Expanded: " + str(expandedNodesGlobal4AlphaBeta)


## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=basic_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""

