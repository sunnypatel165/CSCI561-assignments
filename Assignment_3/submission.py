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

# up_outcomes = {}
# down_outcomes = {}
# left_outcomes = {}
# right_outcomes = {}

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
    # else:
    #     # print_grid(policy, grid_size)


def read_file():
    global policy
    global terminals
    global walls
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

    return grid, grid_size, probability, discount, reward


#
# def # print_grid(grid, grid_size):
#     if debug == False:
#         return
#     s = ""
#     for i in xrange(grid_size):
#         for j in xrange(grid_size):
#             s = s + str(grid[i][j]) + "\t"
#         s += '\n'
#     print s
#
#
# if debug == True:
#     def # dprint(line):
#         if debug == True:
#             print line
# else:
#     def # dprint(line):
#         return


def get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if i == 0:
        outcomes[(i, j)] = 1
        # dprint("moves for up from " + str(i) + " " + str(j))
        # dprint(outcomes)
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j)] = probability
    outcomes[(i - 1, j - 1)] = swing_probability
    outcomes[(i - 1, j + 1)] = swing_probability

    if grid[i - 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j)]
        del outcomes[(i - 1, j)]
    if j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        del outcomes[(i - 1, j - 1)]
    if j + 1 >= grid_size or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        del outcomes[(i - 1, j + 1)]
    # dprint("moves for up from " + str(i) + " " + str(j))
    # dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_up_with_probability2(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    utility_current = 0
    utility_top_left = 0
    utility_top_right = 0
    utility_top = 0

    if i == 0:
        outcomes[(i, j)] = 1
        # dprint("moves for up from " + str(i) + " " + str(j))
        # dprint(outcomes)
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j)] = probability
    outcomes[(i - 1, j - 1)] = swing_probability
    outcomes[(i - 1, j + 1)] = swing_probability

    if grid[i - 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j)]
        del outcomes[(i - 1, j)]
    if j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        del outcomes[(i - 1, j - 1)]
    if j + 1 >= grid_size or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        del outcomes[(i - 1, j + 1)]
    # dprint("moves for up from " + str(i) + " " + str(j))
    # dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if i == grid_size - 1:
        outcomes[(i, j)] = 1
        # dprint("moves for down from " + str(i) + " " + str(j))
        # dprint(outcomes)
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i + 1, j)] = probability
    outcomes[(i + 1, j - 1)] = swing_probability
    outcomes[(i + 1, j + 1)] = swing_probability

    if grid[i + 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j)]
        del outcomes[(i + 1, j)]
    if j - 1 < 0 or grid[i + 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j - 1)]
        del outcomes[(i + 1, j - 1)]
    if j + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        del outcomes[(i + 1, j + 1)]
    # dprint("moves for down from " + str(i) + " " + str(j))
    # dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if j == 0:
        outcomes[(i, j)] = 1
        # dprint("moves for left from " + str(i) + " " + str(j))
        # dprint(outcomes)
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j - 1)] = swing_probability
    outcomes[(i, j - 1)] = probability
    outcomes[(i + 1, j - 1)] = swing_probability

    # Wall in left
    if grid[i][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i, j - 1)]
        del outcomes[(i, j - 1)]

    # Wall in left top
    if i - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        del outcomes[(i - 1, j - 1)]

    # Wall in left bottom
    if i + 1 >= grid_size or grid[i + 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j - 1)]
        del outcomes[(i + 1, j - 1)]
    # dprint("moves for left from " + str(i) + " " + str(j))
    # dprint(outcomes)
    return outcomes


def get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j, probability, swing_probability):
    outcomes = {}
    if j == grid_size - 1:
        outcomes[(i, j)] = 1
        # dprint("moves for right from " + str(i) + " " + str(j))
        # dprint(outcomes)
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i - 1, j + 1)] = swing_probability
    outcomes[(i, j + 1)] = probability
    outcomes[(i + 1, j + 1)] = swing_probability

    if grid[i][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i, j + 1)]
        del outcomes[(i, j + 1)]
    if i - 1 < 0 or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        del outcomes[(i - 1, j + 1)]
    if i + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        del outcomes[(i + 1, j + 1)]
    # dprint("moves for right from " + str(i) + " " + str(j))
    # dprint(outcomes)
    return outcomes


# def get_utility_sum_of_outcomes(grid, grid_size, outcomes):
#     utility = 0.0
#     # dprint(outcomes)
#     for outcome in outcomes:
#         utility = utility + float(grid[outcome[0]][outcome[1]]) * outcomes[outcome]
#     return utility


non_terminal_states = set()


def pre_compute_non_terminal_states(grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            if not (i, j) in walls and not (i, j) in terminals:
                non_terminal_states.add((i, j))


# def pre_compute_outcomes(grid, grid_size, probability, swing_probility):
#     global up_outcomes
#     global down_outcomes
#     global left_outcomes
#     global right_outcomes
#     for i in range(grid_size):
#         for j in range(grid_size):
#             up_outcomes[(i, j)] = get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability,
#                                                                                 swing_probility)
#             down_outcomes[(i, j)] = get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability,
#                                                                                     swing_probility)
#             left_outcomes[(i, j)] = get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability,
#                                                                                     swing_probility)
#             right_outcomes[(i, j)] = get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j,
#                                                                                       probability,
#                                                                                       swing_probility)


def get_utility_sum_of_outcomes(grid, grid_size, outcomes):
    utility = 0.0
    # dprint(outcomes)
    for outcome in outcomes:
        utility = utility + float(grid[outcome[0]][outcome[1]]) * outcomes[outcome]
    return utility


def get_utility_of_action_up(grid, grid_size, i, j, action, probability, swing):
    outcomes = get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability, swing)
    return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


def get_utility_of_action_down(grid, grid_size, i, j, action, probability, swing):
    outcomes = get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability, swing)
    return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


def get_utility_of_action_left(grid, grid_size, i, j, action, probability, swing):
    outcomes = get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability, swing)
    return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


def get_utility_of_action_right(grid, grid_size, i, j, action, probability, swing):
    outcomes = get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j, probability, swing)
    return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


# def get_utility_of_action(grid, grid_size, i, j, action, probability):
#     outcomes = {}
#     if action == UP:
#         outcomes = get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j, probability,
#                                                                  0.5 * (1 - probability))
#     if action == DOWN:
#         outcomes = get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j, probability,
#                                                                    0.5 * (1 - probability))
#     if action == LEFT:
#         outcomes = get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j, probability,
#                                                                    0.5 * (1 - probability))
#
#     if action == RIGHT:
#         outcomes = get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j, probability,
#                                                                     0.5 * (1 - probability))
#     return get_utility_sum_of_outcomes(grid, grid_size, outcomes)


def get_best_action_based_on_utility(grid, grid_size, i, j, probability, swing):
    up_utility = get_utility_of_action_up(grid, grid_size, i, j, UP, probability, swing)
    down_utility = get_utility_of_action_down(grid, grid_size, i, j, DOWN, probability, swing)
    left_utility = get_utility_of_action_left(grid, grid_size, i, j, LEFT, probability, swing)
    right_utility = get_utility_of_action_right(grid, grid_size, i, j, RIGHT, probability, swing)
    max_util = max(up_utility, down_utility, left_utility, right_utility)
    if up_utility == max_util:
        return [up_utility, 'U']
    if down_utility == max_util:
        return [down_utility, 'D']
    if left_utility == max_util:
        return [left_utility, 'L']
    return [right_utility, 'R']


count = 0


def value_iteration(grid, grid_size, probability, discount_factor, reward):
    global count
    global non_terminal_states
    changed = True
    # grid_copy = []
    difference = 0.0006
    # non_terminal_states_list = list(non_terminal_states)

    updated_cells = list(non_terminal_states)
    swing = 0.5 * (1 - probability)

    while len(updated_cells) > 0 and difference > 0.00006:
        changed = False
        difference = 0.0
        count = count + 1
        # grid_copy = deepcopy(grid)
        updated_cells_list = list(updated_cells)
        # print len(updated_cells_list)
        updated_cells = set()
        for (i, j) in updated_cells_list:
            [utility, action] = get_best_action_based_on_utility(grid, grid_size, i, j, probability, swing)
            new_utility = reward + utility * discount_factor
            policy[i][j] = action
            if grid[i][j] < new_utility:
                # difference = difference + abs(grid[i][j] - new_utility)
                difference = max(difference, abs(grid[i][j] - new_utility))
                grid[i][j] = new_utility
                policy[i][j] = action
                changed = True
                # difference = difference / (grid_size * grid_size)
                # updated_cells = updated_cells | (neighbors_map[(i, j)])
                for (n1, n2) in neighbors_map[(i, j)]:
                    updated_cells.add((n1, n2))
    # print_grid(grid, grid_size)
    # print_grid(policy, grid_size)
    print count


neighbors_map = {}


def pre_compute_neighbors(grid, grid_size):
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
    time1 = time.time()
    grid, grid_size, probability, discount, reward = read_file()
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    # dprint(grid_size)
    # print_grid(grid, grid_size)
    # dprint(probability)
    # dprint(discount)
    # dprint("=============")
    pre_compute_neighbors(grid, grid_size)
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    # dprint(neighbors_map)
    pre_compute_non_terminal_states(grid_size)
    # time1 = time.time()
    # pre_compute_outcomes(grid, grid_size, probability, 0.5 * (1 - probability))
    # time2 = time.time()
    # if time2 > 1:
    #     print time2 - time1

    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    value_iteration(grid, grid_size, probability, discount, reward)
    print_output(grid_size)


if __name__ == '__main__':
    time1 = time.time()
    main()
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    else:
        print "No time"
