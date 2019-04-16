import time
from copy import deepcopy

WALL = -float('inf')
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

debug = False
policy = []
terminals = set()
walls = set()
grid_size = 0
grid = [[]]
policy = [[]]
probability = float(0)
reward = float(0)
discount = float(0)
swing = float(0)
epsilon = float(0)

input_file = "input4.txt"
output_file = "output.txt"


def print_output(grid_size):
    if not debug:
        f2 = open(output_file, "w")
        str2 = ""
        for i in range(grid_size):
            for j in range(grid_size):
                str2 += str(policy[i][j]) + ","
            str2 = str2[:-1]
            str2 = str2 + "\n"
        f2.write(str2)


def read_file():
    global policy
    global terminals
    global walls
    global grid
    global grid_size
    global probability
    global discount
    global reward
    global swing
    global epsilon

    f1 = open(input_file, "r")

    grid_size = int(f1.readline())
    grid = [[-1234 for x in xrange(grid_size)] for y in xrange(grid_size)]
    policy = [['X' for x in xrange(grid_size)] for y in xrange(grid_size)]
    num_walls = int(f1.readline())
    for wall in range(num_walls):
        wall_string = f1.readline()
        walls2 = wall_string.split(",")
        w1 = int(walls2[0])
        w2 = int(walls2[1])
        grid[w1 - 1][w2 - 1] = WALL
        policy[w1 - 1][w2 - 1] = 'N'
        walls.add((w1 - 1, w2 - 1))
        # print_grid(grid, grid_size)

    num_terminal = int(f1.readline())
    for terminal in range(num_terminal):
        terminal_string = f1.readline()
        terminal_state = terminal_string.split(",")
        t1 = int(terminal_state[0])
        t2 = int(terminal_state[1])
        grid[t1 - 1][t2 - 1] = float(terminal_state[2])
        policy[t1 - 1][t2 - 1] = 'E'
        terminals.add((t1 - 1, t2 - 1))

    probability = float(f1.readline())
    reward = float(f1.readline())
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == -1234:
                grid[i][j] = float(reward)

    discount = float(f1.readline())
    swing = float((1.0 - probability) / 2.0)
    # print swing
    epsilon = 0.0001 * (1 - discount) / discount


def get_possible_outcomes_for_up_with_probability2(i, j):
    outcomes = {}
    if i == 0:
        outcomes[(i, j)] = 1
        return float(1) * grid[i][j]

    ut = 0
    utl = 0
    us = 0
    utr = 0
    if grid[i - 1][j] == WALL:
        us = us + probability * grid[i][j]
    else:
        ut = probability * grid[i - 1][j]

    if j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        utl = swing * grid[i - 1][j - 1]
    if j + 1 >= grid_size or grid[i - 1][j + 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        utr = swing * grid[i - 1][j + 1]
    utility = ut + utr + utl + us
    return utility


def get_possible_outcomes_for_down_with_probability(i, j):
    outcomes = {}
    if i == grid_size - 1:
        outcomes[(i, j)] = 1
        return float(1) * grid[i][j]
    ud = 0
    udl = 0
    udr = 0
    us = 0
    if grid[i + 1][j] == WALL:
        us = us + probability * grid[i][j]
    else:
        ud = probability * grid[i + 1][j]

    if j - 1 < 0 or grid[i + 1][j - 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        udl = swing * grid[i + 1][j - 1]

    if j + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        udr = swing * grid[i + 1][j + 1]
    utility = ud + udl + udr + us
    return utility


def get_possible_outcomes_for_left_with_probability(i, j):
    outcomes = {}
    if j == 0:
        outcomes[(i, j)] = 1
        return float(1) * grid[i][j]

    ul = 0
    us = 0
    ulu = 0
    uld = 0
    # Wall in left
    if grid[i][j - 1] == WALL:
        us = us + probability * grid[i][j]
    else:
        ul = probability * grid[i][j - 1]

    # Wall in left top
    if i - 1 < 0 or grid[i - 1][j - 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        ulu = swing * grid[i - 1][j - 1]

    # Wall in left bottom
    if i + 1 >= grid_size or grid[i + 1][j - 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        uld = swing * grid[i + 1][j - 1]

    utility = us + uld + ulu + ul
    return utility


def get_possible_outcomes_for_right_with_probability(i, j):
    outcomes = {}
    if j == grid_size - 1:
        outcomes[(i, j)] = 1
        return float(1) * grid[i][j]
    us = 0
    ur = 0
    udu = 0
    udd = 0
    if grid[i][j + 1] == WALL:
        us = us + probability * grid[i][j]
    else:
        ur = probability * grid[i][j + 1]
    if i - 1 < 0 or grid[i - 1][j + 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        udu = swing * grid[i - 1][j + 1]
    if i + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        us = us + swing * grid[i][j]
    else:
        udd = swing * grid[i + 1][j + 1]
    utility = ur + udd + udu + us
    return utility


non_terminal_states = set()


def pre_compute_non_terminal_states():
    for i in range(grid_size):
        for j in range(grid_size):
            if not (i, j) in walls and not (i, j) in terminals:
                non_terminal_states.add((i, j))


def get_utility_sum_of_outcomes(outcomes):
    utility = 0.0
    for outcome in outcomes:
        utility = utility + float(grid[outcome[0]][outcome[1]]) * outcomes[outcome]
    return utility


def get_utility_of_action_up(i, j):
    return get_possible_outcomes_for_up_with_probability2(i, j)


def get_utility_of_action_down(i, j):
    return get_possible_outcomes_for_down_with_probability(i, j)


def get_utility_of_action_left(i, j):
    return get_possible_outcomes_for_left_with_probability(i, j)


def get_utility_of_action_right(i, j):
    return get_possible_outcomes_for_right_with_probability(i, j)


def get_best_action_based_on_utility(i, j):
    up_utility = get_utility_of_action_up(i, j)
    down_utility = get_utility_of_action_down(i, j)
    left_utility = get_utility_of_action_left(i, j)
    right_utility = get_utility_of_action_right(i, j)
    max_util = max(up_utility, down_utility, left_utility, right_utility)

    if up_utility == max_util:
        return [up_utility, 'U']
    if down_utility == max_util:
        return [down_utility, 'D']
    if left_utility == max_util:
        return [left_utility, 'L']
    return [right_utility, 'R']


count = 0


def value_iteration():
    global count
    global non_terminal_states
    changed = True
    # grid_copy = []
    difference = 0.0006
    # non_terminal_states_list = list(non_terminal_states)

    updated_cells = list(non_terminal_states)
    count = 0
    while len(updated_cells) > 0 and difference > epsilon:
        changed = False
        difference = 0.0
        count = count + 1
        updated_cells_list = list(updated_cells)
        updated_cells = set()
        for (i, j) in updated_cells_list:
            [utility, action] = get_best_action_based_on_utility(i, j)
            new_utility = reward + utility * discount
            policy[i][j] = action
            if grid[i][j] < new_utility:
                difference = max(difference, abs(grid[i][j] - new_utility))
                grid[i][j] = new_utility
                policy[i][j] = action
                changed = True
                for (n1, n2) in neighbors_map[(i, j)]:
                    updated_cells.add((n1, n2))
    print count


neighbors_map = {}


def pre_compute_neighbors():
    for i in range(grid_size):
        for j in range(grid_size):
            neighbors = set()
            neighbors.add((i, j))
            if i - 1 >= 0 and j - 1 >= 0 and not (i - 1, j - 1) in walls and not (i - 1, j - 1) in terminals:
                neighbors.add((i - 1, j - 1))
            if i - 1 >= 0 and j >= 0 and not (i - 1, j) in walls and not (i - 1, j) in terminals:
                neighbors.add((i - 1, j))
            if i - 1 >= 0 and j + 1 < grid_size and not (i - 1, j + 1) in walls and not (i - 1, j + 1) in terminals:
                neighbors.add((i - 1, j + 1))
            if i >= 0 and j - 1 >= 0 and not (i, j - 1) in walls and not (i, j - 1) in terminals:
                neighbors.add((i, j - 1))
            if i >= 0 and j + 1 < grid_size and not (i, j + 1) in walls and not (i, j + 1) in terminals:
                neighbors.add((i, j + 1))
            if i + 1 < grid_size and j - 1 >= 0 and not (i + 1, j - 1) in walls and not (i + 1, j - 1) in terminals:
                neighbors.add((i + 1, j - 1))
            if i + 1 < grid_size and j >= 0 and not (i + 1, j) in walls and not (i + 1, j) in terminals:
                neighbors.add((i + 1, j))
            if i + 1 < grid_size and j + 1 < grid_size and not (i + 1, j + 1) in walls and not (i + 1,
                                                                                                j + 1) in terminals:
                neighbors.add((i + 1, j + 1))
            neighbors_map[(i, j)] = neighbors


def main():
    read_file()
    pre_compute_neighbors()
    pre_compute_non_terminal_states()

    time2 = time.time()
    value_iteration()
    print_output(grid_size)


if __name__ == '__main__':
    time1 = time.time()
    main()
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    else:
        print "No time"
