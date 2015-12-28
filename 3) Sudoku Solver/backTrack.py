__author__ = 'Anshul/Aditi'
import ReadGameState
import time
class cspClass:
    def __init__(self):
        self.board=[]
        self.AllEmptyPositions=[]
        self.consistencyChecks=0
        self.N = 0; self.M = 0; self.K = 0
        self.tic = time.clock()
        self.toc = 0

    def backtracking(self, filename):                       ##added self as first parameter
        #print "filename ", filename
        readGame=ReadGameState.ReadGameState()
        self.board, self.AllEmptyPositions, self.N, self.M, self.K = readGame.readGameState(filename)
        veryFirstEmptyCell = 0
        self.backTrack(veryFirstEmptyCell)
        return self.board, self.consistencyChecks

    def backTrack(self, emptyPosition):
        areMoreEmpty = len(self.AllEmptyPositions)-1
        if emptyPosition>areMoreEmpty:
            self.exitCondition()

        #Haven't found a solution yet; get coords of the blank
        row=self.AllEmptyPositions[emptyPosition][0];   col=self.AllEmptyPositions[emptyPosition][1]

        #Try numbers in range 1 to N .
        for num in range(1, self.N+1):
            if self.isValid(row, col, num):
                #If the number is valid, increment current path by 1.
                self.board[row][col] = num
                self.backTrack(emptyPosition+1)

        #No number found...set back to 0 and return to the previous blank
        emptyPosition-=1
        self.board[row][col]=0

    def isValid(self, row, col ,num):
        self.consistencyChecks+=1 #Increment number of constraint checks
        valid=False
        if num==0:
            return True
        else:
            return ((not self.isRowSafe(row, num)) and (not self.isColSafe(col, num)) and (not self.isGridSafe(row - row%self.M, col - col%self.K, num)))

    '''
    Check if num is a legal value for the given row.
    '''
    def isRowSafe(self, row, num ):
        for col in range(self.N):
            currentValue=self.board[row][col]
            if num==currentValue:
                return True
        return False

    '''
    Check if num is a legal value for the given column.
    '''
    def isColSafe(self, col, num ):
        for row in range(self.N):
            currentValue=self.board[row][col]
            if num==currentValue:
                return True
        return False

    '''
    Check if num is a legal value for the box M x K containing given row/col
    '''
    def isGridSafe(self, row, col, num):
        for r in range(self.M):
            for c in range(self.K):
                if self.board[row+r][col+c]==num:
                    return True
        return False


    def exitCondition(self):
            print "Backtracking:"
            self.toc = time.clock()
            timeItr = self.toc - self.tic
            print "Execution Time: " + str(timeItr)
            print "Consistency Checks: " + str(self.consistencyChecks)
            print "Solution: "
            self.printPuzzle()
            exit(0)

    def printPuzzle(self):
        print "____________________"
        rowStrings=[]
        for i in range(self.N):
            rowString=[]
            for j in range(self.N):
                rowString.append(str(self.board[i][j])+" ")
            #print rowString
            rowStrings.append(self.formatRow(rowString))
        for i in range(0, len(rowStrings), 3):
            for j in range(0, 3):
                print rowStrings[i+j]
            print "--------------------"

    def formatRow(self, rowString):
        formattedString=""
        for i in range(0, len(rowString), 3):
            for j in range(0, 3):
                formattedString+=rowString[i+j]
            formattedString+="|"

        return formattedString


