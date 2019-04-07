from copy import deepcopy

rows = 0
columns = 0
discount_factor = 0
p = 0
debug = True
terminals = []


def wall_up(grid, i, j):
    if not row_above_limit(i):
        return True
    if grid[i - 1][j] == float("-inf"):
        return True
    return False


def wall_down(grid, i, j):
    if not row_in_limit(i):
        return True
    if grid[i + 1][j] == float("-inf"):
        return True
    return False


def wall_right(grid, i, j):
    if not col_in_limit(j):
        return True
    if grid[i][j + 1] == float("-inf"):
        return True
    return False


def wall_left(grid, i, j):
    if col_above_limit(j):
        return True
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
    print_grid(grid, rows)
    dprint(str(i) + " " + str(j))
    if col_above_limit(j) and row_above_limit(i):
        if not wall_left(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_up_move_right(grid, i, j):
    if col_in_limit(j) and row_above_limit(i):
        if not wall_right(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_down_move_right(grid, i, j):
    if col_in_limit(j) and row_in_limit(i):
        if not wall_right(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_down_move_left(grid, i, j):
    print_grid(grid, rows)
    dprint(str(i) + " " + str(j))
    if col_above_limit(j) and row_in_limit(i):
        if not wall_left(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_left_move_down(grid, i, j):
    if row_in_limit(j) and col_in_limit(j):
        if not wall_down(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_right_move_up(grid, i, j):
    if row_above_limit(j) and col_in_limit(j):
        if not wall_up(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_left_move_up(grid, i, j):
    if row_above_limit(j) and col_in_limit(j):
        if not wall_down(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_right_move_down(grid, i, j):
    if row_in_limit(i) and col_in_limit(j):
        if not wall_up(grid, i, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def action_up2(grid, i, j):
    if i == 0:
        util = (float(discount_factor) * (float(1) * grid[i][j] + 0 + 0))
        return util, "U"

    if row_above_limit(i) and not wall_up(grid, i, j):
        u1 = get_prob_for_up_move_left(grid, i, j)
        u2 = get_prob_for_up_move_right(grid, i, j)
        util = float(discount_factor) * (float(p) * grid[i - 1][j] + u1 + u2)
    else:
        u1 = get_prob_for_up_move_left(grid, i, j)
        u2 = get_prob_for_up_move_right(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j] + u1 + u2))
    return util, "U"


def action_down2(grid, i, j):
    if i == rows - 1:
        util = (float(discount_factor) * (float(1) * grid[i][j] + 0 + 0))
        return util, "D"
    if row_in_limit(i) and not wall_down(grid, i, j):
        u1 = get_prob_for_down_move_left(grid, i, j)
        u2 = get_prob_for_down_move_right(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i + 1][j] + u1 + u2))
    else:
        u1 = get_prob_for_down_move_left(grid, i, j)
        u2 = get_prob_for_down_move_right(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j] + u1 + u2))
    return util, "D"


def compare(g1, g2):
    for i in range(rows):
        for j in range(columns):
            if not g1[i][j] == g2[i][j]:
                return False
    return True


def action_left2(grid, i, j):
    if j == 0:
        util = (float(discount_factor) * (float(1) * grid[i][j] + 0 + 0))
        return util, "L"

    if col_above_limit(j) and not wall_left(grid, i, j):
        u1 = get_prob_for_left_move_up(grid, i, j)
        u2 = get_prob_for_left_move_down(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j - 1] + u1 + u2))
    else:
        u1 = get_prob_for_left_move_up(grid, i, j)
        u2 = get_prob_for_left_move_down(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j] + u1 + u2))
    return util, "L"


def action_right2(grid, i, j):
    if j == columns - 1:
        util = (float(discount_factor) * (float(1) * grid[i][j] + 0 + 0))
        return util, "R"

    if col_in_limit(j) and not wall_right(grid, i, j):
        u1 = get_prob_for_right_move_up(grid, i, j)
        u2 = get_prob_for_right_move_down(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j + 1] + u1 + u2))
    else:
        u1 = get_prob_for_right_move_up(grid, i, j)
        u2 = get_prob_for_right_move_down(grid, i, j)
        util = (float(discount_factor) * (float(p) * grid[i][j] + u1 + u2))
    return util, "R"


WALL = -float('inf')
debug = True
policy = []


def read_file():
    global policy
    global p
    global discount_factor
    global rows
    global columns
    f1 = open("input0.txt", "r")

    grid_size = int(f1.readline())
    grid = [[-1234 for x in xrange(grid_size)] for y in xrange(grid_size)]
    policy = [['x' for x in xrange(grid_size)] for y in xrange(grid_size)]

    num_walls = int(f1.readline())
    for wall in range(num_walls):
        wall_string = f1.readline()
        walls = wall_string.split(",")
        grid[int(walls[0]) - 1][int(walls[1]) - 1] = WALL
        print_grid(grid, grid_size)

    num_terminal = int(f1.readline())
    for terminal in range(num_terminal):
        terminal_string = f1.readline()
        terminal_state = terminal_string.split(",")
        terminals.append([int(terminal_state[0]) - 1, int(terminal_state[1]) - 1])
        grid[int(terminal_state[0]) - 1][int(terminal_state[1]) - 1] = float(terminal_state[2])

    probability = float(f1.readline())
    reward = float(f1.readline())
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == -1234:
                grid[i][j] = float(reward)

    discount = float(f1.readline())
    p = probability
    discount_factor = discount
    rows = columns = grid_size
    return grid, grid_size, probability, discount


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


def value_iteration(grid, grid_size):
    # i =0
    # while i == 50:
        grid_copy = deepcopy(grid)

        for i in range(grid_size):
            for j in range(grid_size):
                dprint("calling actions for " + str(i) + " " + str(j))
                if [i, j] in terminals or grid[i][j] == WALL:
                    continue
                reward_up, action_up = action_up2(grid, i, j)
                reward_down, action_down = action_down2(grid, i, j)
                reward_left, action_left = action_left2(grid, i, j)
                reward_right, action_right = action_right2(grid, i, j)
                dprint(str(reward_up) + " " + str(reward_down) + " " + str(reward_left) + " " + str(reward_right))
                dprint(action_up + " " + action_down + " " + action_left + " " + action_right)

                if reward_up >= reward_down and reward_up >= reward_left and reward_up >= reward_right:
                    max_reward = reward_up
                    policy[i][j] = action_up
                elif reward_down >= reward_up and reward_down >= reward_left and reward_down >= reward_right:
                    max_reward = reward_down
                    policy[i][j] = action_down
                elif reward_left >= reward_down and reward_left >= reward_up and reward_left >= reward_right:
                    max_reward = reward_left
                    policy[i][j] = action_left
                else:
                    max_reward = reward_right
                    policy[i][j] = action_right
                grid[i][j] = max_reward + grid[i][j]

        dprint("grid")
        print_grid(grid, grid_size)
        dprint("grid_copy")
        print_grid(grid_copy, grid_size)
        if compare(grid, grid_copy):
            print "Iterations over"
            print_grid(grid)
            print_grid(policy)
            exit(0)



def main():
    grid, grid_size, probability, discount = read_file()
    dprint(grid_size)
    print_grid(grid, grid_size)
    dprint(probability)
    dprint(discount)

    dprint("================")
    value_iteration(grid, grid_size)


if __name__ == '__main__':
    main()
