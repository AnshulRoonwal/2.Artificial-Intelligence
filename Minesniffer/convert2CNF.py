import copy
import sys
from itertools import combinations



#Logic to get the grid from the input file cnf.txt
def parse_file(filepath):
    file = open(filepath)
    gridConfiguration = file.readline().split()
    N = int(gridConfiguration[0]);    M = int(gridConfiguration[1])       ##Get the grid configuration of NxM ie; Rows X Column

    gridRows = file.readlines()
    grid = []                                                             ## A list grid to hold the grid Configuration
    for rows in gridRows:
        grid.append(rows.strip().split(','))

    #Remove all 'X' from input and replace them with negative of i_th mine appearance.
    for x in range(N):
        for y in range(M):
            if grid[x][y] == 'X':
                count=0
                for i in range(x+1):                                    #Logic to count the number of mines already encountered
                    for j in range(M):
                        if grid[i][j] == 'X' or int(grid[i][j]) < 0:
                            count = count+1                             #Give proper number to the mine count.
                        if i==x and y == j:
                            break
                count=count*-1                                          #Since we are representing mines by negative value
                grid[x][y] = count
                count=0                                                 #Make the count zero again since we are counting from the begining again.
            else:
                grid[x][y] = int(grid[x][y])
    print "Current grid is ", grid, "\n"
    file.close()

    return grid, N, M

#Method to find out the mine information holders in the whole grid
def mine_value_holders(grid, N, M):
    non_mine_value_positions = []

    for i in range(N):
        for j in range(M):
            if grid[i][j] >0:                               #Take non negative ones, because negative ones are mines.
                tupl = (i,j)
                non_mine_value_positions.append(tupl)
        
    return non_mine_value_positions

#Method to find mines around the passes cell in order specified against each one of them below.
def get_cell_values_around_me(grid, N, M, cell):
    positions_of_mines = []
    x,y = cell


    if (x-1 >= 0 and y-1 >= 0 ):                        #1) neighbour in NORTH-WEST
        positions_of_mines.append(-grid[x-1][y-1])
    if (y-1 >= 0 ):                                     #2) neighbour in WEST
        positions_of_mines.append(-grid[x][y-1])
    if (x+1 < N and y-1 >= 0 ):                         #3) neighbour in SOUTH-WEST
        positions_of_mines.append(-grid[x+1][y-1])
    if (x-1 >= 0 ):                                     #4) neighbour in NORTH
        positions_of_mines.append(-grid[x-1][y])
    if (x+1 < N ):                                      #5) neighbour in SOUTH
        positions_of_mines.append(-grid[x+1][y])
    if (x-1 >= 0 and y+1 < M ):                         #6) neighbour in NORTH-EAST
        positions_of_mines.append(-grid[x-1][y+1])
    if (y+1 < M ):                                      #7) neighbour in EAST
        positions_of_mines.append(-grid[x][y+1])
    if (x+1 < N and y+1 < M ):                          #8) neighbour in SOUTH-EAST
        positions_of_mines.append(-grid[x+1][y+1])

    return positions_of_mines

#Method to check if the board is valid by  comparing the info value at board with the mines given around it.
def checkForInvalidInput(cell,grid,N,M):
    x,y=cell
    no_of_mines = grid[x][y]                #Got value at that cell about how many mines are present.
    temp_positions_of_mines = get_cell_values_around_me(grid, N, M, cell)    #Get how many mines are present arounf this cell
    positions_of_mines=[]
    for i in range (0,len(temp_positions_of_mines)):
        if temp_positions_of_mines[i]>=0:                               
            positions_of_mines.append(temp_positions_of_mines[i])       #Append only the mines and leave the rest
    if no_of_mines > len(positions_of_mines):
        print "Wrong grid, the count of mine exceeds the mines around it."
        return False
    return True

#Compute conjunctive_form for the given grid state
def convert2conjunctive_form(grid, N, M, output):
    # interpret the number constraints
    
    grid_size = N*M + 1                         #Keep the grid size for extra dnf rows

    non_mine_value_positions = mine_value_holders(grid, N, M)   #FInd the cells with info values abt the mines.

    isInvalidgrid = False
    conjunctive_form = []

    #Create DNF for every info cell and append keep appending to cnf
    for cell in non_mine_value_positions:
        isInvalidgrid = checkForInvalidInput(cell,grid,N,M)         #Check for the validity of the grid
        if not isInvalidgrid:
            break

        x, y = cell
        no_of_mines = grid[x][y]
        temp_positions_of_mines = get_cell_values_around_me(grid, N, M, cell)

        positions_of_mines=[]
        for i in range (0,len(temp_positions_of_mines)):
                    if temp_positions_of_mines[i]>=0:
                        positions_of_mines.append(temp_positions_of_mines[i])

        possible_combinations = list(combinations(positions_of_mines, no_of_mines))         #Find all the combinations of possible mines choose number of mines

        disjunctive_form = []

        #find DNF for each info cell
        for i in range(0,len(possible_combinations)):
            temp_positions = copy.deepcopy(positions_of_mines)
            for x in range(0, len(temp_positions)):
                temp_positions[x]= -1*temp_positions[x]

            this_combination = list(possible_combinations[i])
            for j in range(0,len(temp_positions)):
                if temp_positions[j]*-1 in this_combination:
                    temp_positions[j] = -1*temp_positions[j]


            if temp_positions not in disjunctive_form:
                disjunctive_form.append(temp_positions)

        #pass the dnf and cnf, append this dnf to cnf
        conjunctive_form=convert2CNF(conjunctive_form, disjunctive_form, grid_size)
 
    if not isInvalidgrid:
        print "No output file created since the grid is invalid"
        return
    print "conjunctive_form", conjunctive_form
    fout = open(output, 'w')                        #open output.txt
    fout.write("c This is CNF file" + "\n")         # First line is the comment followed by 'c'
    
    # 2nd line to be of the form p cnf NUMBER_OF_VARIABLES NUMBER_OF_CLAUSES
    fout.write("p cnf ")
    fout.write(str(grid_size-1) + " " + str(len(conjunctive_form)) + "\n")
    
    #output every cnf clause in separate line. Keep appending 0 in to end to mark end of line.
    for x in range(0,len(conjunctive_form)):
        for y in range(0,len(conjunctive_form[x])):
             fout.write(str(conjunctive_form[x][y]) + " ")
        fout.write("0 \n")     

    fout.close()


def convert2CNF(conjunctive_form, disjunctive_form, grid_size):
    tmp_conjunctive_form = []
    unique_set = set()

    #The case when no_of_mines is same as mines given around the cell, there will be only one combination. Add the DNF one by one to cnf
    if (len(disjunctive_form)== 1):
        for i in range(0,len(disjunctive_form[0])):
            if [disjunctive_form[0][i]] not in conjunctive_form:
                conjunctive_form.append([disjunctive_form[0][i]])
    else:
        size_disjunctive_form = len(disjunctive_form)

        #find cnf clause of the form Z1 V Z2 ...Z(n-1) Zn
        for i in range(0,size_disjunctive_form):
            unique_set.add(grid_size)
            grid_size = grid_size + 1

        extra = list(set(unique_set))
        conjunctive_form.append(list(set(unique_set)))
        unique_set.clear()

        #find cnf clause of the form by negating Z values and ORing them with variables like (-Z1 V X1), ..., (-Zn V Xn)
        same_but_negative_unique_set = set()
        j = 0
        for a_dnf in disjunctive_form:
            for i in range(0,len(a_dnf)):
                same_but_negative_unique_set.add(-extra[j])
                same_but_negative_unique_set.add(a_dnf[i])
                #print list(set(s1))
                if list(set(same_but_negative_unique_set)) not in conjunctive_form:
                    conjunctive_form.append(list(set(same_but_negative_unique_set)))
                same_but_negative_unique_set.clear()
            j = j + 1
    return conjunctive_form

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    infoParsed = parse_file(sys.argv[1])
    grid = infoParsed[0]
    N = infoParsed[1]
    M = infoParsed[2]

    convert2conjunctive_form(grid, N, M, sys.argv[2])


### References -
### http://www.dwheeler.com/essays/minisat-user-guide.html
### https://en.wikipedia.org/wiki/Conjunctive_normal_form#Conversion_into_CNF
### https://docs.python.org/2/library/sets.html
### https://docs.python.org/2/library/itertools.html
### Discussed with fellow calss mates Aman Raj and Dhanendra Jain
### http://www.dwheeler.com/essays/minisat-user-guide.html
### http://minisat.se/MiniSat.html
### http://www.msoos.org/2013/09/minisat-in-your-browser/