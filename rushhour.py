from queue import PriorityQueue
from copy import deepcopy
import Board


def rushhour(heuristic, startBoard):

    #Run search, save data into intelligibly named variables
    output = searchstate(Board.Board(startBoard), heuristic)
    cameFrom = output[0] #Dictionary {someBoard : prevBoard}, used to backtrace path
    lastBoard = output[1] #Goal board
    moves = output[2] #Dictionary {Board : moves to get to board}
    states = output[3] #Counter for number of states explored
    generated = output[4] #Counter for number of states generated


    #Retrace path from goal to start, then reverse the path. This seems costly and clunky to me.
    path = [lastBoard]
    currBoard = lastBoard
    while cameFrom[currBoard] != None:
        path += [cameFrom[currBoard]]
        nextBoard = cameFrom[currBoard]
        currBoard = nextBoard
    flipPath = path[::-1]

    #Print path out, along with other data saved above
    for board in flipPath:
        board.printboard()
    print('\nTotal moves: ', len(flipPath) - 1)
    print('Total states explored: ', states)
    print('# of states generated: ', generated)




def searchstate(startBoard, mode):
    #Prep data for Manipulation
    open = PriorityQueue()
    dist = startBoard.adist()

    #Data in array follows form of (A* distance for someBoard, moves taken to get to this someBoard, someBoard)
    open.put((dist, 0, 0, startBoard))
    cameFrom = {startBoard : None}
    moves = {startBoard : 0}

    explored = 0
    generated = 0

    while not open.empty():
        currNode = open.get()

        #Necessary data for manipulation, saved in intelligible variable
        currMoves = currNode[1] + 1
        currBoard = currNode[3]
        explored += 1

        #Search through all children of currBoard, add any new board states to open and change cameFrom + moves for any repeats with a faster path
        for child in generateChildren(currBoard):

            generated += 1
            
            if child not in cameFrom:
                dist = 0
                if mode == 0:
                    dist = currMoves + currBoard.adist()
                elif mode == 1:
                    dist = currMoves + currBoard.customdist()
                    
                open.put((dist, currMoves, generated, child))
                cameFrom[child] = currBoard
                moves[child] = currMoves
            else:
                if currMoves < moves[child]:
                    moves[child] = currMoves
                    cameFrom[child] = currBoard
            
            if child.isgoal():
                return (cameFrom, child, moves[child], explored, generated)
                

#Generates a move in either direction (if possible) for each car on the board
def generateChildren(inBoard):
    newBoards = []
    for car in inBoard.cars:
        board = generateChild(inBoard, car, 'F')
        if board != None and board != inBoard:
            newBoards += [board]
        
        
        board = generateChild(inBoard, car, 'B')
        if board != None and board != inBoard:
            newBoards += [board]
    
    return newBoards

#Find the car, move it if possible, return the new board
def generateChild(board, car, dir):
    
    carIndex = board.cars.index(car)

    if dir == 'F' and car.start[car.orient] + car.len <= 5:
        localState = deepcopy(board)
        localState.movecarforward(carIndex)
        return localState

    if dir == 'B' and car.start[car.orient] > 0:
        localState = deepcopy(board)
        localState.movecarbackward(carIndex)
        return localState