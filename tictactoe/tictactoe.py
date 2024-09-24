"""
Tic Tac Toe Player
"""
import copy
from ctypes import util
import math
from operator import indexOf

from sqlalchemy import false
terminalCount = 0
treesExplored = 0
treesPruned = 0
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    XCount = 0
    OCount = 0
    # Count number of X/O moves in each space
    for rowIdx, row in enumerate(board):
        for columnIdx, column in enumerate(row):
            if (board[rowIdx][columnIdx] == "X"):
                XCount += 1
            elif (board[rowIdx][columnIdx] == "O"):
                OCount += 1 
    # Get total    
    totalMoves = XCount + OCount
    # If total moves are greater than 8 then board is full
    if (totalMoves > 8):
        #print("\n No player selected \n")
        return None
    # If no moves made or both on the same number of moves
    if (totalMoves == 0 or XCount == OCount):
        #print("\n X selected \n")
        return "X"
    # If X has made more moves return O
    if (XCount > OCount):
        #print("\n O selected \n")
        return "O"
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibleMoves = []
    for rowIdx, row in enumerate(board):
        for columnIdx, column in enumerate(row):
            #print("Checking: ", rowIdx , ", ", columnIdx, " = ", board[rowIdx][columnIdx])
            if (board[rowIdx][columnIdx] == EMPTY):
                #print("Added move")
                possibleMoves.append((rowIdx, columnIdx))
    #print("possible moves;", possibleMoves)    
    return possibleMoves

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    boardCopy = board.copy()
    row = action[0]
    column = action[1]
    #print("RESULT BOARD Before move: ", board)
    #print("Move valid? ", row, " - ", column, " = ", action, ", value on board: ", boardCopy[row][column])
    if (boardCopy[row][column] == EMPTY):
        boardCopy[row][column] = player(boardCopy)
        return boardCopy
    else:
        raise NameError(action, " is an Invalid Move")


    raise NotImplementedError

def counterCheck(value):
    if(value == "X"):
        return 1
    if(value == "O"):
        return -1
    return 0
def checkWinner(value):
    if (value == -3):
        return "O"
    if (value == 3):
        return "X"
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for rowIdx, row in enumerate(board):
        counter = 0 
        # X is +1, 0 is -1, -3 or 3 means all three values are the same 
        # check rows
        for columnIdx, column in enumerate(row):
            cell = board[rowIdx][columnIdx]
            if (cell == EMPTY):
                break
            counter += counterCheck(cell)
        # CheckWinnder will return none if no winner
        if(checkWinner(counter) != None):
            return checkWinner(counter)
    for column in range(0, 3):
        counter = 0
        for row in range(0,3):
            cell = board[row][column]
            if (cell == EMPTY):
                break
            counter += counterCheck(cell)
        if(checkWinner(counter) != None):
            return checkWinner(counter)
    counter = 0
    for x in range(0, 3):
        cell = board[x][x]
        if ( cell == EMPTY):
            break
        counter += counterCheck(cell)
    if(checkWinner(counter) != None):
        return checkWinner(counter)
    counter = 0
    for x in range(0, 3):
        cell = board[x][2-x]
        if ( cell == EMPTY):
            break
        counter += counterCheck(cell)
    if(checkWinner(counter) != None):
        return checkWinner(counter)
    
    return None
    raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If no moves left then game over
    if (len(actions(board)) ==0):
        return True
    # If a winner then game over
    if (winner(board) != None):
        return True
    # Otherwise game continues
    return False

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    outcome = winner(board)
    if (outcome == None):
        return 0
    if (outcome == "X"):
        return 1
    if (outcome == "O"):
        return -1
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global terminalCount
    global treesExplored
    global treesPruned
    terminalCount = 0
    treesExplored = 0
    treesPruned = 0
    # Copy board
    master = copy.deepcopy(board)
    frontier = []
    # Get every possible move
    moves = actions(copy.deepcopy(master))
    # If first move, remove duplicates of corners and sides
    if (len(moves) == 9):
        moves = [copy.deepcopy(moves[0]), copy.deepcopy(moves[1]), copy.deepcopy(moves[4])]
    # Add the result of each move (board) to the frontier 
    for move in moves:
        b = result(copy.deepcopy(master), copy.deepcopy(move))
        frontier.append(b)
    # For each move represented by a board in the frontier
    # find the optimal score for the opposing player
    for item in frontier:
        if (player(copy.deepcopy(item)) == "X"):
            outcome = maxMove(copy.deepcopy(item)) 
            frontier[frontier.index(item)] = outcome
        else:
            outcome = minMove(copy.deepcopy(item))
            frontier[frontier.index(item)] = outcome
    print(f"Trees Explored: {treesExplored:>6} \nFully Explored: {terminalCount:>6} \nTrees Pruned {treesPruned:>9}")
    # Return the first move gives the best score to the current player
    if (player(copy.deepcopy(master)) == "X"):
        return moves[frontier.index(max(frontier))]
    else:
        return moves[frontier.index(min(frontier))]

#Returns lowest possible score of a move
def minMove(minBoard):
    global terminalCount
    global treesExplored
    global treesPruned
    treesExplored += 1
    # If this board is terminal then return the score
    if (terminal(copy.deepcopy(minBoard)) == True):
        terminalCount += 1
        #print("Min terminal: ", utility(copy.deepcopy(minBoard)))
        return utility(copy.deepcopy(minBoard))
    # Store the score of each move in results
    minResults = []
    # Create a new board representing each move
    minMoves = actions(copy.deepcopy(minBoard))
    # Add this to a frontier
    minFrontier = []
    for minMove in minMoves:
        minFrontier.append(result(copy.deepcopy(minBoard), minMove))
    # Check each move for the optimal reply for the opponent
    for minItem in minFrontier:
        minResults.append(maxMove(copy.deepcopy(minItem)))
        # If the optimal reply from this move for the
        # opponent is -1 then return result as it already has a best case
        if(minResults[-1] == -1):
            if(len(minResults) < len(minFrontier)):
                treesPruned +=1
            return -1
    return min(minResults)

#Returns highest possible score of a move
def maxMove(maxBoard):
    global terminalCount
    global treesExplored
    global treesPruned
    treesExplored += 1
    maxResults = []
    if (terminal(copy.deepcopy(maxBoard)) == True):
        terminalCount += 1
        return utility(copy.deepcopy(maxBoard))
    maxMoves = actions(copy.deepcopy(maxBoard))
    maxFrontier = []
    for maxMove in maxMoves:
        maxFrontier.append(result(copy.deepcopy(maxBoard), maxMove))
    for maxItem in maxFrontier:
        maxResults.append(minMove(copy.deepcopy(maxItem)))
        if(maxResults[-1] == 1):
            if(len(maxResults) < len(maxFrontier)):
                treesPruned +=1
            return 1
    return max(maxResults)