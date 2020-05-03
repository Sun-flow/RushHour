from queue import PriorityQueue
from copy import deepcopy


def testinput():
    #inputBoard(["--B---","--B---","XXB---","--AA--", "------","------"])
    #inputBoard(["---O--","---O--","XX-O--","PQQQ--", "P-----","P-----"])
    #inputBoard(["OOOP--","--AP--","XXAP--","Q-----", "QGGCCD","Q----D"])
    inputBoard(["--OPPP","--O--A","XXO--A","-CC--Q", "-----Q","--RRRQ"])

class Car:
        def __init__(self, start, char, orient, leng):
            self.char = char
            self.orient = orient
            self.start = start
            self.len = leng

        
        def print(self):
            print(
                'Name: ', self.char,
                '\nOrientation: ', self.orient,
                '\nStart: ', self.start,
                '\nLength: ', self.len
            )

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
        self.board = self.tochararray()
        print(
            'board: ', self.board,
            'board[0]: ', self.board[0],
            'board[0][0]: ', self.board[0][0],
            'board[0][2]: ', self.board[0][2]
            
        )

        

    def tochararray(self):
        arr = [['-' for x in range(6)] for y in range(6)]
        #for char in self.chars:
        
        for car in self.cars:
            x = car.start[0]
            y = car.start[1]
            
            for i in range(car.len):
                if car.orient == 0:
                    arr[x+i][y] = car.char
                elif car.orient == 1:
                    arr[x][y+i] = car.char
        return arr

    def printboard(self):
        for row in self.board:
            print(row)
        print('\n')

    def movecarforward(self, carIndex):
        print('beginMove f')
        print(self.board)
        car = self.cars[carIndex]
        x = car.start[0]
        y = car.start[1]
        orient = car.orient
        forwardSpace = []
        if orient == 0:
            forwardSpace = self.board[x + car.len][y]
        elif orient == 1:
            forwardSpace = self.board[x][y + car.len]

        print(
            '(x,y): (', x, ',', y,')',
            '\norient: ', orient,
            '\nforwardSpace: ', forwardSpace,
            '\ncar.start[orient]: ', car.start[orient]
        )

        if car.start[orient] < 5 and forwardSpace == '-':
            print('before move: ', car.start[car.orient])
            car.start[orient] += 1
            print('after move: ', car.start[car.orient])
            self.board = self.tochararray()
            
        #    return [True, self]
        #else:
        #    return False
        
        
    def movecarbackward(self, carIndex):
        print('beginMove b')
        print(self.board)
        car = self.cars[carIndex]
        x = car.start[0]
        y = car.start[1]
        orient = car.orient
        backSpace = []
        if orient == 0:
            backSpace = self.board[x - 1][y]
        elif orient == 1:
            backSpace = self.board[x][y - 1]


        
        print('move b: ')
        if car.start[orient] > 0 and backSpace == '-':
            print('before move: ', car.start[car.orient])
            car.start[orient] += -1
            print('after move: ', car.start[car.orient])
            self.board = self.tochararray()


    
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


def generateChildren(inBoard):
    newBoards = []
    for car in inBoard.cars:
        board = generateChild(inBoard, car, 'F')
        if board != None and board != inBoard:
            newBoards += [board]
        
        
        board = generateChild(inBoard, car, 'B')
        if board != None and board != inBoard:
            newBoards += [board]

    print('original board: ')
    inBoard.printboard()

    print('new boards: ', len(newBoards))
    
    for item in newBoards:
        item.tochararray()
        item.printboard()
    return newBoards

    #TODO: Implement way to save each new board, without having to deepcopy
    #Also, calculate A* dist in here to return as tuple

def generateChild(board, car, dir):
    
    carIndex = board.cars.index(car)

    #TODO: Check to see if there is another car before making moves
    if dir == 'F' and car.start[car.orient] + car.len < 5:
        
        localState = deepcopy(board)
        print('localstate before move: ')
        localState.printboard()
        localState.movecarforward(carIndex)
        localState.cars[carIndex].print()
        print('localstate after move: ')
        localState.printboard()
        return localState
    if dir == 'B' and car.start[car.orient] > 0:
        localState = deepcopy(board)
        print('localstate before move: ')
        localState.printboard()
        localState.movecarbackward(carIndex)
        localState.cars[carIndex].print()
        print('localstate after move: ')
        localState.printboard()
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

    open.put(startBoard)
    cameFrom[startBoard] = None
    dist[startBoard] = findadist(startBoard)

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