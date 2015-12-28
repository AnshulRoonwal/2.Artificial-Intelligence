__author__ = 'Anshul/Aditi'
import ReadGameState
import time
from Queue import PriorityQueue

global shouldIncrementChecks
shouldIncrementChecks = False

class backWithMRV:
    def __init__(self):
        self.board=[]
        self.AllEmptyPositions=[]
        self.consistencyChecks=0
        self.N = 0; self.M = 0; self.K = 0
        self.tic = time.clock()
        self.toc = 0

    def backTrackWithMRV(self, filename):
        readGame=ReadGameState.ReadGameState()
        self.board, self.AllEmptyPositions, self.N, self.M, self.K = readGame.readGameState(filename)
        veryFirstEmptyCell = 0
        self.mrvRecursive()
        return self.board, self.consistencyChecks

    def mrvRecursive(self):
        if len(self.AllEmptyPositions)==0:
            self.endAlgorithm()

        nextBlank=self.getMRV()#Get the most constrained blank

        row=nextBlank[0]
        col=nextBlank[1]

        #Try 1-9 for each blank
        for num in range(1, 10):
            if self.isValid(row, col, num, False):
                self.AllEmptyPositions.remove(nextBlank)
                #self.currentPathLength+=1
                self.board[row][col] = num
                #result=self.backTrackHeuristic()
                if self.mrvRecursive():
                   return
                else:
                #Backtrack
                   #self.currentPathLength-=1
                   #self.pathLengths.append(self.currentPathLength)
                   self.AllEmptyPositions.append(nextBlank)
                   self.board[row][col]=0

        return False


    def getMRV(self):

        #Build the MRV priority queue
        q = PriorityQueue()
        for blank in self.AllEmptyPositions:
            possible = self.getPossibleValues(blank, True)
            q.put((len(possible), blank))

        #Get the first one among (possibly equal)
        blanks = []
        blanks.append(q.get())
        minVal = blanks[0][0]

        #Build max Degree list
        while not q.empty(): #Get all equally-prioritized blanks
            next = q.get()
            if next[0] == minVal:
                blanks.append(next)
            else:
                break

        maxDeg = len(self.getNeighborBlanks(blanks[0][1]))
        maxDegBlank = blanks[0]

        for blank in blanks:
            degree = len(self.getNeighborBlanks(blank[1]))
            if degree > maxDeg:
                maxDegBlank = blank
                maxDeg = degree
        return maxDegBlank[1]

    def getPossibleValues(self, cell, heur):
        row=cell[0]
        col=cell[1]
        allowed=[]
        for i in range(1,10):
            if self.isValid(row, col, i, heur):
                allowed.append(i)

        return allowed

    def getNeighborBlanks(self, blank):
        row=blank[0]
        col=blank[1]

        neighbors=[]
        associatedBlanks=self.getRowBlanks(row)+self.getColumnBlanks(col)+self.getBoxBlanks(row, col)
        for blank in associatedBlanks:
            if blank not in neighbors and blank!=(row,col):
                #Might be that box collided with row / col so check here
                neighbors.append(blank)
        return neighbors

    '''
    Get neighboring cells in row
    '''
    def getRowBlanks(self, row):
        cells=[]
        for col in range(9):
            if self.board[row][col]==0:
                cells.append((row, col))
        return cells

    '''
    Get neighboring cells in column
    '''
    def getColumnBlanks(self, col ):
        cells=[]
        for row in range(9):
            if self.board[row][col]==0:
                cells.append((row,col))

        return cells

    '''
    Get neighboring cells in box
    '''
    def getBoxBlanks(self, row, col):
        cells=[]
        row=(row/3)*3
        col=(col/3)*3

        for r in range(3):
            for c in range(3):
                if self.board[row+r][col+c]==0:
                    cells.append((row+r,col+c))

        return cells

    def isValid(self, row, col ,num, heur):
        if heur==False:
            self.consistencyChecks+=1 #Increment number of constraint checks
        valid=False
        if num==0:
            return True
        else:
            #Return true if row, column, and box have no violations
            rowValid=self.checkRow(row, num)
            colValid=self.checkColumn(col, num)
            boxValid=self.checkBox(row, col, num)
            valid=(rowValid&colValid&boxValid)

        return valid

    '''
    Check if num is a legal value for the given row.
    '''
    def checkRow(self, row, num ):
        for col in range(9):
            currentValue=self.board[row][col]
            if num==currentValue:
                return False
        return True

    '''
    Check if num is a legal value for the given column.
    '''
    def checkColumn(self, col, num ):
        for row in range(9):
            currentValue=self.board[row][col]
            if num==currentValue:
                return False
        return True

    '''
    Check if num is a legal value for the box (one of 9 boxes) containing given row/col
    '''
    def checkBox(self, row, col, num):
        row=(row/3)*3
        col=(col/3)*3

        for r in range(3):
            for c in range(3):
                if self.board[row+r][col+c]==num:
                    return False
        return True

    def endAlgorithm(self):
        #self.pathLengths.append(self.currentPathLength) #Append the final path's length
        #self.runningTime=time.clock()-self.runningTime
        print "Solution found."
        #print ""
        #self.outputSolutionFile()
        self.printMetrics()
        exit(0)


    def printMetrics(self):
        print "+++++++++Metrics+++++++++"
        print ""
        #print "Constraint checks: "+str(self.constraintChecks)
        #print "Running time: "+str(self.runningTime)
        #print "Number of paths: "+str(len(self.pathLengths))
        #print "Deepest path: "+str(max(self.pathLengths))
        #print "Average path length: "+str(float(sum(self.pathLengths))/len(self.pathLengths))
        print ""
        print "Solved board: "
        self.printboard()
        print "+++++++++++++++++++++++++"
        print ""


    '''
    Return a string with '|'s inserted every 3 digits; format one row for printing the board neatly
    '''
    def formatRow(self, rowString):
        formattedString=""
        for i in range(0, len(rowString), 3):
            for j in range(0, 3):
                formattedString+=rowString[i+j]
            formattedString+="|"

        return formattedString

    def printboard(self):
        print "____________________"
        rowStrings=[]
        for i in range(9):
            rowString=[]
            for j in range(9):
                rowString.append(str(self.board[i][j])+" ")
            #print rowString
            rowStrings.append(self.formatRow(rowString))
        for i in range(0, len(rowStrings), 3):
            for j in range(0, 3):
                print rowStrings[i+j]
            print "--------------------"
