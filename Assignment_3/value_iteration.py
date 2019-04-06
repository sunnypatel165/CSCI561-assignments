WALL = -float('inf')
debug = True


def read_file():
    f1 = open("input0.txt", "r")

    grid_size = int(f1.readline())
    grid = [[-1234 for x in xrange(grid_size)] for y in xrange(grid_size)]

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


def main():
    grid, grid_size, probability, discount = read_file()
    dprint(grid_size)
    print_grid(grid, grid_size)
    dprint(probability)
    dprint(discount)


if __name__ == '__main__':
    main()
