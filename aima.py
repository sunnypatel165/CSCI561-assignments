from enum import Enum
from copy import copy, deepcopy

debug = False
# class State(Enum):
EMPTY = 0
P1_LASER = 1
P2_LASER = 2
WALL = 3
P1_AREA = 4
P2_AREA = 5
BOTH_AREA = 6
P1 = 7
AI = 8


def read_file():
    f1 = open("input.txt", "r")
    grid_size = int(f1.readline())
    grid = [[-1 for x in xrange(grid_size)] for y in xrange(grid_size)]

    for i in xrange(grid_size):
        line = f1.readline().strip()
        for j in xrange(grid_size):
            grid[i][j] = int(line[j])
    # dprint("====read====")
    # dprint("====read done===")
    return grid, grid_size


def print_grid(grid, grid_size):
    if debug==False:
        return
    s = ""
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            s = s + str(grid[i][j]) + " "
        s += '\n'
    print s


def apply_moves(grid, grid_size):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == 1 or grid[i][j] == 2:
                mark_player(grid, grid_size, i, j, grid[i][j])


# Expects the moves to be applied
def check_game_over(grid, grid_size):
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == 0:
                return False
    return True


def mark_player(grid, grid_size, x, y, player):
    # dprint("Marking player" + str(player))
    # Upper 3
    for i in xrange(1, 4):
        if x-i >= 0 and grid[x-i][y] == WALL:
            break
        change_color(grid, grid_size, x-i, y, player)

    # Lower 3
    for i in xrange(1, 4):
        if x+i < grid_size and grid[x+i][y] == WALL:
            break
        change_color(grid, grid_size, x+i, y, player)

    # Left 3
    for i in xrange(1, 4):
        if y - i >= 0 and grid[x][y-i] == WALL:
            break
        change_color(grid, grid_size, x, y-i, player)

    # Right 3
    for i in xrange(1, 4):
        if y+i < grid_size and grid[x][y+i] == WALL:
            break
        change_color(grid, grid_size, x, y+i, player)

    # Left Top Diagonal
    for i in xrange(1, 4):
        if x-i >= 0 and y-i >= 0 and grid[x-i][y-i] == WALL:
            break
        change_color(grid, grid_size, x-i, y-i, player)

    # Right Top Diagonal
    for i in xrange(1,4):
        if x-i >= 0 and y+i < grid_size and grid[x-i][y+i] == WALL:
            break
        change_color(grid, grid_size, x-i, y+i, player)

    # Left Bottom Diagonal
    for i in xrange(1, 4):
        if x + i < grid_size and y - i >= 0 and grid[x + i][y - i] == WALL:
            break
        change_color(grid, grid_size, x+i, y-i, player)

    # Right Bottom Diagonal
    for i in xrange(1, 4):
        if x + i < grid_size and y + i < grid_size and grid[x + i][y + i] == WALL:
            break
        change_color(grid, grid_size, x+i, y+i, player)


def change_color(grid, grid_size, x, y, player):
    if x < 0 or x >= grid_size or y < 0 or y >= grid_size:
        return
    if grid[x][y] == player or grid[x][y] == player+3:
        return
    elif grid[x][y] == P1_LASER or grid[x][y] == P2_LASER:
        return
    elif grid[x][y] == EMPTY:
        grid[x][y] = player+3
    elif grid[x][y] == P1_AREA or grid[x][y] == P2_AREA:
        grid[x][y] = BOTH_AREA


def calculate_score(grid, grid_size):
    p1_score = 0
    p2_score = 0
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == P1_AREA or grid[i][j] == P1_LASER:
                p1_score = p1_score + 1
            elif grid[i][j] == P2_AREA or grid[i][j] == P2_LASER:
                p2_score = p2_score + 1
            elif grid[i][j] == BOTH_AREA:
                p1_score = p1_score + 1
                p2_score = p2_score + 1
    return p1_score, p2_score

if debug==True:
    def dprint(line):
        if debug == True:
            print line
else:
    def dprint(line):
        return


def get_empty_slots(grid, grid_size, player):
    # dprint("getting empty slots on ")
    # print_grid(grid, grid_size)
    moves = []
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            if grid[i][j] == EMPTY:
                moves.append((i, j))
    moves.sort(key=lambda move: check_move_value(grid, grid_size, move[0], move[1], player), reverse=True)
    # dprint("sorted moves " + str(moves))
    return moves

def check_move_value(grid, grid_size, x, y, player):
    # state = [row[:] for row in grid]
    state = deepcopy(grid)
    state[x][y] = player - 6
    mark_player(state, grid_size, x, y, player - 6)
    # dprint("Checking move value " + str(state))
    # dprint("returning score" + str(calculate_score(state, grid_size)))
    p1_score, p2_score = calculate_score(state, grid_size)
    return p1_score - p2_score


def max_value(grid, grid_size, player, alpha, beta):
    # dprint("inside max " + str(player))
    # print_grid(grid, grid_size)
    if player == AI:
        next_player = P1
    else:
        next_player = AI
    if check_game_over(grid, grid_size):
        p1_score, p2_score = calculate_score(grid, grid_size)
        if p1_score > p2_score:
            return [10, -1, -1, -1, -1]
        else:
            return [-10, -1, -1, -1, -1]


    available_moves = get_empty_slots(grid, grid_size, player)
    score = [-float('inf'), -1, -1, -1, -1]
    for i in xrange(len(available_moves)):
        state = deepcopy(grid)
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        # dprint("=======")
        # dprint("played move " + str(available_moves[i][0]) + " " + str(available_moves[i][1]))
        # print_grid(state, grid_size)
        # dprint("=======")

        new_score = min_value(state, grid_size, next_player, alpha, beta)


        # dprint("score inside max " + str(new_score) + " " + str(score))
        if new_score[0] > score[0]:
            score[0] = new_score[0]
            score[1] = available_moves[i][0]
            score[2] = available_moves[i][1]
            score[3] = new_score[3]
            score[4] = new_score[4]

        if score[0] > 0:
            return score

    return score


def min_value(grid, grid_size, player, alpha, beta):
    # print_grid(grid, grid_size)
    # dprint("inside min " + str(player))
    if player == AI:
        next_player = P1
    else:
        next_player = AI
    if check_game_over(grid, grid_size):
        p1_score, p2_score = calculate_score(grid, grid_size)
        if p1_score > p2_score:
            return [10, -1, -1, -1, -1]
        else:
            return [-10, -1, -1, -1, -1]

    available_moves = get_empty_slots(grid, grid_size, player)
    score = [float('inf'), -1, -1, -1, -1]
    for i in xrange(len(available_moves)):
        # state = [row[:] for row in grid]
        state = deepcopy(grid)
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        # dprint("=======")
        # dprint("played move " + str(available_moves[i][0]) + " " + str(available_moves[i][1]))
        # print_grid(state, grid_size)
        # dprint("=======")
        new_score = max_value(state, grid_size, next_player, alpha, beta)

        # dprint("score inside min " + str(new_score) + " " + str(score))
        if new_score[0] < score[0]:
            score[0] = new_score[0]
            score[1] = new_score[1]
            score[2] = new_score[2]
            score[3] = available_moves[i][0]
            score[4] = available_moves[i][1]

        if score[0] < 0:
            return score

    return score


def minimax(grid, grid_size, player):
    # return max_value(grid, grid_size, P1, -1000, 1000)
    available_moves = get_empty_slots(grid, grid_size, player)
    # print "avaiable moves " + str(available_moves)
    score = [-float('inf'), -1, -1, -1, -1]

    for i in xrange(len(available_moves)):
        # state = [row[:] for row in grid]
        state = deepcopy(grid)
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        # print_grid(state, grid_size)
        new_score = min_value(state, grid_size, AI, -float('inf'), float('inf'))
        # dprint("score inside minimax " + str(new_score) + " " + str(score) + " with move" + str(available_moves[i][0]) + " " + str(available_moves[i][1]))
        if new_score[0] > score[0]:
            score[0] = new_score[0]
            score[1] = available_moves[i][0]
            score[2] = available_moves[i][1]
            score[3] = new_score[3]
            score[4] = new_score[4]
        if score[0] > 0:
            return score

    return score

def main():
    grid, grid_size = read_file()
    apply_moves(grid, grid_size)
    # print_grid(grid, grid_size)
    dprint(calculate_score(grid, grid_size))
    # print_grid(grid, grid_size)

    score = minimax(grid, grid_size, 7)
    x = score[1]
    y = score[2]
    if debug == False:
        f2 = open("output.txt", "w")
        str2 = str(x) + " " + str(y) + "\n"
        f2.write(str2)
    else:
        print str(x) + " " + str(y)


if __name__ == '__main__':
    main()
