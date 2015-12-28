import pegSolitaireUtils
import config
import quopri
import Queue as Q
from copy import deepcopy

########################################################################################################
########################################################################################################


def ItrDeepSearch(pegSolitaireObject):  # this function is the main method to implement iterative deepening search
    for i in range(1,):					# it starts from 1 to infinity and the function "depLimSearch" is called iteratively
        returned_object=depLimSearch(pegSolitaireObject, i) # if the search is successful, an object with attributes
        if type(returned_object) == object:                           # nodesExpanded and trace is returned else -1
            break
    if type(returned_object) == object:
		pegSolitaireObject.nodesExpanded=returned_object.nodesExpanded # initialize the nodesExpanded and trace to the pegSolitaireObject
		pegSolitaireObject.trace=returned_object.trace

    return True

    # iterative deepening can be though of depth limited search where depth iterates over a range of 0 to infinity till the goal is reached
def depLimSearch(start, depth): # this is the function a called by "ItrDeepSearch(pegSolitaireObject)" iteratively
    count=0
    nodeToExplore = start    # make a copy of the Starting board state object
    trace_list=[]
    goal = [[-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1]]
           # goal is the board position of the final state which the game has to reach

    q = []				  # declare an empty stack
    child_parent_dict={}  # declare a dictionary to store child and parent relationship and the initial and next board position of pegs
    goal_found = 0
    total_iterations = 0
    depthCheck = 0
    peg_list = []
    visited = []
    q.append(nodeToExplore)  # make the start of the stack as the nodeToExplore i.e. Start Node

    while not q==[] or depthCheck<=depth :		 # run loop from 0 till infinity till either the stack gets empty or the depth passed is reached
        parent = q.pop()				 # pop an element from the stack and store as parent

        if parent.gameState == goal:	 # if parent == goal then set goal_found flag to 1 and break. else continue
            
            goal_found = 1
            break
        else:
            if parent.gameState not in visited:		   # check if parent already in the visited list, if not , only then explore it further
                visited.append(parent.gameState)	   # and add it to the visited list now
                peg_list = find_pegs(parent.gameState) # call function to find all the pegs on the current board position

                for peg in peg_list:  # for all peg positions on the board
                    for direction in config.DIRECTION:  # for all directions (N,S,E,W)
                        child=deepcopy(parent)			# now make the parent, i.e. the node to be expanded the child.
                        returned_value=child.getNextState(peg, direction) # check and return the next state of it

                        if returned_value:				# the getNextState sends false, ie move not valid then don't execute this block, else do
                            q.append(child)				# push the child to the stack	
                            nextPosition=peg[0] + 2 * config.DIRECTION[direction][0], peg[1] + 2 *config.DIRECTION[direction][1]
                            child_parent_dict.update({child:[parent,peg, nextPosition]}) # store child, its parent and peg (initial and next) positions in a dictionary
                            count=count+1				# count the number of nodes expanded
        depthCheck+=1									# update depth by one

    i=0

    if goal_found==0:
        print "GOAL NOT FOUND: UNSOLVABLE"
        return -1

    else:
         node=parent										# the node is set to the last child explored when the goal is found, i.e. the goal state

         while True:
            if start.gameState==node.gameState:				# stop if the initial game state is reached
                break
            trace_list.append(child_parent_dict[node][2])	# first the peg position after the move is appended to trace_list
            trace_list.append(child_parent_dict[node][1])	# then the initial peg position  is appended to trace_list

            node=child_parent_dict[node][0]		# on moving up from child to parent in the correct tree branch, 
												#node is set to its parent for the next iteration

    trace_list.reverse()
    start.trace=trace_list		# trace list is updated

    start.nodesExpanded=count	# nodesExpanded is updated for Start
    return start				# after updating the object attributes of "start" it is passed to "ItrDeepSearch"

########################################################################################################
########################################################################################################

def aStarOne(pegSolitaireObject):

    nodeToExplore = pegSolitaireObject	# store the original pegSolitaireObject to nodeToExplore
    goal = [[-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1]]
    count=0
    q = Q.PriorityQueue()  	# create a priority queue for a* search
    child_parent_dict={}	# create a dictionary to store child parent relationship to traverse the tree when goal found
    goal_found = 0
    total_iterations = 0
    peg_list = []
    visited = []			# this is the list of all visited nodes
    f_value = heuristic_function_1(nodeToExplore.gameState) # store the heuristic value of start node
    q.put((f_value, nodeToExplore))							# enqueue the start node

    while not q.empty():									# run loop till queue is empty
        parent = q.get()[1]									#dequeue and store the element as parent 
        
        if parent.gameState == goal:						# if goal found set flag goal_found as 1 and break
            goal_found = 1
            break
        else:												# else continue
            if parent.gameState not in visited:				# check if parent is not in the visited list, if not only then explore
                visited.append(parent.gameState)			# now add it to the visited list
                peg_list = find_pegs(parent.gameState)		# call function to find all the pegs on the current board position
                f_value = heuristic_function_1(parent.gameState) # call heuristic_function_1 to find the F(x) value


                for peg in peg_list:  # for all peg positions on the board
                    for direction in config.DIRECTION:  # for all directions (N,S,E,W)
                        child=deepcopy(parent)# now make the parent, i.e. the node to be expanded the child.
                        returned_value=child.getNextState(peg, direction) # check and return the next state of it

                        if returned_value:              # the getNextState sends false, ie move not valid then don't execute this block, else do
                            f_value = heuristic_function_1(child.gameState) # calculate the f(x) value

                            q.put((f_value, child))		# enqueue the child and the f_value	


                            child_parent_dict.update({child:[parent,peg, child.getNextPosition(peg,direction)]})# store child, its parent and peg (initial and next) positions in a dictionary
                            count=count+1				# count the number of nodes expanded
    trace_list=[]
    if goal_found==0:
        print "GOAL NOT FOUND: UNSOLVABLE"
    else:
        node=parent        # the node is set to the last child explored when the goal is found, i.e. the goal state

        while True:			# traverse the tree from last node (goal) to the first node (start state) till true
            if pegSolitaireObject.gameState==node.gameState:  # if the start state is reached, means that we have captured the whole trace from goal to start
               
                break
            trace_list.append(child_parent_dict[node][2])  # store the nextPosition of the peg 
            trace_list.append(child_parent_dict[node][1])  # store the initial of the peg 

            
            node=child_parent_dict[node][0]				# on moving up from child to parent in the correct tree branch, 
														#node is set to its parent for the next iteration
    trace_list.reverse()								# reverse the trace list and store it in pegSolitaireObject.trace
    pegSolitaireObject.trace=trace_list

    pegSolitaireObject.nodesExpanded=count

    return True


########################################################################################################
########################################################################################################


def aStarTwo(pegSolitaireObject):		# this is similar to the first A* search except some minor changes in the heuristic_function_2

    nodeToExplore = pegSolitaireObject	# store the original pegSolitaireObject to nodeToExplore
    goal = [[-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1]]
    count=0
    q = Q.PriorityQueue()  	# create a priority queue for a* search
    child_parent_dict={}	# create a dictionary to store child parent relationship to traverse the tree when goal found
    goal_found = 0
    total_iterations = 0
    peg_list = []
    visited = []			# this is the list of all visited nodes
    f_value = heuristic_function_2(nodeToExplore.gameState) # store the heuristic value of start node
    q.put((f_value, nodeToExplore))							# enqueue the start node

    while not q.empty():									# run loop till queue is empty
        parent = q.get()[1]									#dequeue and store the element as parent 
        
        if parent.gameState == goal:						# if goal found set flag goal_found as 1 and break
            goal_found = 1
            break
        else:												# else continue
            if parent.gameState not in visited:				# check if parent is not in the visited list, if not only then explore
                visited.append(parent.gameState)			# now add it to the visited list
                peg_list = find_pegs(parent.gameState)		# call function to find all the pegs on the current board position
                f_value = heuristic_function_2(parent.gameState) # call heuristic_function_1 to find the F(x) value


                for peg in peg_list:  # for all peg positions on the board
                    for direction in config.DIRECTION:  # for all directions (N,S,E,W)
                        child=deepcopy(parent)# now make the parent, i.e. the node to be expanded the child.
                        returned_value=child.getNextState(peg, direction) # check and return the next state of it

                        if returned_value:              # the getNextState sends false, ie move not valid then don't execute this block, else do
                            f_value = heuristic_function_2(child.gameState) # calculate the f(x) value

                            q.put((f_value, child))		# enqueue the child and the f_value	


                            child_parent_dict.update({child:[parent,peg, child.getNextPosition(peg,direction)]})# store child, its parent and peg (initial and next) positions in a dictionary
                            count=count+1				# count the number of nodes expanded
    trace_list=[]
    if goal_found==0:
        print "GOAL NOT FOUND: UNSOLVABLE"
    else:
        node=parent        # the node is set to the last child explored when the goal is found, i.e. the goal state

        while True:			# traverse the tree from last node (goal) to the first node (start state) till true
            if pegSolitaireObject.gameState==node.gameState:  # if the start state is reached, means that we have captured the whole trace from goal to start
               
                break
            trace_list.append(child_parent_dict[node][2])  # store the nextPosition of the peg 
            trace_list.append(child_parent_dict[node][1])  # store the initial of the peg 

            
            node=child_parent_dict[node][0]				# on moving up from child to parent in the correct tree branch, 
														#node is set to its parent for the next iteration
    trace_list.reverse()								# reverse the trace list and store it in pegSolitaireObject.trace
    pegSolitaireObject.trace=trace_list

    pegSolitaireObject.nodesExpanded=count

    return True

########################################################################################################################################
########################################################################################################################################

def find_pegs(node_state):				# this function finds all the pegs present on the current board state
    peg_list = []
    for i in range(0, 7):
        for j in range(0, 7):
            if (node_state[i][j] == 1):
                peg_list.append((i, j))
    #print peg_list
    return peg_list


def heuristic_function_1(object_a_star):  # This function calculates the Manhattan Distance Heuristic of the board.
    entropy = 0 						  # HF(board state) =
    numberOfPegs = 0 					  # absolute distance of each peg to reach goal(3,3)
    for i in range(0, 7):				  # for each cell of the board we calculate the
        for j in range(0, 7):			  # distance of each peg from (3,3)
            entropy += abs(i - 3) + abs(j - 3) # this is the  Manhattan distance of each peg from goal (3,3)
    return entropy

def heuristic_function_2(object_a_star):  # This function calculates the entropy of the board.
    entropy = 0 						  # HF(board state) = number of pegs still left on the board +
    numberOfPegs = 0 					  # absolute distance of each peg to reach goal(3,3)
    for i in range(0, 7):				  # for each cell of the board we calculate the board positions
        for j in range(0, 7):			  # which are still 1, signifying a peg.
            if object_a_star[i][j]:
                numberOfPegs += 1		  # get a sum of all the pegs
            entropy += abs(i - 3) + abs(j - 3) # then find the Manhattan distance of each peg from goal (3,3)
    entropy += numberOfPegs				  # add sum of all pegs and sum of Manhattan distances and return as entropy of the board
    return entropy
