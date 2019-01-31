from enum import Enum
debug = True
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
    grid = [[-1 for x in range(grid_size)] for y in range(grid_size)]

    for i in range(grid_size):
        line = f1.readline().strip()
        for j in range(grid_size):
            grid[i][j] = int(line[j])
    dprint("====read====")
    dprint("====read done===")
    return grid, grid_size


def print_grid(grid, grid_size):
    s = ""
    for i in range(grid_size):
        for j in range(grid_size):
            s = s + str(grid[i][j]) + " "
        s += '\n'
    print s


def apply_moves(grid, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 1 or grid[i][j] == 2:
                mark_player(grid, grid_size, i, j, grid[i][j])


# Expects the moves to be applied
def check_game_over(grid, grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 0:
                return False
    return True


def mark_player(grid, grid_size, x, y, player):
    dprint("Marking player" + str(player))
    # Upper 3
    for i in range(1, 4):
        if x-i >= 0 and grid[x-i][y] == WALL:
            break
        change_color(grid, grid_size, x-i, y, player)

    # Lower 3
    for i in range(1, 4):
        if x+i < grid_size and grid[x+i][y] == WALL:
            break
        change_color(grid, grid_size, x+i, y, player)

    # Left 3
    for i in range(1, 4):
        if y - i >= 0 and grid[x][y-i] == WALL:
            break
        change_color(grid, grid_size, x, y-i, player)

    # Right 3
    for i in range(1, 4):
        if y+i < grid_size and grid[x][y+i] == WALL:
            break
        change_color(grid, grid_size, x, y+i, player)

    # Left Top Diagonal
    for i in range(1, 4):
        if x-i >= 0 and y-i >= 0 and grid[x-i][y-i] == WALL:
            break
        change_color(grid, grid_size, x-i, y-i, player)

    # Right Top Diagonal
    for i in range(1,4):
        if x-i >= 0 and y+i < grid_size and grid[x-i][y+i] == WALL:
            break
        change_color(grid, grid_size, x-i, y+i, player)

    # Left Bottom Diagonal
    for i in range(1, 4):
        if x + i < grid_size and y - i >= 0 and grid[x + i][y - i] == WALL:
            break
        change_color(grid, grid_size, x+i, y-i, player)

    # Right Bottom Diagonal
    for i in range(1, 4):
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
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == P1_AREA or grid[i][j] == P1_LASER:
                p1_score = p1_score + 1
            elif grid[i][j] == P2_AREA or grid[i][j] == P2_LASER:
                p2_score = p2_score + 1
            elif grid[i][j] == BOTH_AREA:
                p1_score = p1_score + 1
                p2_score = p2_score + 1

    return p1_score - p2_score

def dprint(line):
    if debug == True:
        print line


def get_empty_slots(grid, grid_size):
    dprint("getting empty slots on ")
    dprint(str(grid))
    moves = []
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == EMPTY:
                moves.append((i, j))
    return moves


def max_value(grid, grid_size, player):
    print "inside max " + str(player)
    if player == AI:
        next_player = P1
    else:
        next_player = AI
    if check_game_over(grid, grid_size):
        score = calculate_score(grid, grid_size)
        return score
    available_moves = get_empty_slots(grid, grid_size)
    score = -float('inf')
    for i in range(len(available_moves)):
        state = [row[:] for row in grid]
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        new_score = min_value(state, grid_size, next_player)

        if new_score > score:
            new_score = score


    print("Max value score = " + str(score))
    return new_score


def min_value(grid, grid_size, player):
    print "inside min " + str(player)
    if player == AI:
        next_player = P1
    else:
        next_player = AI
    if check_game_over(grid, grid_size):
        score = calculate_score(grid, grid_size)
        return score
    available_moves = get_empty_slots(grid, grid_size)
    score = float('inf')
    for i in range(len(available_moves)):
        state = [row[:] for row in grid]
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        new_score = min_value(state, grid_size, next_player)

        if new_score > score:
            new_score = score

    print("Min value score = " + str(score))
    return new_score


def minimax(grid, grid_size, player):
    available_moves = get_empty_slots(grid, grid_size)
    score = - float('inf')
    for i in range(len(available_moves)):
        state = [row[:] for row in grid]
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player - 6)
        score = max(score,  min_value(state, grid_size, AI))
    return score

def main():
    grid, grid_size = read_file()
    apply_moves(grid, grid_size)
    # print_grid(grid, grid_size)
    dprint(calculate_score(grid, grid_size))
    print(minimax(grid, grid_size, 7))
    #move = minimax(grid, grid_size, 7)


if __name__ == '__main__':
    main()
