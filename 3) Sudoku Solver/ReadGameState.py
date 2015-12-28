__author__ = 'Anshul/Aditi'

class ReadGameState:
    def __init__(self):
        self.board = []
        self.AllEmptyPositions = []


    def readGameState(self, filePath):				#New Function for reading game state
        #Reading file
        fileHandle = open(filePath, 'r')
        rawState = fileHandle.readline().strip().split(';')		##replace , with ;
        # print rawState		#Debug
        # print rawState[0]	#Debug
        # print len(rawState[0])
        configuration = rawState[0].split(',')
        #print configuration
        N = configuration[0];	M = configuration[1];	K = configuration[2];
        #print 'N=', N, 'M=', M, 'K=', K
        #updating game state with all 0
        N=int(N); M=int(M); K=int(K);
        if (N!=M*K):
            print "What is this man! Don't know basic Sudoku configuration? N=MxK should be maintained"
            exit(0)
        self.board = [[0 for i in range(N)] for j in range(N)]
        self.AllEmptyPositions = []
        #check for dimension of given board
        if len(rawState) != N+2:
            print "Wrong gameState given, check txt file"
            exit(0)
        else:
            for i in range(N):
                row = rawState[i+1].split(',')
                if len(row) != N:
                    print "Wrong gameState given, check txt file"
                    exit(0)
                else:
                    for j in range(N):							#Ignored the condition of a character other than '-' and 'A number'
                        if row[j] not in('-','1','2','3','4','5','6','7','8','9','10','11','12'):
                            print 'Wrong characters in the input file, plz check it. It should have either '-' or number between 1 to 9'
                            exit(0)
                        if row[j] == '-':
                            self.board[i][j]=int("0")
                            self.FindEmptyPosition(i,j)
                        else:
                            self.board[i][j]=int(row[j])
            return self.board, self.AllEmptyPositions, N,M,K


    def FindEmptyPosition(self,i,j):
        self.AllEmptyPositions.append([i,j])