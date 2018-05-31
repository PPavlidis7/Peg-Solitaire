# This program check if the given solution for a given Peg Solitaire problem is correct:
# Game board is read from a given input file and the solution is read from a second given file
# This program is written by Pavlidis Pavlos for a task at the Artificial Intelligence course, April 2018
from __future__ import print_function
import time
import sys

# method = sys.argv[1]
# input_file = sys.argv[2]
# output_file = sys.argv[3]
start_time = time.time()

width = None
height = None
board = {}
movehistory = []


def readfile(gameboard):
    # This function reads the data from the input file and stores them in a dictionary
    # Dictionary board has: key : x,y and value 0, 1 or 2
    # 0 -> invalid position
    # 1 -> position with peg
    # 2 -> position without peg
    # 1 <= x <= width
    # 1 <= y <= height
    # inputs : game_board -> an empty dictionary
    # output : returns a dictionary created by file's data
    file = sys.argv[1]
    with open(file, 'r') as f:
        w, h = map(int, f.readline().split())
        x = 0
        test = []
        for line in f:  # read rest of lines
            test.append([int(x) for x in line.split()])
            y = 0
            for inner_l in test:
                for item in inner_l:
                    gameboard[x, y] = item
                    y += 1
            x += 1
            test.clear()
    return w, h


def read_solution():
    # This function reads the data from the input file and stores them in a list
    # output : returns the number of moves and a list containing those moves
    results_file = sys.argv[2]
    with open(results_file, 'r') as f:
        moves = int(f.readline())
        movehistory = []
        for line in f:  # read rest of lines
            movehistory.append([int(x) for x in line.split()])
    return moves,movehistory


def adjust_coordinates_to_write(solution_board):
    # This function is used to adjust the coordinates for our input file.
    # It adjusts our coordinates reducing them by 1
    # After this function coordinates values are :
    # 0 <= x <= width - 1
    # 0 <= y <= height - 1
    # inputs : solution_board : a list with our moves. Every value represents a coordinate
    for i1 in range(len(solution_board)):
        for i2 in range(len(solution_board[i1])):
            solution_board[i1][i2] -= 1


def verify_solution(game_board, moves, history):
    # This function is used to check if we have been given a correct solution
    # inputs : game_board : the initial game board
    #        : moves = the number of moves that had been made to solve the problem
    #        : history : a list with our moves
    # output : Prints a message to console whether a solution it correct or not
    for item in range(0, moves):
        for inner in history:

            # The peg [inner[0], inner[1]] moved right
            if inner[0] == inner[2] and inner[1] < inner[3]:
                game_board[inner[0], inner[1]+1] = 2

            # The peg [inner[0], inner[1]] moved left
            elif inner[0] == inner[2] and inner[1] > inner[3]:
                game_board[inner[0], inner[1] - 1] = 2

            # The peg [inner[0], inner[1]] moved up
            elif inner[0] > inner[2] and inner[1] == inner[3]:
                game_board[inner[0] - 1, inner[1]] = 2

            # The peg [inner[0], inner[1]] moved down
            elif inner[0] < inner[2] and inner[1] == inner[3]:
                game_board[inner[0] + 1, inner[1]] = 2

            game_board[inner[0], inner[1]] = 2
            game_board[inner[2], inner[3]] = 1

    if checkforsolution(game_board):
        print("The problem has been solved")
    else:
        print("Wrong solution")


def checkforsolution(game_board):
    # This function checks if we have found a solution
    # inputs : game_board : the current game board
    # output : true if we have solve the problem , else return false
    count = 0
    for item in game_board:
        if game_board[item] == 1:
            count += 1
    if count > 1:
        return False
    else:  # The count must be 1. That's means there is only one peg in our board
        return True


width, height = readfile(board)
moves_counter, movehistory = read_solution()
adjust_coordinates_to_write(movehistory)
verify_solution(board, moves_counter, movehistory)