import time
from copy import deepcopy
rows = 0
columns = 0
discount_factor = 0
p = 0
q = 0
terminals = set()
wall_cells = set()
non_terminals = set()
reward = 0
WALL = -float('inf')
policy = []
UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"
up_outcomes = {}
down_outcomes = {}
left_outcomes = {}
right_outcomes = {}

all_moves = [UP, DOWN, LEFT, RIGHT]


def wall_up(grid, i, j):
    if grid[i - 1][j] == float("-inf"):
        return True
    return False


def wall_down(grid, i, j):
    if grid[i + 1][j] == float("-inf"):
        return True
    return False


def wall_right(grid, i, j):
    if grid[i][j + 1] == float("-inf"):
        return True
    return False


def wall_left(grid, i, j):
    if grid[i][j - 1] == float("-inf"):
        return True
    return False


def row_in_limit(i):
    if i + 1 <= rows - 1:
        return True
    else:
        return False


def row_above_limit(i):
    if i - 1 >= 0:
        return True
    else:
        return False


def col_in_limit(j):
    if j + 1 <= columns - 1:
        return True
    else:
        return False


def col_above_limit(j):
    if j - 1 >= 0:
        return True
    else:
        return False


def get_prob_for_up_move_left(grid, i, j):
    if col_above_limit(j) and row_above_limit(i):
        if not wall_left(grid, i - 1, j):
            u = q * grid[i - 1][j - 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_up_move_right(grid, i, j):
    if col_in_limit(j) and row_above_limit(i):
        if not wall_right(grid, i - 1, j):
            u = q * grid[i - 1][j + 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_down_move_right(grid, i, j):
    if col_in_limit(j) and row_in_limit(i):
        if not wall_right(grid, i + 1, j):
            u = q * grid[i + 1][j + 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_down_move_left(grid, i, j):
    if col_above_limit(j) and row_in_limit(i):
        if not wall_left(grid, i + 1, j):
            u = q * grid[i + 1][j - 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_left_move_down(grid, i, j):
    if row_in_limit(i) and col_above_limit(j):
        if not wall_down(grid, i, j - 1):
            u = q * grid[i + 1][j - 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_right_move_up(grid, i, j):
    if row_above_limit(i) and col_in_limit(j):
        if not wall_up(grid, i, j + 1):
            u = q * grid[i - 1][j + 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_left_move_up(grid, i, j):
    if row_above_limit(i) and col_above_limit(j):
        if not wall_up(grid, i, j - 1):
            u = q * grid[i - 1][j - 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_prob_for_right_move_down(grid, i, j):
    if row_in_limit(i) and col_in_limit(j):
        if not wall_down(grid, i, j + 1):
            u = q * grid[i + 1][j + 1]
        else:
            u = q * grid[i][j]
    else:
        u = q * grid[i][j]
    return u


def get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j):
    outcomes = {}
    if i == 0:
        outcomes[(i, j)] = 1
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j)] = p
    outcomes[(i - 1, j - 1)] = q
    outcomes[(i - 1, j + 1)] = q

    if i - 1 < 0 or grid[i - 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j)]
        outcomes[(i - 1, j)] = 0

    if i - 1 < 0 or j - 1 < 0 or grid[i - 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j - 1)]
        outcomes[(i - 1, j - 1)] = 0
    if i - 1 < 0 or j + 1 >= grid_size or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        outcomes[(i - 1, j + 1)] = 0
    return outcomes


def get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j):
    outcomes = {}
    if i == grid_size - 1:
        outcomes[(i, j)] = 1
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i + 1, j)] = p
    outcomes[(i + 1, j - 1)] = q
    outcomes[(i + 1, j + 1)] = q

    if i + 1 >= grid_size or grid[i + 1][j] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j)]
        outcomes[(i + 1, j)] = 0
    if i + 1 >= grid_size or j - 1 < 0 or grid[i + 1][j - 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j - 1)]
        outcomes[(i + 1, j - 1)] = 0
    if i + 1 >= grid_size or j + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        outcomes[(i + 1, j + 1)] = 0
    return outcomes


def get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j):
    outcomes = {}
    if j == 0:
        outcomes[(i, j)] = 1
        return outcomes
    outcomes[(i, j)] = 0
    outcomes[(i - 1, j - 1)] = q
    outcomes[(i, j - 1)] = p
    outcomes[(i + 1, j - 1)] = q

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
    return outcomes


def get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j):
    outcomes = {}
    if j == grid_size - 1:
        outcomes[(i, j)] = 1
        return outcomes

    outcomes[(i, j)] = 0
    outcomes[(i - 1, j + 1)] = q
    outcomes[(i, j + 1)] = p
    outcomes[(i + 1, j + 1)] = q

    if j + 1 >= grid_size or grid[i][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i, j + 1)]
        outcomes[(i, j + 1)] = 0
    if j + 1 >= grid_size or i - 1 < 0 or grid[i - 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i - 1, j + 1)]
        outcomes[(i - 1, j + 1)] = 0
    if j + 1 >= grid_size or i + 1 >= grid_size or grid[i + 1][j + 1] == WALL:
        outcomes[(i, j)] = outcomes[(i, j)] + outcomes[(i + 1, j + 1)]
        outcomes[(i + 1, j + 1)] = 0
    return outcomes


def get_utility_sum_of_outcomes(grid, outcomes):
    utility = 0.0
    for outcome in outcomes:
        if outcomes[outcome] > 0:
            utility = utility + float(grid[outcome[0]][outcome[1]]) * outcomes[outcome]
    return utility


def pre_compute_outcomes(grid, grid_size):
    global up_outcomes
    global down_outcomes
    global left_outcomes
    global right_outcomes
    global discount_factor
    for i in range(grid_size):
        for j in range(grid_size):
            up_outcomes[(i, j)] = get_possible_outcomes_for_up_with_probability(grid, grid_size, i, j)
            down_outcomes[(i, j)] = get_possible_outcomes_for_down_with_probability(grid, grid_size, i, j)
            left_outcomes[(i, j)] = get_possible_outcomes_for_left_with_probability(grid, grid_size, i, j)
            right_outcomes[(i, j)] = get_possible_outcomes_for_right_with_probability(grid, grid_size, i, j)

    for i in range(grid_size):
        for j in range(grid_size):
            up_outcomes_1 = up_outcomes[(i, j)]
            up_outcomes_2 = down_outcomes[(i, j)]
            up_outcomes_3 = left_outcomes[(i, j)]
            up_outcomes_4 = right_outcomes[(i, j)]
            for outcome in up_outcomes_1:
                up_outcomes_1[outcome] = up_outcomes_1[outcome] * discount_factor
            for outcome in up_outcomes_2:
                up_outcomes_2[outcome] = up_outcomes_2[outcome] * discount_factor
            for outcome in up_outcomes_3:
                up_outcomes_3[outcome] = up_outcomes_3[outcome] * discount_factor
            for outcome in up_outcomes_4:
                up_outcomes_4[outcome] = up_outcomes_4[outcome] * discount_factor


def get_utility_of_action(grid, i, j, action):
    outcomes = {}
    if action == UP:
        outcomes = up_outcomes[(i, j)]
    if action == DOWN:
        outcomes = down_outcomes[(i, j)]
    if action == LEFT:
        outcomes = left_outcomes[(i, j)]
    if action == RIGHT:
        outcomes = right_outcomes[(i, j)]
    return get_utility_sum_of_outcomes(grid, outcomes)


def action_up2(grid, i, j):
    global reward
    global terminals
    if i == 0:
        util = grid[i][j]
        return util, "U"
    if row_above_limit(i) and not wall_up(grid, i, j):
        u1 = get_prob_for_up_move_left(grid, i, j)
        u2 = get_prob_for_up_move_right(grid, i, j)
        util = (p * grid[i - 1][j] + u1 + u2)
    else:
        u1 = get_prob_for_up_move_left(grid, i, j)
        u2 = get_prob_for_up_move_right(grid, i, j)
        util = (p * grid[i][j] + u1 + u2)
    return util, "U"


def action_down2(grid, i, j):
    global reward
    global terminals
    if i == rows - 1:
        util = grid[i][j]
        return util, "D"
    if row_in_limit(i) and not wall_down(grid, i, j):
        u1 = get_prob_for_down_move_left(grid, i, j)
        u2 = get_prob_for_down_move_right(grid, i, j)
        util = (p * grid[i + 1][j] + u1 + u2)
    else:
        u1 = get_prob_for_down_move_left(grid, i, j)
        u2 = get_prob_for_down_move_right(grid, i, j)
        util = (p * grid[i][j] + u1 + u2)
    return util, "D"


def action_left2(grid, i, j):
    global reward
    global terminals
    if j == 0:
        util = grid[i][j]
        return util, "L"
    if col_above_limit(j) and not wall_left(grid, i, j):
        u1 = get_prob_for_left_move_up(grid, i, j)
        u2 = get_prob_for_left_move_down(grid, i, j)
        util = p * grid[i][j - 1] + u1 + u2
    else:
        u1 = get_prob_for_left_move_up(grid, i, j)
        u2 = get_prob_for_left_move_down(grid, i, j)
        util = p * grid[i][j] + u1 + u2
    return util, "L"


def action_right2(grid, i, j):
    global reward
    global terminals
    if j == columns - 1:
        util = grid[i][j]
        return util, "R"
    if col_in_limit(j) and not wall_right(grid, i, j):
        u1 = get_prob_for_right_move_up(grid, i, j)
        u2 = get_prob_for_right_move_down(grid, i, j)
        util = p * grid[i][j + 1] + u1 + u2
    else:
        u1 = get_prob_for_right_move_up(grid, i, j)
        u2 = get_prob_for_right_move_down(grid, i, j)
        util = p * grid[i][j] + u1 + u2
    return util, "R"


def read_file():
    global policy
    global p
    global q
    global discount_factor
    global rows
    global columns
    global reward
    global non_terminals
    f1 = open("input4.txt", "r")

    grid_size = int(f1.readline())
    grid = [[-1234 for x in xrange(grid_size)] for y in xrange(grid_size)]
    policy = [['' for x in xrange(grid_size)] for y in xrange(grid_size)]

    num_walls = int(f1.readline())
    for wall in range(num_walls):
        wall_string = f1.readline()
        walls = wall_string.split(",")
        wall_cells.add((int(walls[0]) - 1, int(walls[1]) - 1))
        grid[int(walls[0]) - 1][int(walls[1]) - 1] = WALL

    num_terminal = int(f1.readline())
    for terminal in range(num_terminal):
        terminal_string = f1.readline()
        terminal_state = terminal_string.split(",")
        terminals.add((int(terminal_state[0]) - 1, int(terminal_state[1]) - 1))
        grid[int(terminal_state[0]) - 1][int(terminal_state[1]) - 1] = float(terminal_state[2])

    probability = float(f1.readline())
    reward = float(f1.readline())
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == -1234:
                grid[i][j] = float(reward)
            if (i, j) in terminals or (i, j) in wall_cells:
                update_policy_for_terminal(i, j)
            else:
                non_terminals.add((i, j))

    discount = float(f1.readline())
    p = float(probability)
    q = (1.0 - float(probability)) * 0.5
    discount_factor = float(discount)
    rows = columns = grid_size
    return grid, grid_size, probability, discount


def print_grid(grid, grid_size):
    s = ""
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            s = s + str(grid[i][j]) + "\t"
        s += '\n'
    print s


def file_write_do():
    with open('output.txt', 'w') as the_file:
        for i in range(0, rows, 1):
            for j in range(0, columns, 1):
                the_file.write(policy[i][j])
                if j != columns - 1:
                    the_file.write(",")
            if i != rows - 1:
                the_file.write("\n")
    the_file.close()


def update_max_and_policy(reward, action, max_util, i, j):
    global policy
    if reward > max_util:
        max_util = reward
        policy[i][j] = action
    return max_util


def update_policy_for_terminal(i, j):
    global policy
    global terminals
    global wall_cells
    if (i, j) in terminals:
        policy[i][j] = "E"
    if (i, j) in wall_cells:
        policy[i][j] = "N"


def value_iteration(grid):

    global reward
    global policy
    global non_terminals
    list_nodes = list(non_terminals)
    hash_map = {}
    time1 = time.time()
    diff = 1

    while diff > 0.00006:
        diff = 0.0
        for (i, j) in list_nodes:
            reward_up, action_up = action_up2(grid, i, j)
            hash_map[reward_up] = action_up
            reward_down, action_down = action_down2(grid, i, j)
            hash_map[reward_down] = action_down
            reward_left, action_left = action_left2(grid, i, j)
            hash_map[reward_left] = action_left
            reward_right, action_right = action_right2(grid, i, j)
            hash_map[reward_right] = action_right
            max_util = max(reward_up, reward_down, reward_left, reward_right)
            policy[i][j] = hash_map[max_util]
            if grid[i][j] - discount_factor * max_util + reward:
                diff = max(diff, abs(grid[i][j] - (discount_factor * max_util + reward)))
                grid[i][j] = discount_factor * max_util + reward
    time2 = time.time()
    print time2 - time1
    file_write_do()


def get_best_action_based_on_utility(grid, i, j):
    hash_map = {}
    up_utility = get_utility_of_action(grid, i, j, UP)
    hash_map[up_utility] = UP
    down_utility = get_utility_of_action(grid, i, j, DOWN)
    hash_map[down_utility] = DOWN
    left_utility = get_utility_of_action(grid, i, j, LEFT)
    hash_map[left_utility] = LEFT
    right_utility = get_utility_of_action(grid, i, j, RIGHT)
    hash_map[right_utility] = RIGHT
    max_util = max(up_utility, down_utility, left_utility, right_utility)
    return [max_util, hash_map[max_util]]


def value_iteration2(grid):
    global reward
    global policy
    global non_terminals
    diff = 1
    list_temp = list(non_terminals)
    while len(list_temp) > 0 and diff > 0.00006:
        diff = 0.0
        list_temp = list(list_temp)
        list_nodes = deepcopy(list_temp)
        list_temp = set()
        for (i, j) in list_nodes:
            [utility, action] = get_best_action_based_on_utility(grid, i, j)
            if grid[i][j] < utility + reward:
                list_temp.add((i, j))
                list_temp = add_neighbour_states(list_temp, i, j)
                diff = max(diff, abs(grid[i][j] - (utility + reward)))
                grid[i][j] = utility + reward
            policy[i][j] = action

    file_write_do()


def in_bounds(i, j):
    if 0 <= i < rows and 0 <= j < columns:
        return True
    else:
        return False


neighbor_map = {}


def add_neighbour_states(list_temp, i, j):
    for (p1, p2) in neighbor_map[(i, j)]:
        list_temp.add((p1, p2))
    return list_temp


def precompute_neighbour_states():
    for i in range(rows):
        for j in range(columns):
            list_temp = set()
            list_temp.add((i,j))
            if in_bounds(i + 1, j) and (i + 1, j) in non_terminals:
                list_temp.add((i + 1, j))
            if in_bounds(i -1, j) and (i -1, j) in non_terminals:
                list_temp.add((i - 1, j))
            if in_bounds(i, j -1) and (i, j - 1) in non_terminals:
                list_temp.add((i , j -1))
            if in_bounds(i, j + 1) and (i, j + 1) in non_terminals:
                list_temp.add((i, j + 1))
            if in_bounds(i + 1, j -1) and (i + 1, j -1) in non_terminals:
                list_temp.add((i + 1, j -1))
            if in_bounds(i + 1, j + 1) and (i + 1, j + 1) in non_terminals:
                list_temp.add((i + 1, j + 1))
            if in_bounds(i - 1, j - 1) and (i - 1, j -1) in non_terminals:
                list_temp.add((i - 1, j -1))
            if in_bounds(i - 1, j + 1) and (i - 1, j + 1) in non_terminals:
                list_temp.add((i - 1, j + 1))
            neighbor_map[(i,j)] = list_temp


def main():
    grid, grid_size, probability, discount = read_file()
    precompute_neighbour_states()
    pre_compute_outcomes(grid, grid_size)
    time1 = time.time()
    # value_iteration(grid)
    value_iteration2(grid)
    time2 = time.time()
    print time2 - time1


if __name__ == '__main__':
    main()