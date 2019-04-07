import time

rows = 0
columns = 0
discount_factor = 0
p = 0
terminals = set()
wall_cells = set()
reward = 0
WALL = -float('inf')
policy = []


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
            u = 0.5 * (1 - float(p)) * grid[i - 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_up_move_right(grid, i, j):
    if col_in_limit(j) and row_above_limit(i):
        if not wall_right(grid, i - 1, j):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_down_move_right(grid, i, j):
    if col_in_limit(j) and row_in_limit(i):
        if not wall_right(grid, i + 1, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_down_move_left(grid, i, j):
    if col_above_limit(j) and row_in_limit(i):
        if not wall_left(grid, i + 1, j):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_left_move_down(grid, i, j):
    if row_in_limit(i) and col_above_limit(j):
        if not wall_down(grid, i, j - 1):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_right_move_up(grid, i, j):
    if row_above_limit(i) and col_in_limit(j):
        if not wall_up(grid, i, j + 1):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_left_move_up(grid, i, j):
    if row_above_limit(i) and col_above_limit(j):
        if not wall_up(grid, i, j - 1):
            u = 0.5 * (1 - float(p)) * grid[i - 1][j - 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def get_prob_for_right_move_down(grid, i, j):
    if row_in_limit(i) and col_in_limit(j):
        if not wall_down(grid, i, j + 1):
            u = 0.5 * (1 - float(p)) * grid[i + 1][j + 1]
        else:
            u = 0.5 * (1 - float(p)) * grid[i][j]
    else:
        u = 0.5 * (1 - float(p)) * grid[i][j]
    return u


def action_up2(grid, i, j):
    global reward
    global terminals
    if i == 0:
        util = (float(discount_factor) * (float(1) * grid[i][j]))
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
    global reward
    global terminals
    if i == rows - 1:
        util = (float(discount_factor) * (float(1) * grid[i][j]))
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


def action_left2(grid, i, j):
    global reward
    global terminals
    if j == 0:
        util = (float(discount_factor) * (float(1) * grid[i][j]))
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
    global reward
    global terminals
    if j == columns - 1:
        util = (float(discount_factor) * (float(1) * grid[i][j]))
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


def read_file():
    global policy
    global p
    global discount_factor
    global rows
    global columns
    global reward
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

    discount = float(f1.readline())
    p = probability
    discount_factor = discount
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
    changed = True
    while changed:
        changed = False
        for i in range(0, rows, 1):
            for j in range(0, columns, 1):
                max_util = float("-inf")
                if (i, j) in terminals or (i, j) in wall_cells:
                    update_policy_for_terminal(i, j)
                else:
                    reward_up, action_up = action_up2(grid, i, j)
                    max_util = update_max_and_policy(reward_up, action_up, max_util, i, j)
                    reward_down, action_down = action_down2(grid, i, j)
                    max_util = update_max_and_policy(reward_down, action_down, max_util, i, j)
                    reward_left, action_left = action_left2(grid, i, j)
                    max_util = update_max_and_policy(reward_left, action_left, max_util, i, j)
                    reward_right, action_right = action_right2(grid, i, j)
                    max_util = update_max_and_policy(reward_right, action_right, max_util, i, j)
                    if grid[i][j] < max_util + reward:
                        grid[i][j] = max_util + reward
                        changed = True
    file_write_do()


def main():
    grid, grid_size, probability, discount = read_file()
    value_iteration(grid)


if __name__ == '__main__':
    time1 = time.time()
    main()
    time2 = time.time()
    if time2 > 1:
        print time2 - time1
    else:
        print "No time"