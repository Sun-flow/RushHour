import Car

class Board:

    #Take in board from character array, generate list of cars.
    def __init__(self, inBoard):
        cars = []
        chars = []
        for x in range(6):
            for y in range(6):

                #Search for characters that are not '-'
                if inBoard[x][y] != 0 and inBoard[x][y] != '-':

                    #If this character is new, check to see which orientation the car is (horizontal or vertical).
                    # If car is not new, find it in the list and increment its length by 1.
                    if not inBoard[x][y] in chars:
                        chars += inBoard[x][y]
                        char = inBoard[x][y]
                        if x < 5 and inBoard[x+1][y] == char:
                            cars += [Car.Car([x,y], char, 0, 1)]
                        elif y < 5 and inBoard[x][y+1] == char:
                            cars += [Car.Car([x,y], char, 1, 1)]
                    else:
                        cars[chars.index(inBoard[x][y])].sizeup()

        self.cars = cars
        self.board = self.tochararray()


    #Translate array of cars into character array, used also to save a copy into the self.board memeber
    def tochararray(self):
        #Create "blank" array
        arr = [['-' for x in range(6)] for y in range(6)]
        
        #For each car in cars, replace the blanks with the appropriate character
        for car in self.cars:
            x = car.start[0]
            y = car.start[1]
            
            for i in range(car.len):
                if car.orient == 0:
                    arr[x+i][y] = car.char
                elif car.orient == 1:
                    arr[x][y+i] = car.char
        return arr


    #Prints character array of board
    def printboard(self):
        for row in self.board:
            print(row)
        print('\n')


    #Moves given car forward one space, if there is room to do so
    def movecarforward(self, carIndex):
        #Prep data with intelligible names
        car = self.cars[carIndex]
        x = car.start[0]
        y = car.start[1]
        orient = car.orient

        #Find the space ahead of the car, save its value
        forwardSpace = []
        if orient == 0:
            forwardSpace = self.board[x + car.len][y]
        elif orient == 1:
            forwardSpace = self.board[x][y + car.len]

        #Check to see if forwardSpace is a valid space for the car to move into. If it is, move the car forward one.
        if car.start[orient] + car.len <= 5 and forwardSpace == '-':
            car.start[orient] += 1
            self.board = self.tochararray()
        

    #Moves given car backward one space, if there is room to do so
    def movecarbackward(self, carIndex):
        #Prep data with intelligible names
        car = self.cars[carIndex]
        x = car.start[0]
        y = car.start[1]
        orient = car.orient

        #Find the space behind of the car, save its value
        backSpace = []
        if orient == 0:
            backSpace = self.board[x - 1][y]
        elif orient == 1:
            backSpace = self.board[x][y - 1]

        #Check to see if backSpace is a valid space for the car to move into. If it is, move the car forward one.
        if car.start[orient] > 0 and backSpace == '-':
            car.start[orient] += -1
            self.board = self.tochararray()


    #Calculate adist to goal for this board
    def adist(self):
        adist = 1
        for y in range(2, 5):
            if self.board[2][y] != '-' and self.board[2][y] != 'X':
                adist += 1

        return adist


    #!ATTN! This is my custom heuristic. Basically an improved blocking heuristic, with heavier weights on trucks in the way in order to force them out.
    def customdist(self):
        customdist = 1

        start = 5
        while self.board[2][start] != 'X':
            start += -1
        start += -1
        
        customdist += 5 - start #similar to A* Distance, but does not check for blocking cars

        #Heavier weight is applied to trucks, which need to end up in the bottom three rows. Rest get weight based on how far they need to move to get out of the way.
        for y in range(start, 6):
            
            #Distance is based on minimum anticipated moves to clear a piece from the main car's way, except for trucks which are weighted heavier in order to prioritize moving them. This saves generations on smaller boards.
            # I've run into issues in some iterations of this method where the solution is 2 moves higher than expected (consistently 2). I believe I've solved this error, but it may show up. If it does, I would love feedback on what's caused it. 
            if self.board[2][y] != '-' and self.board[2][y] != 'X':
                char = self.board[2][y]

                #If is truck, multiply (movement requirement - 1) by 5 and look for blockage below.
                if char == self.board[0][y]:
                    customdist += 10 + self.findbelow(3, y, 5)
                elif char == self.board[1][y]:
                    if char == self.board[3][y]:
                        customdist += 5 + self.findbelow(4, y, 5)
                    elif self.board[0][y] == '-':
                        customdist += 2
                    else: 
                        customdist += 1
                elif char == self.board[4][y]:
                    customdist += 1 + self.findbelow(5, y, 5)
                else:
                    customdist += 1

        return customdist


    #Checks to see if there are cars blocking the path of a car that needs to be moved for a win. Used in customheur().
    def findbelow(self, x, y, limit):
        count = 0
        for i in range (x, limit + 1):
            if self.board[i][y] != '-':
                count += 1
        
        return count    


    #Returns true if the board is a goal, false if not.
    def isgoal(self):
        if self.board[2][5] == "X":
            return True
        else:
            return False

    
    def __eq__(self, other):
        return isinstance(other, Board) and self.cars == other.cars

    
    def __hash__(self):
        return hash(tuple(self.cars))
