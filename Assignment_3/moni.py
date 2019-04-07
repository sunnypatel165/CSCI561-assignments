# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 13:34:06 2019

@author: User
"""
import copy
import time

action = ['L', 'R', 'U', 'D']
initial_grid = []
updated_grid = []
N = 0
wall_state_num = 0
wall_state_pos = []
terminal_state_num = 0
terminal_state_pos = []
prob = 0
rp = 0
discount_factor = 0
calculate_policy = []


def getInput():
    file = open(r"input4.txt")
    global N
    global wall_state_num
    global wall_state_pos
    global terminal_state_num
    global terminal_state_pos
    global prob
    global discount_factor
    global rp
    global initial_grid
    global updated_grid
    global calculate_policy

    N = int(file.readline())
    initial_grid = [[0 for x in range(N)] for y in range(N)]
    updated_grid = [[0 for x in range(N)] for y in range(N)]
    calculate_policy = [[0 for x in range(N)] for y in range(N)]
    # print("size : ", N)
    wall_state_num = int(file.readline())
    for i in range(wall_state_num):
        line = file.readline()
        line = line[:-1]
        row, col = line.split(",")
        temp = []
        temp.append(int(row) - 1)
        temp.append(int(col) - 1)
        wall_state_pos.append(temp)
    terminal_state_num = int(file.readline())
    for i in range(terminal_state_num):
        line = file.readline()
        line = line[:-1]
        row, col, rew = line.split(",")
        temp = []
        temp.append(int(row) - 1)
        temp.append(int(col) - 1)
        initial_grid[int(row) - 1][int(col) - 1] = float(rew)
        terminal_state_pos.append(temp)
    prob = float(file.readline())
    rp = float(file.readline())
    discount_factor = float(file.readline())

    for i in range(N):
        for j in range(N):
            if [i, j] not in terminal_state_pos:
                initial_grid[i][j] = rp

    for i in range(wall_state_num):
        initial_grid[wall_state_pos[i][0]][wall_state_pos[i][1]] = float("-inf")

    updated_grid = copy.deepcopy(initial_grid)

    converge()


def converge():
    previous_iter_grid = copy.deepcopy(updated_grid)
    while True:
        calculateUtility()
        if updated_grid == previous_iter_grid:
            #            print("policy for this grid :", calculate_policy)
            write_output()
            break
        else:
            previous_iter_grid = copy.deepcopy(updated_grid)


def write_output():
    with open('output.txt', 'w') as the_file:
        for i in range(N):
            for j in range(N):
                the_file.write(calculate_policy[i][j])
                if j != N - 1:
                    the_file.write(",")
            if i != N - 1:
                the_file.write("\n")

    the_file.close()


def calculateUtility():
    global updated_grid
    global calculate_policy
    #    updated_grid=copy.deepcopy(grid)
    for row in range(len(updated_grid)):
        for col in range(len(updated_grid[0])):
            reward_for_each_state = []
            if [row, col] not in terminal_state_pos and [row, col] not in wall_state_pos:
                for a in action:
                    if a == 'L':
                        reward_for_each_state.append(actionLeft(row, col))
                    elif a == 'R':
                        reward_for_each_state.append(actionRight(row, col))
                    elif a == 'U':
                        reward_for_each_state.append(actionUp(row, col))
                    else:
                        reward_for_each_state.append(actionDown(row, col))
                maxReward = reward_for_each_state[0]
                ac = 0
                for i in range(1, 4):
                    if reward_for_each_state[i] > maxReward:
                        maxReward = reward_for_each_state[i]
                        ac = i
                updated_grid[row][col] = initial_grid[row][col] + discount_factor * maxReward
                calculate_policy[row][col] = action[ac]

    for coord in wall_state_pos:
        calculate_policy[coord[0]][coord[1]] = 'N'

    for coord in terminal_state_pos:
        calculate_policy[coord[0]][coord[1]] = 'E'


def checkInBounds(row, col):
    if row < 0 or row >= N or col < 0 or col >= N:
        return False
    return True


def checkNotWall(row, col):
    if updated_grid[row][col] == float("-inf"):
        return False
    return True


def actionLeft(row, col):
    possible_state = []
    tempLoc = []
    if checkInBounds(row, col - 1) and checkNotWall(row, col - 1):
        tempLoc.append(row)
        tempLoc.append(col - 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row - 1, col - 1) and checkNotWall(row - 1, col - 1):
        tempLoc.append(row - 1)
        tempLoc.append(col - 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row + 1, col - 1) and checkNotWall(row + 1, col - 1):
        tempLoc.append(row + 1)
        tempLoc.append(col - 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    return calculateReward(possible_state)


def actionRight(row, col):
    possible_state = []
    tempLoc = []
    if checkInBounds(row, col + 1) and checkNotWall(row, col + 1):
        tempLoc.append(row)
        tempLoc.append(col + 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row - 1, col + 1) and checkNotWall(row - 1, col + 1):
        tempLoc.append(row - 1)
        tempLoc.append(col + 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row + 1, col + 1) and checkNotWall(row + 1, col + 1):
        tempLoc.append(row + 1)
        tempLoc.append(col + 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    return calculateReward(possible_state)


def actionUp(row, col):
    possible_state = []
    tempLoc = []
    if checkInBounds(row - 1, col) and checkNotWall(row - 1, col):
        tempLoc.append(row - 1)
        tempLoc.append(col)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row - 1, col - 1) and checkNotWall(row - 1, col - 1):
        tempLoc.append(row - 1)
        tempLoc.append(col - 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row - 1, col + 1) and checkNotWall(row - 1, col + 1):
        tempLoc.append(row - 1)
        tempLoc.append(col + 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    return calculateReward(possible_state)


def actionDown(row, col):
    possible_state = []
    tempLoc = []
    if checkInBounds(row + 1, col) and checkNotWall(row + 1, col):
        tempLoc.append(row + 1)
        tempLoc.append(col)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row + 1, col - 1) and checkNotWall(row + 1, col - 1):
        tempLoc.append(row + 1)
        tempLoc.append(col - 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    tempLoc = []
    if checkInBounds(row + 1, col + 1) and checkNotWall(row + 1, col + 1):
        tempLoc.append(row + 1)
        tempLoc.append(col + 1)
        possible_state.append(tempLoc)
    else:
        tempLoc.append(row)
        tempLoc.append(col)
        possible_state.append(tempLoc)

    return calculateReward(possible_state)


def calculateReward(possible_state):
    reward = 0
    for i in range(len(possible_state)):
        if i == 0:
            reward += updated_grid[possible_state[i][0]][possible_state[i][1]] * prob
        else:
            reward += updated_grid[possible_state[i][0]][possible_state[i][1]] * ((1 - prob) / 2)
    return reward


if __name__ == '__main__':
    start_time = time.time()
    getInput()
    final_time = time.time()
    # print("time_taken : ", final_time - start_time)
