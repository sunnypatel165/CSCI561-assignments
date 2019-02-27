from enum import Enum

# power of laser
power = 3

# player types - helps to distinguish between the two player types
MAX_PLAYER = True           # My Code - Red Player
MIN_PLAYER = False          # AI Engine - Blue Player

# winning states
MAX_PLAYER_WIN = 1
MIN_PLAYER_WIN = -1

# Reading Input File
f_in = open("./input5.txt", "r")

# Fetching the board size
n = int(f_in.readline().strip())

# laser grid
laser_grid = [[0 for row in xrange(n)] for col in xrange(n)]


# This enum class helps visualize and understand the different cell types
class CellState(Enum):
    empty = 0           # The cell in the grid is empty
    bLaser = 1          # The cell in the grid has a BLUE laser
    rLaser = 2          # The cell in the grid has a RED laser
    block = 3           # The cell in the grid is blocked, i.e., no laser light can pass through
    bArea = 4           # The cell in the grid is lit by the blue laser
    rArea = 5           # The cell in the grid is lit by the red laser
    bothArea = 6        # The cell in the grid is lit by both the lasers

    # Basic method to get the enum name and value
    def describe(self):
        return self.name, self.value

    # This method updates the color in the cell,i.e., sets the color to blue or red depending on whether the
    # cell is in the power radius of the respective laser.
    # Or color violet if the cell is in range of both lasers
    # laser_state - denotes if its a red or a blue laser
    def update_color(self, laser_state):
        # if cell is empty, it gets the color of the laser
        if self.value == 0:
            return CellState(laser_state.value + 3)

        # if the cell has a laser on it or is a block, the cell state wont change
        elif self.value < 4:
            return self

        # if the cell has already the same color as the laser, no need to update
        elif self.value - laser_state.value == 3:
            return self

        # if the cell already has a color, but is different from the laser color
        else:
            return CellState(6)

    # This method removes the color on a cell if a laser is removed from the grid
    # laser_state - denotes if its a red or a blue laser
    def uncolor(self, laser_state):
        # if cell is empty, no point removing any color from it
        if self.value == 0:
            return self

        # if cell hold a red/blue laser, it will set to empty
        elif self.value < 3:
            return CellState(0)

        # if cell is a block, then its not updated
        elif self.value == 3:
            return self

        # if cell has the same color as the laser, we set it empty
        elif self.value - laser_state.value == 3:
            return CellState(0)

        # if cell has a color, but it is different from the laser removed, it means the cell under consideration
        # originally has both laser colors(violet)
        else:
            # if laser being removed is blue, then cell is updated to red
            if laser_state.value == 1:
                return CellState(5)

            # if laser being removed is red, then cell is updated to blue
            else:
                return CellState(4)

    # Overriding the default toString method to make the grid visually more appealing
    def __str__(self):
        if self.value == 0:
            return '-'              # Empty cell
        elif self.value == 1:
            return 'B'              # Blue Laser cell
        elif self.value == 2:
            return 'R'              # Red Laser cell
        elif self.value == 3:
            return 'X'              # Blocked cell
        elif self.value == 4:
            return 'b'              # Cell lit by blue laser
        elif self.value == 5:
            return 'r'              # Cell lit by red laser
        elif self.value == 6:
            return 'v'              # Cell lit by both lasers
        else:
            return '*'              # Default value (redundant!)


# read grid layout from the input file
for r in xrange(n):
    row_str = str(f_in.readline().strip())
    c = 0
    for ch in row_str:
        laser_grid[r][c] = CellState(int(ch))
        c += 1


# This method colors the grid initially based on the input and the placement of the lasers and blockages
# It scans through the grid and if it encounters any laser, traverses the grid in all the 8 directions within the
# power/range of the laser, and updates the colors of those cells
# Also it checks if there is any blockage in the path of the laser with its power/range and stop coloring the grid
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


# This method recolors the grid in the scenario when we add a new laser in the existing grid at (r, c)
# This too checks in all directions relative to the new laser position and the range/power of the laser
# Also checks for blockages
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


# This method recolors the grid in the scenario when we remove a new laser from the existing grid at (r, c)
# This too checks in all directions relative to the removed laser position and the range/power of the laser
# Also checks for blockages
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


# This is a utility function to pretty print the grid
def print_grid(grid):
    for r in xrange(len(grid)):
        row_str = ''
        for c in xrange(len(grid[r])):
            row_str += str(grid[r][c]) + " "
        print row_str


# This method calculates the rewards individually for both laser placements at (r, c) without
# physically placing the laser
# This also checks for blockages and takes the range/power of the laser into consideration
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


# This method builds two lists, one for each laser.
# These lists hold the empty cell locations where one could place a red/blue laser
# This method also calculates rewards one would receive if either a blue or red laser was placed at the empty cell
# Then sorts in the descending order based on the reward received
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
    print "rlist " + str(r_list)
    print "blist " + str(b_list)
    return r_list, b_list


# This is the primary recursive method which implements DFS based search space traversal and prunes the search space
# using the alpha beta pruning analogy of the minimax algorithm
def run_minimax(grid, r_points, b_points, player_type):

    #print "*************** Turn : " + str(player) + " | R [ " + str(r_points) + " ] | B [ " + str(b_points) + " ] ******************"
    #print_grid(grid)

    # Fetching the rewards list based on the current grid layout for both the players
    r_reward_list, b_reward_list = gen_reward_list(grid)

    # MAX Player turn
    if player_type:

        # Check if there are any empty spaces left for th player to keep its laser
        if len(r_reward_list) == 0:
            return MAX_PLAYER_WIN if (r_points - b_points > 0) else MIN_PLAYER_WIN
        else:
            # local maximizing variable
            local_max = -2

            # Looping over all possible empty spaces where the MAX player can place his RED laser
            for e_space in r_reward_list:

                # get the coordinates and reward the player would receive
                laser_row = e_space[0]
                laser_col = e_space[1]
                laser_reward = e_space[2]

                # place the laser on the grid
                grid[laser_row][laser_col] = CellState.rLaser

                # create a temp copy of grid to manipulate in the recursive depths
                temp_grid = [row[:] for row in grid]

                # re color the grid
                recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

                # recursively call minimax again for the other player
                returned_val = run_minimax(temp_grid, r_points + laser_reward, b_points, MIN_PLAYER)

                # remove the placed laser, as part of backtracking
                grid[laser_row][laser_col] = CellState.empty

                # capture the best values and update local maximizing variables
                if local_max < returned_val:
                    local_max = returned_val

                # Return max player victory if any iteration of the subtree returns a win for the max player
                if local_max > 0:
                    return MAX_PLAYER_WIN

            return MAX_PLAYER_WIN if (local_max > 0) else MIN_PLAYER_WIN

    # MIN Player turn
    else:

        # Check if there are any empty spaces left for th player to keep its laser
        if len(b_reward_list) == 0:
            return MAX_PLAYER_WIN if (r_points - b_points > 0) else MIN_PLAYER_WIN
        else:
            # local minimizing variable
            local_min = 2

            # Looping over all possible empty spaces where the MIN player can place his BLUE laser
            for e_space in b_reward_list:

                # get the coordinates and reward the player would receive
                laser_row = e_space[0]
                laser_col = e_space[1]
                laser_reward = e_space[2]

                # place the laser on the grid
                grid[laser_row][laser_col] = CellState.bLaser

                # create a temp copy of grid to manipulate in the recursive depths
                temp_grid = [row[:] for row in grid]

                # re color the grid
                recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

                # recursively call minimax again for the other player
                returned_val = run_minimax(temp_grid, r_points, b_points + laser_reward, MAX_PLAYER)

                # remove the placed laser, as part of backtracking
                grid[laser_row][laser_col] = CellState.empty

                # capture the best values and update local minimizing variables
                if local_min > returned_val:
                    local_min = returned_val

                # Return min player victory if any iteration of the subtree returns a win for the min player
                if local_min < 0:
                    return MIN_PLAYER_WIN

            return MIN_PLAYER_WIN if (local_min < 0) else MAX_PLAYER_WIN


# This method is where the game play begins
# We manually call the minimax function for every possible position for the MAX player to place his red laser
# And then find the case when the max player wins and terminate
def start_game(grid):

    # Initializing the best move the MAX player would make
    best_x_move = -1
    best_y_move = -1

    # Fetching the rewards list based on the current grid layout for both the players
    r_reward_list, b_reward_list = gen_reward_list(grid)

    # Initializing the points the players have on the initial grid layout
    r_points = 0
    b_points = 0

    # Looping over all possible empty spaces where the MAX player can place his RED laser
    for e_space in r_reward_list:

        # get the coordinates and reward the player would receive
        laser_row = e_space[0]
        laser_col = e_space[1]
        laser_reward = e_space[2]

        # place the laser on the grid
        grid[laser_row][laser_col] = CellState.rLaser

        # create a temp copy of grid to manipulate in the recursive depths
        temp_grid = [row[:] for row in grid]

        # re color the grid based on the newly added laser
        recolor_grid_adding_laser(temp_grid, laser_row, laser_col)

        # recursively call minimax again for the other player
        returned_val = run_minimax(temp_grid, r_points + laser_reward, b_points, MIN_PLAYER)

        # remove the placed laser, as part of backtracking
        grid[laser_row][laser_col] = CellState.empty

        # check if the returned state is where the MAX player is winning or not and
        # capture the laser coordinates of the winning position
        # Once we know MAX player is winning, we stop and return the best coordinates of the laser
        #
        # NOTE : This works under the assumption derived from the question that winning is not
        #        dependent on by what margin does a player dominate the other
        if returned_val == MAX_PLAYER_WIN:
            best_x_move = laser_row
            best_y_move = laser_col
            break

    print("--------------------------------------")
    print(str(best_x_move) + ", " + str(best_y_move))

    # Saving move coordinates to file
    f_out = open("./output.txt", "w")
    f_out.write(str(best_x_move) + " " + str(best_y_move) + "\n")
    f_out.close()


##############################################
# This is where the code starts

# Color the initial grid
color_grid(laser_grid)

# Start the game-play
start_game(laser_grid)