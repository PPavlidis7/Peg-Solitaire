# This program solves the Peg Solitaire problem using two algorithms:
#       - BFS - Best First Search (argument = best)
#       - DFS - Depth First Search (argument = depth)
# Game board is read from an given input file and the solution is written to a given output ile
# This program is written by Pavlidis Pavlos for a task at the Artificial Intelligence course, April 2018

from __future__ import print_function
from collections import defaultdict
import copy
from operator import itemgetter
import sys
import time

start_time = time.time()

width = None
height = None
board = {}
movehistory = []

# Functions


def readfile(gameboard):
    # This function reads the data from the input file and stores them in a dictionary
    # Dictionary board has: key : x,y and value 0, 1 or 2
    # 0 -> invalid position
    # 1 -> position with peg
    # 2 -> position without peg
    # 0 <= x <= width - 1
    # 0 <= y <= height - 1
    # inputs : game_board -> an empty dictionary
    # output : returns a dictionary created by file's data
    file = sys.argv[2]
    with open(file,'r') as f:
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
    else:  # The count must be 1. That's means there is only one peg in our board and we have solve the problem
        return True


def calculate_pegs_area(game_board):
    # This function finds the corners of the orthogonal area which surrounds the pegs
    # inputs : game_board : the current game board
    # output : returns the area
    min_r = -1
    min_c = height + 1
    max_r = 0
    max_c = 0
    # Find first and last rows
    for item in game_board:
        if game_board[item] == 1:
            if min_r == -1:
                min_r = item[0]
            elif max_r < item[0]:
                max_r = item[0]
    # Find first and last columns
    for item in game_board:
        if game_board[item] == 1:
            if min_c > item[1]:
                min_c = item[1]
            if max_c < item[1]:
                max_c = item[1]
    return (max_r - min_r + 1) * (max_c - min_c + 1)


def heuristic(game_board, peg_position, direction):
    # This function calculates the heuristic value for a possible move
    # inputs : game_board : the current game board
    #        : peg_position : The pegs' coordinates that we will move
    #        : direction : The direction which the peg will take
    # output : Returns the orthogonal area multiplied by manhattan distance and multiplied by
    #           the remained number of pegs
    number_of_pegs = 0
    temp_board = make_move(game_board, peg_position, direction)
    man_dis = 0
    for item in temp_board:
        if temp_board[item] == 1:
            number_of_pegs +=1
            for item2 in temp_board:
                if temp_board[item2] == 1:
                    man_dis += abs(item[0] - item2[0]) + abs(item[1] - item2[1])
    area = calculate_pegs_area(temp_board)
    if man_dis == 0:
        man_dis = 1
    return area*number_of_pegs*man_dis


def valid_move(game_board, item, direction):
    # This function check if a peg at position 'item' can move to a specific direction
    # inputs : game_board : the current game board
    #        : item : The pegs' coordinates that we will move
    #        : direction : The direction which the peg will take
    # output : Returns True if we can make that move , else returns False
    if direction == 'left':
        if item[1] >= 2 and game_board[item] == 1 and game_board[item[0], item[1] - 2] == 2 and \
                game_board[item[0], item[1] - 1] == 1:
            return True
    elif direction == 'right':
        if (item[1] != height - 1) and (item[1] + 2 <= (height - 1)) and game_board[item] == 1 \
                and game_board[item[0], item[1] + 2] == 2 and game_board[item[0], item[1] + 1] == 1:
            return True
    elif direction == 'up':
        if item[0] >= 2 and game_board[item] == 1 and game_board[item[0] - 2, item[1]] == 2 and \
                game_board[item[0] - 1, item[1]] == 1:
            return True
    elif direction == 'under':
        if (item[0] != (width - 1)) and (item[0] + 2 <= (width - 1)) and game_board[item] == 1 \
                and game_board[item[0] + 2, item[1]] == 2 and game_board[item[0] + 1, item[1]] == 1:
            return True
    return False


def make_move(game_board, position, direction):
    # This function return the new board after we move the peg at given position and towards a given direction
    # inputs : game_board : the current game board
    #        : position : The pegs' coordinates that we will move
    #        : direction : The direction which the peg will take
    # output : Returns the new game board after peg's movement
    next_board = copy.deepcopy(game_board)

    if (direction == 'left') and valid_move(game_board, position, direction):
        next_board[position] = 2
        next_board[position[0], position[1] - 2] = 1
        next_board[position[0], position[1] - 1] = 2
    elif direction == 'right' and valid_move(game_board, position, direction):
        next_board[position] = 2
        next_board[position[0], position[1] + 2] = 1
        next_board[position[0], position[1] + 1] = 2
    elif direction == 'under' and valid_move(game_board, position, direction):
        next_board[position] = 2
        next_board[position[0] + 2, position[1]] = 1
        next_board[position[0] + 1, position[1]] = 2
    elif direction == 'up' and valid_move(game_board, position, direction):
        next_board[position] = 2
        next_board[position[0] - 2, position[1]] = 1
        next_board[position[0] - 1, position[1]] = 2
    return next_board


def get_possible_moves(game_board):
    # This function detects all possible moves
    # inputs : game_board : the current game board
    # output : Returns a dictionary with all possible moves and their direction
    free_positions = []
    moves = defaultdict(list)
    pegs_position = ('under', 'left', 'up', 'right')
    # Find all free positions
    for item in game_board:
        if game_board[item] == 2:
            free_positions.append(item)

    for free_position in free_positions:
        # Find the neighbors at 'temp' side who can move to this free position
        for temp in pegs_position:
            row = 0
            col = 0
            if temp == 'under':
                row = free_position[0] + 2
                col = free_position[1]
                pegs_move_direction = 'up'
            elif temp == 'right':
                row = free_position[0]
                col = free_position[1] + 2
                pegs_move_direction = 'left'
            elif temp == 'up':
                row = free_position[0] - 2
                col = free_position[1]
                pegs_move_direction = 'under'
            elif temp == 'left':
                row = free_position[0]
                col = free_position[1] - 2
                pegs_move_direction = 'right'
            if row < 0 or col < 0 or row >= width or col >= height:
                continue
            position = row, col
            # If it is a possible move and at 'position' there is a peg put at 'move' dictionary this move
            if valid_move(game_board, position, pegs_move_direction) and (game_board[position] == 1):
                moves[position].append(pegs_move_direction)
    return moves


def find_child(game_board):
    # This Function finds the node's children
    # inputs : game_board : the current game board
    # output : Return node's children
    moves = get_possible_moves(game_board)
    return moves


def adjust_coordinats_to_write(position, direction):
    # This function is used to adjust the coordinates for our output file.
    # It adjusts our coordinates increasing them by 1
    # inputs : position : peg's coordinates
    #        : direction: peg's movement direction
    # output : Returns a string with the peg's adjusted coordinates before and after its movement
    if direction == 'left':
        line = [str(position[0] + 1), " ", str(position[1] + 1), " ", str(position[0] + 1), " ", str(position[1] - 1)]
    elif direction == 'right':
        line = [str(position[0] + 1), " ", str(position[1] + 1), " ", str(position[0] + 1), " ", str(position[1] + 3)]
    elif direction == 'under':
        line = [str(position[0] + 1), " ", str(position[1] + 1), " ", str(position[0] + 3), " ", str(position[1] + 1)]
    elif direction == 'up':
        line = [str(position[0] + 1), " ", str(position[1] + 1), " ", str(position[0] - 1), " ", str(position[1] + 1)]
    return line


def find_solution_BFS(game_board, counter):
    # This function uses BFS algorithm to find the moves that we need to solve our problem.
    # inputs : game_board : the current game board
    #        : counter : the current counter's value. At the beginning of our program it is equal with zero
    # output : Returns the new counter's value . If we reach a dead end path, it will returns the value that
    #           it got when we called this function

    # flag variable contains the initial value of counter
    flag = counter
    # a list with the heuristics values that we are going to estimate
    heuristics_values = []
    # check if a solution has been found and create the output file
    if checkforsolution(game_board):
        results.writelines(str(counter) + '\n')
        for item in movehistory:
            results.writelines(item)
            results.writelines('\n')
        # We found a solution so we return -1 to stop all find_solution_BFS calls
        return -1

    else:
        # Find the current node's children
        moves = find_child(game_board)
        # Estimate their heuristic values
        for inner_1 in moves:
            for inner_2 in moves[inner_1]:
                heuristics_values.append([inner_1, inner_2, heuristic(game_board, inner_1, inner_2)])
        # Sort them by their heuristic value
        heuristics_values.sort(key=itemgetter(2))
        # Take the best child, make this move and call again the find_solution_BFS function do the same
        # activity with its children
        for inner in heuristics_values:
            position = inner.__getitem__(0)
            direction = inner.__getitem__(1)
            child_board = make_move(game_board, position, direction)
            counter += 1
            # The program close if it is running for 5 mins and it have not find a solution
            if (time.time() - start_time) >= 300:
                print('I could not find a solution in 5 minutes')
                print(time.time() - start_time)
                quit()
            line = adjust_coordinats_to_write(position,direction)
            # Put to movehistory list this move
            movehistory.append(line)
            counter = find_solution_BFS(child_board, counter)
            if (counter == -1):
                break;
            # if this line is executed then we have reached a dead end so we delete the last move we have made
            del movehistory[-1]
        # if we reached a dead end return the counter - 1 because we discard this path
        if flag == counter:
            return counter - 1
        return counter


def find_solution_DFS(game_board, counter):
    # This function uses DFS algorithm to find the moves that we need to solve our problem.
    # inputs : game_board : the current game board
    #        : counter : the current counter's value. At the beginning of our program it is equal with zero
    # output : Returns the new counter's value . If we reach a dead end path, it will returns the value that
    #           it got when we called this function

    # flag variable contains the initial value of counter
    flag= counter
    #check if a solution has been found
    if checkforsolution(game_board):
        results.writelines(str(counter) + '\n')
        for item in movehistory:
            results.writelines(item)
            results.writelines('\n')
        # We found a solution so we return -1 to stop all find_solution_BFS calls
        return -1

    else:
        # for each cell of our game board
        for item in game_board:
            if checkforsolution(game_board):
                break
            #Check if peg can move left
            if valid_move(game_board,item,'left'):
                # Make a copy of current game board updated with the new move
                new_board = make_move(game_board, item, 'left')
                counter += 1
                # If we have been unsuccessfully trying over 5 minutes to find a solution terminate the program
                if (time.time() - start_time) >= 300:
                    print('I could not find a solution in 5 minutes')
                    print(time.time() - start_time)
                    quit()
                if new_board not in movehistory:
                    line = adjust_coordinats_to_write(item, 'left')
                    # Put to movehistory list this move
                    movehistory.append(line)
                    # Call again find_solution_BFS function parsing the new game board
                    counter = find_solution_DFS(new_board, counter)
                    if counter == -1:
                        break;
                    # if this line is executed then we have reached a dead end so we delete the last move we have made
                    del movehistory[-1]

            # Check if peg can move right
            if valid_move(game_board, item,'right'):
                # Make a copy of current game board updated with the new move
                new_board = make_move(game_board, item, 'right')
                counter += 1
                # If we have been unsuccessfully trying over 5 minutes to find a solution terminate the program
                if (time.time() - start_time) >= 300:
                    print('I could not find a solution in 5 minutes')
                    print(time.time() - start_time)
                    quit()
                if new_board not in movehistory:
                    line = adjust_coordinats_to_write(item, 'right')
                    # Put to movehistory list this move
                    movehistory.append(line)
                    # Call again find_solution_BFS function parsing the new game board
                    counter = find_solution_DFS(new_board, counter)
                    if counter == -1:
                        break;
                    # if this line is executed then we have reached a dead end so we delete the last move we have made
                    del movehistory[-1]

            #Check if peg can move up
            if valid_move(game_board, item, 'up'):
                # Make a copy of current game board updated with the new move
                new_board = make_move(game_board, item, 'up')
                counter += 1
                if (time.time() - start_time) >= 300:
                    # If we have been unsuccessfully trying over 5 minutes to find a solution terminate the program
                    print('I could not find a solution in 5 minutes')
                    print(time.time() - start_time)
                    quit()
                if new_board not in movehistory:
                    line = adjust_coordinats_to_write(item, 'up')
                    # Put to movehistory list this move
                    movehistory.append(line)
                    # Call again find_solution_BFS function parsing the new game board
                    counter = find_solution_DFS(new_board, counter)
                    if counter == -1:
                        break;
                    # if this line is executed then we have reached a dead end so we delete the last move we have made
                    del movehistory[-1]

            ##Check if peg can move down
            if valid_move(game_board, item, 'under'):
                # Make a copy of current game board updated with the new move
                new_board = make_move(game_board, item, 'under')
                counter += 1
                # If we have been unsuccessfully trying over 5 minutes to find a solution terminate the program
                if (time.time() - start_time) >= 300:
                    print('I could not find a solution in 5 minutes')
                    print(time.time() - start_time)
                    quit()
                if new_board not in movehistory:
                    line = adjust_coordinats_to_write(item, 'under')
                    # Put to movehistory list this move
                    movehistory.append(line)
                    # Call again find_solution_BFS function parsing the new game board
                    counter = find_solution_DFS(new_board, counter)
                    if counter == -1:
                        break;
                    # if this line is executed then we have reached a dead end so we delete the last move we have made
                    del movehistory[-1]
        # if we reached a dead end return the counter - 1 because we discard this path
        if(flag ==counter):
            return (counter-1)
        return counter

# if user asked for DFS algorithm
if sys.argv[1] == 'depth':
    # estimate game board's size
    width, height = readfile(board)

    results = open(sys.argv[3], 'w')
    # Call DFS algorithm
    counter = find_solution_DFS(board, counter=0)

    results.close()

    print("--- It took %s seconds to find a solution ---" % (time.time() - start_time))
# if user asked for DFS algorithm
elif sys.argv[1] == 'best':
    # estimate game board's size
    width, height = readfile(board)

    results = open(sys.argv[3], 'w')
    # Call BFS algorithm
    counter = find_solution_BFS(board, counter=0)
    results.close()
    print("--- It took %s seconds to find a solution ---" % (time.time() - start_time))
# if user input wrong algorithm name
else:
    print('You have put wrong method')