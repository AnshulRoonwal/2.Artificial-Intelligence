import readGame
import config


#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.trace = []

    def is_corner(self, pos):
        if self.gameState[pos[0]][pos[1]] == -1:
            return True
        else:
            return False


    def getNextPosition(self, oldPos, direction):
        newPos = oldPos[0] + 2 * config.DIRECTION[direction][0], oldPos[1] + 2 * config.DIRECTION[direction][1]

        return newPos

    def is_validMove(self, oldPos, direction):

        newPos = self.getNextPosition(oldPos, direction)

        midPos = oldPos[0] + config.DIRECTION[direction][0], oldPos[1] + config.DIRECTION[direction][1]
        if self.is_corner(oldPos):
            return False
        #########################################

        ########################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # check for cases like:
        # if new move is already occupied
        # or new move is outside peg Board
        # Remove next line according to your convenience
        # Anshul, Checking if 1) Not out of Board 2) Not already Occupied 3) Position is available, ie: = 0 4) midPos = 1
        if newPos[0] < 0 or newPos[0] > 6 or newPos[1] < 0 or newPos[1] > 6:  # Checked if outside the board
            return False
        if self.gameState[newPos[0]][newPos[1]] == 1 or self.gameState[newPos[0]][newPos[1]] != 0:  # Checked if newPos is already occupied (==1), and if it is 0 and not -1
            return False
        if self.gameState[midPos[0]][midPos[1]] != 1:  # Checked if midPos is 1 and nothing else, if it is something other than 1, return False
            return False

        if self.is_corner(newPos):
            return False
        if self.is_corner(midPos):
            return False

        # elif((self.gameState[newPos[0]][newPos[1]]== 0) and (self.gameState[midPos[0]][midPos[1]]== 1)):
        # #if(pegHolder[newPos[0]][newPos[1]]== 0):
        # 	return True
        return True  # Return true as a validMove since we checked for all wrong conditions.

    def getNextState(self, oldPos, direction):
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            #print "Error, You are not checking for valid move"
            return False
        # exit(0)
        ###############################################

        ###############################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # Update the gameState after moving peg
        # eg: remove crossed over pegs by replacing it's
        # position in gameState by 0
        # and updating new peg position as 1
        else:
            newPos = self.getNextPosition(oldPos,
                                          direction)  # capture newPos from the return function of getNextPosition
            middlePeg = oldPos[0] + config.DIRECTION[direction][0], oldPos[1] + config.DIRECTION[direction][1]
            # pegHolder[newPos[0]][newPos[1]]=1                #convert
            # pegHolder[oldPos[0]][oldPos[1]]=0
            self.gameState[newPos[0]][newPos[1]] = 1
            self.gameState[middlePeg[0]][middlePeg[1]] = 0
            self.gameState[oldPos[0]][oldPos[1]] = 0
            #return self.gameState
            return True