import collections

# ----------------Variables-------------------
# To enable debug level prints
debug = False

# To represent empty state
EMPTY = 0

# To represent lasers
P1_LASER = 1
P2_LASER = 2

# To represent block
WALL = 3

# To represent regions
P1_AREA = 4
P2_AREA = 5
BOTH_AREA = 6

# To represent players
P1 = 7
AI = 8

# Files
input_file = "input100.txt"
output_file = "output.txt"

# List of available moves sorted based on the value
available_moves_dict = {}


# ----------------Utilities-------------------

# Reads file and returns a grid and the size
def read_file():
    f1 = open(input_file, "r")
    grid_size = int(f1.readline())
    grid = [[-1 for x in xrange(grid_size)] for y in xrange(grid_size)]

    for i in xrange(grid_size):
        line = f1.readline().strip()
        for j in xrange(grid_size):
            grid[i][j] = int(line[j])
    return grid, grid_size


# Method to print the grid
def print_grid(grid, grid_size):
    if not debug:
        return
    s = ""
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            s = s + str(grid[i][j]) + " "
        s += '\n'
    print s


# Returns true if this is a valid position in the grid
def is_valid_position(grid, grid_size, x , y ):
    if x < 0 or x >= grid_size or y < 0 or y >= grid_size:
        return False
    return True


# Debug level print
if debug:
    def dprint(line):
        if debug:
            print line
else:
    def dprint(line):
        return


# ----------------Game functions-------------------


# Marks the regions covered by the lasers
def apply_moves(grid, grid_size):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == P1_LASER or grid[i][j] == P2_LASER:
                mark_player(grid, grid_size, i, j, grid[i][j])


# Checks if there are any empty cells
def check_game_over(grid, grid_size):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == EMPTY:
                return False
    return True


# Returns next player
def get_next_player(player):
    if player == AI:
        return P1
    else:
        return AI


# Marks a given players region
def mark_player(grid, grid_size, x, y, player):
    dprint("Marking player moves: " + str(player))

    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x - i, y, player):
            break

    # Lower 3
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x + i, y, player):
            break

    # Left 3
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x, y - i, player):
            break

    # Right 3
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x, y + i, player):
            break

    # Left Top Diagonal
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x - i, y - i, player):
            break

    # Right Top Diagonal
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x - i, y + i, player):
            break

    # Left Bottom Diagonal
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x + i, y - i, player):
            break

    # Right Bottom Diagonal
    for i in xrange(1, 4):
        if not change_color(grid, grid_size, x + i, y + i, player):
            break


# Changes color of a cell
def change_color(grid, grid_size, x, y, player):
    # Bounds check
    if x < 0 or x >= grid_size or y < 0 or y >= grid_size:
        return True

    # If WALL then break the loop
    if grid[x][y] == WALL:
        return False

    # If already player's laser or player's area then do nothing
    if grid[x][y] == player or grid[x][y] == player + 3:
        return True

    # If already player's laser then do nothing
    elif grid[x][y] == P1_LASER or grid[x][y] == P2_LASER:
        return True

    # If empty then place a laser
    elif grid[x][y] == EMPTY:
        grid[x][y] = player + 3

    # If the other player's area then mark as both area
    elif grid[x][y] == P1_AREA or grid[x][y] == P2_AREA:
        grid[x][y] = BOTH_AREA

    return True


# Marks affected cells by this move as un-live and returns them as a list
def get_affected_cells(grid, grid_size, x, y):

    affected_cells = [(x, y)]
    available_moves_dict[(x, y)] = -1
    # Upper 3
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x - i, y) and grid[x - i][y] == EMPTY:
            affected_cells.append((x - i, y))
            available_moves_dict[(x - i, y)] = -1

    # Lower 3
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x + i, y,) and grid[x + i][y] == EMPTY:
            affected_cells.append((x + i, y))
            available_moves_dict[(x + i, y)] = -1

    # Left 3
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x, y - i ) and grid[x][y - i] == EMPTY:
            affected_cells.append((x, y - i))
            available_moves_dict[(x, y - i)] = -1

    # Right 3
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x, y + i,) and grid[x][y + i] == EMPTY:
            affected_cells.append((x, y + i))
            available_moves_dict[(x, y + i)] = -1

    # Left Top Diagonal
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x - i, y - i ) and grid[x - i][y - i] == EMPTY:
            affected_cells.append((x - i, y - i))
            available_moves_dict[(x - i, y - i)] = -1

    # Right Top Diagonal
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x - i, y + i) and grid[x - i][y + i] == EMPTY:
            affected_cells.append((x - i, y + i))
            available_moves_dict[(x - i, y + i)] = -1

    # Left Bottom Diagonal
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x + i, y - i) and grid[x + i][y - i] == EMPTY:
            affected_cells.append((x + i, y - i))
            available_moves_dict[(x + i, y - i)] = -1

    # Right Bottom Diagonal
    for i in xrange(1, 4):
        if is_valid_position(grid, grid_size, x + i, y + i) and grid[x + i][y + i] == EMPTY:
            affected_cells.append((x + i, y + i))
            available_moves_dict[(x + i, y + i)] = -1

    dprint("affected rows detected: " + str(affected_cells))
    dprint("affected moves: " + str(available_moves_dict))
    return affected_cells


# Calculates both player's scores and returns 2 values
def calculate_score(grid, grid_size):
    p1_score = 0
    p2_score = 0
    for i in xrange(grid_size):
        for j in xrange(grid_size):

            # Player 1 score
            if grid[i][j] == P1_AREA or grid[i][j] == P1_LASER or grid[i][j] == BOTH_AREA:
                p1_score = p1_score + 1

            # Player 2 score
            elif grid[i][j] == P2_AREA or grid[i][j] == P2_LASER or grid[i][j] == BOTH_AREA:
                p2_score = p2_score + 1

    return p1_score, p2_score


# Marks given slots as live
def mark_live(affected_cells):
    for cell in affected_cells:
        available_moves_dict[cell] = 1


# Returns empty slots with live flag
def get_empty_slots_with_live(grid, grid_size, player):
    dprint("getting EMPTY slots on ")
    print_grid(grid, grid_size)
    available_moves = {}
    global available_moves_dict
    # Collect all the moves
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == EMPTY:
                available_moves[(i, j)] = 1
    available_moves_sorted = sorted(available_moves.items(), key=lambda move: check_move_value(grid, grid_size, move[0][0], move[0][1], player), reverse=True)
    available_moves_dict = collections.OrderedDict(available_moves_sorted)
    dprint("sorted moves with live" + str(available_moves_dict))


# Returns a list of all live spots
def get_all_live_slots():
    live_slots = []
    for i in available_moves_dict.keys():
        if available_moves_dict[i] == 1:
            live_slots.append(i)
        return live_slots


# Computes the value of placing a laser here
def check_move_value(grid, grid_size, x, y, player):
    state = [row[:] for row in grid]
    # state = deepcopy(grid)

    # Mark the player
    state[x][y] = player - 6
    mark_player(state, grid_size, x, y, player - 6)

    # Return the difference in scores of 2 players
    p1_score, p2_score = calculate_score(state, grid_size)
    return p1_score - p2_score


# ----------------Minimax functions-------------------

# Max value function which is the maximising player - P1
def max_value(grid, grid_size, player):
    dprint("inside max " + str(player))
    print_grid(grid, grid_size)

    # Get the next player
    next_player = get_next_player(player)

    # Check if the game is over and return the score based on the current board situation
    if check_game_over(grid, grid_size):
        p1_score, p2_score = calculate_score(grid, grid_size)
        if p1_score > p2_score:
            return [10, -1, -1, -1, -1]
        elif p1_score == p2_score:
            return [0, -1, -1, -1, -1]
        else:
            return [-10, -1, -1, -1, -1]

    # Get available positions for the board
    available_moves = get_all_live_slots()

    # Initialise score to -inf
    score = [-10000, -1, -1, -1, -1]

    # For every possible move
    for move in available_moves:

        dprint("move" + str(move))
        # Create a copy of the grid
        # state = deepcopy(grid)
        state = [row[:] for row in grid]

        # Get the cells affected by this move, eventually used to undo the move
        affected_cells = get_affected_cells(grid, grid_size, move[0], move[1])

        # Mark the grid
        state[move[0]][move[1]] = player - 6
        mark_player(state, grid_size, move[0], move[1], player - 6)

        # Print
        dprint("=======")
        dprint("played move " + str(move[0]) + " " + str(move[1]))
        print_grid(state, grid_size)
        dprint("=======")

        # Call min function on this state
        new_score = min_value(state, grid_size, next_player)

        # Undo move by marking the affected cells live
        mark_live(affected_cells)

        dprint("score inside max " + str(new_score) + " " + str(score))

        # Update the score - take a max
        if new_score[0] > score[0]:
            # Update the score
            score[0] = new_score[0]

            # P1's move marked at indices 1 and 2
            score[1] = move[0]
            score[2] = move[1]

            # P2's move copied over
            score[3] = new_score[3]
            score[4] = new_score[4]

        # Prune
        if score[0] > 0:
            return score

    return score


# Min value function which is the minimizing player - AI
def min_value(grid, grid_size, player):
    print_grid(grid, grid_size)
    dprint("inside min " + str(player))

    # Get the next player
    next_player = get_next_player(player)

    # Check if the game is over and return the score based on the current board situation
    if check_game_over(grid, grid_size):
        p1_score, p2_score = calculate_score(grid, grid_size)
        if p1_score > p2_score:
            return [10, -1, -1, -1, -1]
        elif p1_score == p2_score:
            return [0, -1, -1, -1, -1]
        else:
            return [-10, -1, -1, -1, -1]

    # Get available positions for the board
    available_moves = get_all_live_slots()

    # Initialise score to +inf
    score = [10000, -1, -1, -1, -1]

    # For every possible move
    for move in available_moves:

        # Create a copy of the grid
        # state = deepcopy(grid)
        state = [row[:] for row in grid]

        # Get the cells affected by this move, eventually used to undo the move
        affected_cells = get_affected_cells(grid, grid_size, move[0], move[1])

        # Mark the grid
        state[move[0]][move[1]] = player - 6
        mark_player(state, grid_size, move[0], move[1], player - 6)

        dprint("=======")
        dprint("played move " + str(move[0]) + " " + str(move[1]))
        print_grid(state, grid_size)
        dprint("=======")

        # Update the score - take a min
        new_score = max_value(state, grid_size, next_player)

        dprint("score inside min " + str(new_score) + " " + str(score))
        if new_score[0] < score[0]:
            # Update the score
            score[0] = new_score[0]

            # P1's move copied over
            score[1] = new_score[1]
            score[2] = new_score[2]

            # P2's move marked at indices 3 and 4
            score[3] = move[0]
            score[4] = move[1]

        # Undo move by marking the affected cells live
        mark_live(affected_cells)

        # Prune
        if score[0] < 0:
            return score

    return score


def minimax(grid, grid_size, player):
    get_empty_slots_with_live(grid, grid_size, player)
    dprint("live map")
    return max_value(grid, grid_size, P1)


# ----------------Main-------------------
def main():
    # Read the file
    grid, grid_size = read_file()

    # Apply moves and mark regions
    apply_moves(grid, grid_size)

    print_grid(grid, grid_size)
    dprint(calculate_score(grid, grid_size))
    print_grid(grid, grid_size)

    # Call minimax
    score = minimax(grid, grid_size, 7)

    # P1's best move is on indices 1, 2
    x = score[1]
    y = score[2]

    # Write to output file if debug is off
    if not debug:
        f2 = open(output_file, "w")
        str2 = str(x) + " " + str(y) + "\n"
        f2.write(str2)
    else:
        print str(x) + " " + str(y)


# Call main
if __name__ == '__main__':
    main()
