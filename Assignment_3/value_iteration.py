from copy import deepcopy

WALL = -float('inf')
debug = True
policy = []


def read_file():
    global policy
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
        grid[int(terminal_state[0]) - 1][int(terminal_state[1]) - 1] = float(terminal_state[2])

    probability = float(f1.readline())
    reward = float(f1.readline())
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == -1234:
                grid[i][j] = float(reward)

    discount = float(f1.readline())

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


def value_iteration(grid, grid_size, discount_factor):
    while True:
        grid_copy = deepcopy(grid)

        for i in range(grid_size):
            for j in range(grid_size):
                reward_up, action_up = action_up(grid, i, j)
                reward_down, action_down = action_down(grid, i, j)
                reward_left, action_left = action_left(grid, i, j)
                reward_right, action_right = action_right(grid, i, j)
                max_reward = float('-inf')

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

                grid_copy[i][j] = grid[i][j] + max_reward * discount_factor
        print_grid(grid, grid_size)
        print_grid(grid_copy, grid_size)
        if grid == grid_copy:
            print "Iterations over"
            print_grid(grid)
            exit(0)

        grid = deepcopy(grid_copy)


def main():
    grid, grid_size, probability, discount = read_file()
    dprint(grid_size)
    print_grid(grid, grid_size)
    dprint(probability)
    dprint(discount)


if __name__ == '__main__':
    main()
