###########################################
#   SUDOKU SOLVER- 5 FUNCTIONS/METHODS    #
###########################################


#####################################################################################################
#                                    BACKTRACKING                                                    #
#####################################################################################################
global board
global checks
checks=0
def backtracking(filename):

    #board=()
    checks=0
    board,board_size,small_row,small_col=convertBoard(filename)




    #board,bool_val=backtrackingRecursive(board,board_size,small_row,small_col)

    board=[[0,0,0,0,0,1,9,8,0],
           [0,4,5,0,0,7,0,0,0],
           [0,0,2,0,0,0,6,0,0],
           [0,0,0,0,0,0,8,0,6],
           [0,0,0,4,0,3,0,0,0],
           [5,1,0,0,0,0,0,0,7],
           [2,6,0,0,5,0,3,0,0],
           [0,0,0,0,6,4,0,0,0],
           [7,0,8,0,0,0,0,0,0]]
    board_size=9
    printBoard(board,board_size)
    bool_val,checks=backtrackingRecursive(board,board_size,3,3,checks)
    #print board
    if (bool_val):
       print("\n successfully completed sudoku. ")
    else:
        print("\n not completed board. ",bool_val)
        return(board,checks)

    return (board,checks)

#-----Backtracking Recursive Function----------#

def backtrackingRecursive(board,board_size,small_row,small_col,checks):

    unassigned_row,unassigned_col=findNextPos(board,board_size)
    if unassigned_col==-1 and unassigned_row==-1:
        printBoard(board,board_size)
        print "\n checks=",checks
        return True,checks

    for digit in range (1,board_size+1):
        checks=checks+1
        unassigned_row,unassigned_col=findNextPos(board,board_size)
        if(boardValidate(digit,board,board_size,unassigned_row,unassigned_col,small_row,small_col)==True):
            board[unassigned_row][unassigned_col]=digit
            if( backtrackingRecursive(board,board_size,small_row,small_col,checks)[0]==True):
               return True,checks

            board[unassigned_row][unassigned_col]=0

    return False,checks

#####################################################################################################
#                                  BACKTRACKING + MRV                                               #
#####################################################################################################
def backtrackingMRV(filename):
    ###
    # use backtracking + MRV to solve sudoku puzzle here,
    # return the solution in the form of list of
    # list as describe in the PDF with # of consistency
    # checks done
    ###
    board=()
    checks=0
    board,board_size,small_row,small_col=convertBoard(filename)
    board=[[0,0,0,0,0,1,9,8,0],
           [0,4,5,0,0,7,0,0,0],
           [0,0,2,0,0,0,6,0,0],
           [0,0,0,0,0,0,8,0,6],
           [0,0,0,4,0,3,0,0,0],
           [5,1,0,0,0,0,0,0,7],
           [2,6,0,0,5,0,3,0,0],
           [0,0,0,0,6,4,0,0,0],
           [7,0,8,0,0,0,0,0,0]]
    board_size=9
    printBoard(board,board_size)
    bool_val,checks=backtrackingRecursiveMRV(board,board_size,3,3,checks)
    #print board
    if (bool_val):
       print("\n successfully completed sudoku. ")
    else:
        print("\n not completed board. ",bool_val)
        return(board,checks)

    return (board,checks)

#-----Backtracking+MRV Recursive Function----------#

def backtrackingRecursiveMRV(board,board_size,small_row,small_col,checks):

    #unassigned_row,unassigned_col,board_dict=findNextPosMRV(board,board_size,small_row,small_col)
    #print("\n unassigned row,col=",unassigned_row,unassigned_col)

    #base case
    if boardFull(board,board_size):
        printBoard(board,board_size)
        print "\n checks=",checks
        return True

    #initial board_dict
    board_dict=updateDict(board,board_size,small_row,small_col,board_dict={})
    print board_dict

    for digit in range(1,board_size*board_size+1):
        unassigned_row,unassigned_col,board_dict=findNextPosMRV(board,board_size,small_row,small_col)
        print("\n unassigned row,col=",unassigned_row,unassigned_col,board_dict[board_size*unassigned_row+unassigned_col][0])
        if(boardValidate(digit,board,board_size,unassigned_row,unassigned_col,small_row,small_col)==True):
            print("\n boardValidate==True for digit",digit)
            board[unassigned_row][unassigned_col]=digit
            printBoard(board,board_size)

            if(backtrackingRecursiveMRV(board,board_size,small_row,small_col,checks)==True):
                print("\n not backtracking")
                return True
            print("\n  backtracking")
            board[unassigned_row][unassigned_col]=0

    return False

#####################################################################################################
#                                   BACKTRACKING + MRV + FORWARD PROPOGATION                        #
#####################################################################################################

def backtrackingMRVfwd(filename):


    board=()
    checks=0
    board,board_size,small_row,small_col=convertBoard(filename)


    return (board,checks)


#####################################################################################################
#                                     BACKTRACKING + MRV + CONSTRAINT PROPOGATION                   #
#####################################################################################################

def backtrackingMRVcp(filename):


    board=()
    checks=0
    board,board_size,small_row,small_col=convertBoard(filename)


    return (board,checks)


#####################################################################################################
#                                          MINIMUM CONFLICT                                         #
#####################################################################################################

def minConflict(filename):


    board=()
    checks=0
    board,board_size,small_row,small_col=convertBoard(filename)


    return (board,checks)

#######################-----------------UTILITY FUNCTIONS--------------------------################

#####################################################################################################
#                   function to convert strings in file to a list of lists (Board)                  #
#####################################################################################################
def convertBoard(filename):
    board=()
    raw=()
    checks=0

    fileHandle= open(filename,'r')
    firstLine=fileHandle.readline().strip(';\n').split(',')
    board_size=int(firstLine[0])
    small_row=int(firstLine[1])
    small_col=int(firstLine[2])
    print ("\n boardsize,smallrow,smallcol=",board_size,small_row,small_col)

    raw= fileHandle.readlines()
    if(len(raw)!=board_size):
        print "\n Wrong Input. Board size doesn't match"
        exit(0)

    board = [[0 for x in range(board_size)] for x in range(board_size)]

    for i in range(0,board_size):
        raw[i]=raw[i].strip(';\n')

    for i in range(0,board_size):
        x=raw[i].split(',')
        if(len(x)!=board_size):
            print "\n Wrong Input. Board size doesn't match"
            exit(0)
        for j in range(0,board_size):
            if not x[j]=='-':
               board[i][j]=int(x[j])
    print("\n return from convert board")
    return board,board_size,small_row,small_col


#####################################################################################################
#                   board_validate function                                                         #
#####################################################################################################

def boardValidate(digit,board, board_size,row,col,small_row,small_col):

    value=digit
    for i in range (0,board_size):
        if board[i][col]==value:
            return False
        if board[row][i]==value:
            return False
    #check which small box does the value lie in
    box_row_start=row-(row%small_row)
    box_col_start=col-(col%small_col)

    for i in range(box_row_start,box_row_start+small_row):
         for j in range(box_col_start,box_col_start+small_col):
             if value==board[i][j]:
                 return False
    return True

#####################################################################################################
#                   Function to find Next Row and Column for Backtracking                           #
#####################################################################################################

def findNextPos(board, board_size):

    for i in range(0,board_size):
        for j in range(0,board_size):
            if board[i][j]==0:
                return i,j  #return the next position which is a hole
    return -1,-1    #if the whole board is complete means that sudoku completed
                    #return out of board value and check it in the basr condition for recursion

#####################################################################################################
#                   Function to find Next Row and Column for Backtracking+MRV                       #
#####################################################################################################

def findNextPosMRV(board, board_size,small_row,small_col):
    min=1
    i=0
    j=0
    board_dict={}
    board_dict=updateDict(board,board_size,small_row,small_col,board_dict)
    for elements in board_dict:
        if min>=board_dict[elements][1]:
            min=board_dict[elements][1]
            i=board_dict[elements][2]
            j=board_dict[elements][3]
    if boardFull(board,board_size):
        print "\n board is full in findNextPosMRV function"
        return -1,-1,[0]
    else:
        print "\n returning min value min=%d, board_dict=%d",min,board_dict[i*board_size+j][1]
        return i,j,board_dict
#####################################################################################################
#                   Function to update valid moves                                                  #
#####################################################################################################

def updateDict(board, board_size,small_row,small_col,board_dict):
    pos=0

    for i in range(0,board_size):
        for j in range(0,board_size):
            if board[i][j]==0:
                pos=(board_size*i)+j  #this position is used as key for dictionary hashing
                list=findAllValidValues(board,board_size,small_row,small_col,i,j)
                board_dict.update({pos:(list,len(list),i,j)})
            #else:
            #    del board_dict[pos]
    return board_dict

###----------------Find all Valid values that the cell can take---------####

def findAllValidValues(board,board_size,small_row,small_col,row,col):

    list = [x for x in range(1,board_size+1)] #initialize list with all values

    for i in range(0,board_size):
        if board[i][col]!=0:
            try:
                list.remove(board[i][col])
            except ValueError:
                continue

        if board[row][i]!=0:
            try:
                list.remove(board[row][i])
            except ValueError:
                continue


    #check which small box does the value lie in
    box_row_start=row-(row%small_row)
    box_col_start=col-(col%small_col)

    for i in range(box_row_start,box_row_start+small_row):
         for j in range(box_col_start,box_col_start+small_col):
             if board[i][j]!=0:
                 try:
                    list.remove(board[i][j])
                 except ValueError:
                     continue
    return list


#####################################################################################################
#                   Function to find if board completed                                             #
#####################################################################################################

def boardFull(board,board_size):
    for i in range(0,board_size):
        for j in range(0,board_size):
            if board[i][j]==0:
                return False
    return True


#####################################################################################################
#                   Function to print the Final State                                               #
#####################################################################################################

def printBoard(board,board_size):
    for i in range(0,board_size):
        print(board[i])

#####################################################################################################
