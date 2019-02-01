from enum import Enum
import copy

# power of laser
power = 3

# Reading Input File
f_in = open("./input.txt", "r")

# Fetching the board size
n = int(f_in.readline().strip())

# laser grid
laser_grid = [[0 for row in xrange(n)] for col in xrange(n)]


class CellState(Enum):
    empty = 0
    bLaser = 1
    rLaser = 2
    block = 3
    bArea = 4
    rArea = 5
    bothArea = 6

    def describe(self):
        return self.name, self.value

    def update_color(self, laser_state):
        if self.value == 0:
            return CellState(laser_state.value + 3)
        elif self.value < 4:
            return self
        elif self.value - laser_state.value == 3:
            return self
        else:
            return CellState(6)

    def uncolor(self, laser_state):
        if self.value == 0:
            return self
        elif self.value < 3:
            return CellState(0)
        elif self.value == 3:
            return self
        elif self.value - laser_state.value == 3:
            return CellState(0)
        else:
            if laser_state.value == 1:
                return CellState(5)
            else:
                return CellState(4)


    # Overriding the default toString method
    def __str__(self):
        if self.value == 0:
            return '-'
        elif self.value == 1:
            return 'B'
        elif self.value == 2:
            return 'R'
        elif self.value == 3:
            return 'X'
        elif self.value == 4:
            return 'b'
        elif self.value == 5:
            return 'r'
        elif self.value == 6:
            return 'v'
        else:
            return '*'


# read grid layout
for r in xrange(n):
    row_str = str(f_in.readline().strip())
    c = 0
    for ch in row_str:
        laser_grid[r][c] = CellState(int(ch))
        c += 1


def color_grid(grid):
    for r in xrange(len(grid)):
        for c in xrange(len(grid[r])):
            if grid[r][c] == CellState.bLaser or grid[r][c] == CellState.rLaser:
                for p in xrange(1, power+1, 1):                             # North
                    if r-p < 0:
                        break
                    else:
                        grid[r-p][c] = grid[r-p][c].update_color(grid[r][c])
                        if grid[r-p][c] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # South
                    if r+p > (n-1):
                        break
                    else:
                        grid[r+p][c] = grid[r+p][c].update_color(grid[r][c])
                        if grid[r+p][c] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # East
                    if c+p > (n-1):
                        break
                    else:
                        grid[r][c+p] = grid[r][c+p].update_color(grid[r][c])
                        if grid[r][c+p] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # West
                    if c-p < 0:
                        break
                    else:
                        grid[r][c-p] = grid[r][c-p].update_color(grid[r][c])
                        if grid[r][c-p] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # North-East
                    if c+p > (n-1) or r-p < 0:
                        break
                    else:
                        grid[r-p][c+p] = grid[r-p][c+p].update_color(grid[r][c])
                        if grid[r-p][c+p] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # South-West
                    if r+p > (n-1) or c - p < 0:
                        break
                    else:
                        grid[r+p][c-p] = grid[r+p][c-p].update_color(grid[r][c])
                        if grid[r+p][c-p] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # North-West
                    if r-p < 0 or c-p < 0:
                        break
                    else:
                        grid[r-p][c-p] = grid[r-p][c-p].update_color(grid[r][c])
                        if grid[r-p][c-p] == CellState.block:
                            break

                for p in xrange(1, power+1, 1):                             # South-East
                    if r+p > (n-1) or c+p > (n-1):
                        break
                    else:
                        grid[r+p][c+p] = grid[r+p][c+p].update_color(grid[r][c])
                        if grid[r+p][c+p] == CellState.block:
                            break


def recolor_grid_adding_laser(grid, r, c):
    if grid[r][c] == CellState.bLaser or grid[r][c] == CellState.rLaser:
        for p in xrange(1, power + 1, 1):  # North
            if r - p < 0:
                break
            else:
                grid[r - p][c] = grid[r - p][c].update_color(grid[r][c])
                if grid[r - p][c] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South
            if r + p > (n - 1):
                break
            else:
                grid[r + p][c] = grid[r + p][c].update_color(grid[r][c])
                if grid[r + p][c] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # East
            if c + p > (n - 1):
                break
            else:
                grid[r][c + p] = grid[r][c + p].update_color(grid[r][c])
                if grid[r][c + p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # West
            if c - p < 0:
                break
            else:
                grid[r][c - p] = grid[r][c - p].update_color(grid[r][c])
                if grid[r][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # North-East
            if c + p > (n - 1) or r - p < 0:
                break
            else:
                grid[r - p][c + p] = grid[r - p][c + p].update_color(grid[r][c])
                if grid[r - p][c + p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South-West
            if r + p > (n - 1) or c - p < 0:
                break
            else:
                grid[r + p][c - p] = grid[r + p][c - p].update_color(grid[r][c])
                if grid[r + p][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # North-West
            if r - p < 0 or c - p < 0:
                break
            else:
                grid[r - p][c - p] = grid[r - p][c - p].update_color(grid[r][c])
                if grid[r - p][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South-East
            if r + p > (n - 1) or c + p > (n - 1):
                break
            else:
                grid[r + p][c + p] = grid[r + p][c + p].update_color(grid[r][c])
                if grid[r + p][c + p] == CellState.block:
                    break


def recolor_grid_removing_laser(grid, r, c):
    if grid[r][c] == CellState.bLaser or grid[r][c] == CellState.rLaser:
        for p in xrange(1, power + 1, 1):  # North
            if r - p < 0:
                break
            else:
                grid[r - p][c] = grid[r - p][c].uncolor(grid[r][c])
                if grid[r - p][c] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South
            if r + p > (n - 1):
                break
            else:
                grid[r + p][c] = grid[r + p][c].uncolor(grid[r][c])
                if grid[r + p][c] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # East
            if c + p > (n - 1):
                break
            else:
                grid[r][c + p] = grid[r][c + p].uncolor(grid[r][c])
                if grid[r][c + p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # West
            if c - p < 0:
                break
            else:
                grid[r][c - p] = grid[r][c - p].uncolor(grid[r][c])
                if grid[r][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # North-East
            if c + p > (n - 1) or r - p < 0:
                break
            else:
                grid[r - p][c + p] = grid[r - p][c + p].uncolor(grid[r][c])
                if grid[r - p][c + p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South-West
            if r + p > (n - 1) or c - p < 0:
                break
            else:
                grid[r + p][c - p] = grid[r + p][c - p].uncolor(grid[r][c])
                if grid[r + p][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # North-West
            if r - p < 0 or c - p < 0:
                break
            else:
                grid[r - p][c - p] = grid[r - p][c - p].uncolor(grid[r][c])
                if grid[r - p][c - p] == CellState.block:
                    break

        for p in xrange(1, power + 1, 1):  # South-East
            if r + p > (n - 1) or c + p > (n - 1):
                break
            else:
                grid[r + p][c + p] = grid[r + p][c + p].uncolor(grid[r][c])
                if grid[r + p][c + p] == CellState.block:
                    break


def print_grid(grid):
    for r in xrange(len(grid)):
        row_str = ''
        for c in xrange(len(grid[r])):
            row_str += str(grid[r][c]) + " "
        print row_str


def calc_reward_value(grid, r, c):
    r_reward = 0
    b_reward = 0

    for p in xrange(1, power + 1, 1):  # North
        if r - p < 0:
            break
        else:
            r_reward += 1 if grid[r - p][c] == CellState.empty or grid[r - p][c] == CellState.bArea else 0
            b_reward += 1 if grid[r - p][c] == CellState.empty or grid[r - p][c] == CellState.rArea else 0
            if grid[r - p][c] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # South
        if r + p > (n - 1):
            break
        else:
            r_reward += 1 if grid[r + p][c] == CellState.empty or grid[r + p][c] == CellState.bArea else 0
            b_reward += 1 if grid[r + p][c] == CellState.empty or grid[r + p][c] == CellState.rArea else 0
            if grid[r + p][c] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # East
        if c + p > (n - 1):
            break
        else:
            r_reward += 1 if grid[r][c + p] == CellState.empty or grid[r][c + p] == CellState.bArea else 0
            b_reward += 1 if grid[r][c + p] == CellState.empty or grid[r][c + p] == CellState.rArea else 0
            if grid[r][c + p] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # West
        if c - p < 0:
            break
        else:
            r_reward += 1 if grid[r][c - p] == CellState.empty or grid[r][c - p] == CellState.bArea else 0
            b_reward += 1 if grid[r][c - p] == CellState.empty or grid[r][c - p] == CellState.rArea else 0
            if grid[r][c - p] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # North-East
        if c + p > (n - 1) or r - p < 0:
            break
        else:
            r_reward += 1 if grid[r - p][c + p] == CellState.empty or grid[r - p][c + p] == CellState.bArea else 0
            b_reward += 1 if grid[r - p][c + p] == CellState.empty or grid[r - p][c + p] == CellState.rArea else 0
            if grid[r - p][c + p] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # South-West
        if r + p > (n - 1) or c -p < 0:
            break
        else:
            r_reward += 1 if grid[r + p][c - p] == CellState.empty or grid[r + p][c - p] == CellState.bArea else 0
            b_reward += 1 if grid[r + p][c - p] == CellState.empty or grid[r + p][c - p] == CellState.rArea else 0
            if grid[r + p][c - p] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # North-West
        if r - p < 0 or c - p < 0:
            break
        else:
            r_reward += 1 if grid[r - p][c - p] == CellState.empty or grid[r - p][c - p] == CellState.bArea else 0
            b_reward += 1 if grid[r - p][c - p] == CellState.empty or grid[r - p][c - p] == CellState.rArea else 0
            if grid[r - p][c - p] == CellState.block:
                break

    for p in xrange(1, power + 1, 1):  # South-East
        if r + p > (n - 1) or c + p > (n - 1):
            break
        else:
            r_reward += 1 if grid[r + p][c + p] == CellState.empty or grid[r + p][c + p] == CellState.bArea else 0
            b_reward += 1 if grid[r + p][c + p] == CellState.empty or grid[r + p][c + p] == CellState.rArea else 0
            if grid[r + p][c + p] == CellState.block:
                break

    return r_reward + 1, b_reward + 1


def gen_reward_list(grid):
    r_list = list(())
    b_list = list(())
    for r in xrange(len(grid)):
        for c in xrange(len(grid[r])):
            if grid[r][c] == CellState.empty:
                r_reward, b_reward = calc_reward_value(grid, r, c)
                r_reward_value = list((int(r), int(c), r_reward))
                b_reward_value = list((int(r), int(c), b_reward))
                r_list.append(r_reward_value)
                b_list.append(b_reward_value)

    r_list.sort(key=lambda t: t[2], reverse=True)
    b_list.sort(key=lambda t: t[2], reverse=True)
    return r_list, b_list


def run_minimax(grid, r_points, b_points, player):

    #print "*************** Turn : " + str(player) + " | R [ " + str(r_points) + " ] | B [ " + str(b_points) + " ] ******************"
    #print_grid(grid)

    r_reward_list, b_reward_list = gen_reward_list(grid)

    # MAX Player
    if player == 'r':
        if len(r_reward_list) == 0:    # no available white space
            return 1 if r_points - b_points > 0 else -1
        else:
            # local maximizing variable
            local_max = -float("inf")

            for e_space in r_reward_list:

                # get the coordinates
                laser_row = e_space[0]
                laser_col = e_space[1]
                laser_reward = e_space[2]

                # place the laser on the grid
                grid[laser_row][laser_col] = CellState.rLaser

                # create a temp copy of grid
                temp_grid = copy.deepcopy(grid)

                # re color the grid
                recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

                # adjust the points
                r_points += laser_reward

                # recursively call minimax again
                returned_val = run_minimax(temp_grid, r_points, b_points, 'b')

                # de adjust the points
                r_points -= laser_reward

                # remove the placed laser
                grid[laser_row][laser_col] = CellState.empty

                # capture the best values and update local maximizing variables
                if local_max < returned_val:
                    local_max = returned_val

                if local_max > 0:
                    return 1

            return 1 if local_max > 0 else -1

    # MIN Player
    elif player == 'b':
        if len(b_reward_list) == 0:     # no available white space
            return r_points - b_points
        else:
            # local minimizing variable
            local_min = float("inf")

            for e_space in b_reward_list:

                # get the coordinates
                laser_row = e_space[0]
                laser_col = e_space[1]
                laser_reward = e_space[2]

                # place the laser on the grid
                grid[laser_row][laser_col] = CellState.bLaser

                # create a temp copy of grid
                temp_grid = copy.deepcopy(grid)

                # re color the grid
                recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

                # adjust the points
                b_points += laser_reward

                # recursively call minimax again
                returned_val = run_minimax(temp_grid, r_points, b_points, 'r')

                # de adjust the points
                b_points -= laser_reward

                # remove the placed laser
                grid[laser_row][laser_col] = CellState.empty

                # capture the best values and update local maximizing variables
                if local_min > returned_val:
                    local_min = returned_val

                if local_min < 0:
                    return -1

            return -1 if local_min < 0 else 1

    return 1 if r_points - b_points > 0 else -1


def start_game(grid):

    best_x_move = -1
    best_y_move = -1

    r_reward_list, b_reward_list = gen_reward_list(grid)

    r_points = 0
    b_points = 0

    # local maximizing variable
    local_max = -float("inf")

    for e_space in r_reward_list:
        # get the coordinates
        laser_row = e_space[0]
        laser_col = e_space[1]
        laser_reward = e_space[2]

        # place the laser on the grid
        grid[laser_row][laser_col] = CellState.rLaser

        # create a temp copy of grid
        temp_grid = copy.deepcopy(grid)

        # re color the grid
        recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

        # adjust the points
        r_points += laser_reward

        # recursively call minimax again
        returned_val = run_minimax(temp_grid, r_points, b_points, 'b')

        # de adjust the points
        r_points -= laser_reward

        # remove the placed laser
        grid[laser_row][laser_col] = CellState.empty

        # capture the best values and update local maximizing variables
        if local_max < returned_val:
            local_max = returned_val
            best_x_move = laser_row
            best_y_move = laser_col

        if local_max > 0:
            break


    f2 = open("output.txt", "w")
    str2 = str(best_x_move) + " " + str(best_y_move) + "\n"
    f2.write(str2)


color_grid(laser_grid)
print_grid(laser_grid)

start_game(laser_grid)

