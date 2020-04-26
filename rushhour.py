from queue import PriorityQueue

def class Board:
    def __init__(thisObj, inBoard):
        traverse(inBoard)


    def traverse(inBoard):
        #read in array of trucks
        #read in array of cars
        #read in escape car
        #sort by letter 

    

def rushhour(heuristic, startBoard):
    if heuristic == 0:
        return astar(startBoard)
    elif heuristic == 1:
        return myheur(startBoard)



def astar(startBoard):
    open = PriorityQueue()

    dist = findadist(startBoard)
    open.put((dist, startBoard, []))

    while not open.empty():
        currBoard = open.get()
        if isGoal(currBoard):
            return currBoard
        else:
            children = findChildren(currBoard)
            for child in children:
                if isOpen(child):
                    if child.adist < found.adist:
                        #replace found
                if isClosed(child):
                    if child.adist < found.adist:
                        #replace found


def findadist(board):
    dist = 0
    for x in board[1]:
        if x != 'X' or x != None:
            dist += 1
    return dist



def myheur(startBoard):
    return []