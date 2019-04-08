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

up_outcomes = {}
down_outcomes = {}
left_outcomes = {}
right_outcomes = {}


def file_write_do(grid_size):
    with open('output.txt', 'w') as the_file:
        for i in range(0, grid_size, 1):
            for j in range(0, grid_size, 1):
                the_file.write(policy[i][j])
                if j != grid_size - 1:
                    the_file.write(",")
            if i != grid_size - 1:
                the_file.write("\n")

    the_file.close()


def read_file():
    global policy
    global terminals
    global walls
    f1 = open("input4.txt", "r")

    grid_size = int(f1.readline())
    grid = [[-1234 for x in xrange(grid_size)] for y in xrange(grid_size)]
    policy = [['X' for x in xrange(grid_size)] for y in xrange(grid_size)]

    num_walls = int(f1.readline())
    for wall in range(num_walls):
        wall_string = f1.readline()
        walls2 = wall_string.split(",")
        grid[int(walls2[0]) - 1][int(walls2[1]) - 1] = WALL
        policy[int(walls2[0]) - 1][int(walls2[1]) - 1] = 'N'
        walls.add((int(walls2[0]) - 1, int(walls2[1]) - 1))
        print_grid(grid, grid_size)

    num_terminal = int(f1.readline())
    for terminal in range(num_terminal):
        terminal_string = f1.readline()
        terminal_state = terminal_string.split(",")
        grid[int(terminal_state[0]) - 1][int(terminal_state[1]) - 1] = float(terminal_state[2])
        policy[int(terminal_state[0]) - 1][int(terminal_state[1]) - 1] = 'E'
        terminals.add((int(terminal_state[0]) - 1, int(terminal_state[1]) - 1))

    probability = float(f1.readline())
    reward = float(f1.readline())
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == -1234:
                grid[i][j] = float(reward)

    discount = float(f1.readline())

    return grid, grid_size, probability, discount, reward


def print_grid(grid, grid_size):
    if debug == False:
        return
    s = ""
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            s = s + str(grid[i][j]) + "\t"
        s += '\n'
    print s


if debug == True:
    def dprint(line):
        if debug == True:
            print line
else:
    def dprint(line):
        return


def get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if i == 0:
        outcomes[(i, j)] = 1
        dprint("moves for up from " + str(i) + " " + str(j))
        dprint(outcomes)
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j)] = probability
    outcomes[(i - 1, j - 1)] = swing_probability
    outcomes[(i - 1, j + 1)] = swing_probability

    if i - 1 < 0 or grid[i - 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j)]
        outcomes[(i - 1, j)] = 0
    if i - 1 < 0 or j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        outcomes[(i - 1, j - 1)] = 0
    if i - 1 < 0 or j + 1 >= grid_size or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        outcomes[(i - 1, j + 1)] = 0
    dprint("moves for up from " + str(i) + " " + str(j))
    dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if i == grid_size - 1:
        outcomes[(i, j)] = 1
        dprint("moves for down from " + str(i) + " " + str(j))
        dprint(outcomes)
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i + 1, j)] = probability
    outcomes[(i + 1, j - 1)] = swing_probability
    outcomes[(i + 1, j + 1)] = swing_probability

    if i + 1 >= grid_size or grid[i + 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j)]
        outcomes[(i + 1, j)] = 0
    if i + 1 >= grid_size or j - 1 < 0 or grid[i + 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j - 1)]
        outcomes[(i + 1, j - 1)] = 0
    if i + 1 >= grid_size or j + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        outcomes[(i + 1, j + 1)] = 0
    dprint("moves for down from " + str(i) + " " + str(j))
    dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if j == 0:
        outcomes[(i, j)] = 1
        dprint("moves for left from " + str(i) + " " + str(j))
        dprint(outcomes)
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j - 1)] = swing_probability
    outcomes[(i, j - 1)] = probability
    outcomes[(i + 1, j - 1)] = swing_probability

    # Wall in left
    if j - 1 < 0 or grid[i][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i, j - 1)]
        outcomes[(i, j - 1)] = 0

    # Wall in left top
    if i - 1 < 0 or j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        outcomes[(i - 1, j - 1)] = 0

    # Wall in left bottom
    if i + 1 >= grid_size or j - 1 < 0 or grid[i + 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j - 1)]
        outcomes[(i + 1, j - 1)] = 0
    dprint("moves for left from " + str(i) + " " + str(j))
    dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if j == grid_size - 1:
        outcomes[(i, j)] = 1
        dprint("moves for right from " + str(i) + " " + str(j))
        dprint(outcomes)
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i - 1, j + 1)] = swing_probability
    outcomes[(i, j + 1)] = probability
    outcomes[(i + 1, j + 1)] = swing_probability

    if j + 1 >= grid_size or grid[i][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i, j + 1)]
        outcomes[(i, j + 1)] = 0
    if j + 1 >= grid_size or i - 1 < 0 or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        outcomes[(i - 1, j + 1)] = 0
    if j + 1 >= grid_size or i + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        outcomes[(i + 1, j + 1)] = 0
    dprint("moves for right from " + str(i) + " " + str(j))
    dprint(outcomes)
    return outcomes


def get_utility_sum_of_outcomes(grid, grid_size, outcomes):
    utility = 0.0
    dprint(outcomes)
    for outcome in outcomes:
        if outcomes[outcome] > 0:
            utility = utility + float(grid[outcome[0]][outcome[1]]) * outcomes[outcome]
    return utility


def pre_compute_outcomes(grid, grid_size, probability):
    global up_outcomes
    global down_outcomes
    global left_outcomes
    global right_outcomes
    for i in range(grid_size):
        for j in range(grid_size):
            up_outcomes[(i, j)] = get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability,
                                                                                0.5 * (1 - probability))
            down_outcomes[(i, j)] = get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability,
                                                                                    0.5 * (1 - probability))
            left_outcomes[(i, j)] = get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability,
                                                                                    0.5 * (1 - probability))
            right_outcomes[(i, j)] = get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j,
                                                                                      probability,
                                                                                      0.5 * (1 - probability))


def get_utility_of_action(grid, grid_size, i, j, action, probability):
    outcomes = {}
    if action == UP:
        outcomes = up_outcomes[(i, j)]
    if action == DOWN:
        outcomes = down_outcomes[(i, j)]
    if action == LEFT:
        outcomes = left_outcomes[(i, j)]
    if action == RIGHT:
        outcomes = right_outcomes[(i, j)]

    return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


def get_best_action_based_on_utility(grid, grid_size, i, j, probability):
    up_utility = get_utility_of_action(grid, grid_size, i, j, UP, probability)
    down_utility = get_utility_of_action(grid, grid_size, i, j, DOWN, probability)
    left_utility = get_utility_of_action(grid, grid_size, i, j, LEFT, probability)
    right_utility = get_utility_of_action(grid, grid_size, i, j, RIGHT, probability)

    if up_utility >= down_utility and up_utility >= left_utility and up_utility >= right_utility:
        return [up_utility, 'U']
    if down_utility >= up_utility and down_utility >= left_utility and down_utility >= right_utility:
        return [down_utility, 'D']
    if left_utility >= down_utility and left_utility >= up_utility and left_utility >= right_utility:
        return [left_utility, 'L']
    return [right_utility, 'R']


def value_iteration(grid, grid_size, probability, discount_factor, reward):
    changed = True
    # grid_copy = []
    while changed:
        changed = False
        # grid_copy = deepcopy(grid)

        for i in range(grid_size):
            for j in range(grid_size):
                if not (i, j) in walls and not (i, j) in terminals:
                    [utility, action] = get_best_action_based_on_utility(grid, grid_size, i, j, probability)
                    if grid[i][j] !=  reward + utility * discount_factor:
                        grid[i][j] = reward + utility * discount_factor
                        policy[i][j] = action
                        changed = True

    print_grid(grid, grid_size)
    print_grid(policy, grid_size)


def main():
    grid, grid_size, probability, discount, reward = read_file()
    dprint(grid_size)
    print_grid(grid, grid_size)
    dprint(probability)
    dprint(discount)
    dprint("=============")
    pre_compute_outcomes(grid, grid_size, probability)
    value_iteration(grid, grid_size, probability, discount, reward)
    file_write_do(grid_size)


if __name__ == '__main__':
    time1 = time.time()
    main()
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    else:
        print "No time"
