from queue import PriorityQueue
from copy import deepcopy


class Car:
        def __init__(self, start, char, orient, leng):
            self.char = char
            self.orient = orient
            self.start = start
            self.len = leng

        def move(self, dir):
            if dir == 'F':
                if self.start[self.orient] < 5:
                    self.start[0] += 1
                    return [True, self]
                else:
                    return False
            elif dir == 'B':
                if self.start[self.orient] > 0:
                    self.start[0] += -1
                    return [True, self]
                else:
                    return False
        
        def sizeup(self):
            self.len += 1

        def __attrs(self):
            return(self.char, self.orient, self.start, self.len)

        def __eq__(self, other):
            return isinstance(other, Car) and self.__attrs() == other.__attrs()
        
        def __hash__(self):
            return hash(self.__attrs())


class Board:
    def __init__(self, inBoard):
        cars = []
        chars = []
        for x in range(6):
            for y in range(6):
                if inBoard[x][y] != 0 and inBoard[x][y] != '-':
                    if not inBoard[x][y] in chars:
                        chars += inBoard[x][y]
                        char = inBoard[x][y]
                        if x < 5 and inBoard[x+1][y] == char:
                            cars += [Car([x,y], char, 0, 1)]
                        elif y < 5 and inBoard[x][y+1] == char:
                            cars += [Car([x,y], char, 1, 1)]
                    else:
                        cars[chars.index(inBoard[x][y])].sizeup()

        self.cars = cars

        

    def tochararray(self):
        arr = [[0 for x in range(6)] for y in range(6)]
        #for char in self.chars:
        
        for car in self.cars:
            x = car.start[0]
            y = car.start[1]
            
            for i in range(car.len):
                if car.orient == 0:
                    arr[x+i][y] = car.char
                elif car.orient == 1:
                    arr[x][y+i] = car.char
        
        for row in arr:
            print(row)
        print('\n\n')
        return arr

    def boardcopy(self):
        return self

    
    def __eq__(self, other):
        return isinstance(other, Board) and self.cars == other.cars
        
    def __hash__(self):
        return hash(self.cars)


                    
        #read in array of trucks
        #read in array of cars
        #read in escape car
        #sort by letter 

    
def inputBoard(inBoard):
    board = Board(inBoard)
    print('Original:')
    board.tochararray()
    print('NewBoards:')
    newBoards = generateChildren(board)
    newBoards[0].tochararray()


def generateChildren(inBoard):
    newBoards = []
    for car in inBoard.cars:
        board = generateChild(inBoard, car, 'F')
        if board != None and board != []:
            newBoards += [board]

        board = generateChild(inBoard, car, 'B')
        if board != None and board != []:
            newBoards += [board]

    return newBoards

    #TODO: Implement way to save each new board, without having to deepcopy
    #Also, calculate A* dist in here to return as tuple

def generateChild(board, car, dir):


    #TODO: Check to see if there is another car before making moves
    if dir == 'F' and car.start[car.orient] + car.len < 5:
        localState = board.boardcopy()
        
        #whichCar = localState.cars.index(car)
        localState.cars[0].move(dir)
        return localState
    if dir == 'B' and car.start[car.orient] > 0:
        localState = board.boardcopy()
        #whichCar = localState.cars.index(car)
        localState.cars[0].move(dir)
        return localState
        


def repeatBoard(board, boards):
    return board in boards
    

def rushhour(heuristic, startBoard):
    if heuristic == 0:
        return astar(startBoard)
    elif heuristic == 1:
        return myheur(startBoard)



def astar(startBoard):
    open = PriorityQueue()

    dist = findadist(startBoard)
    open.put((dist, startBoard, []))

    #while not open.empty():
    #    currBoard = open.get()
        #if isGoal(currBoard):
        #    return currBoard
        #else:
        #    children = findChildren(currBoard)
        #    for child in children:
        #        if repeatBoard(child, open):
        #            if child.adist < found.adist:
        #                xx = 1
        #                #replace found
        #        if repeatBoard(child, closed):
        #            if child.adist < found.adist:
        #                #replace found
        #                xx = 1


def findadist(board):
    dist = 0
    for x in board[1]:
        if x != 'X' or x != None:
            dist += 1
    return dist



def myheur(startBoard):
    return []