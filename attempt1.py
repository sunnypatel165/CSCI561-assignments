from enum import Enum


class State(Enum):
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
    f1 = open("input1.txt", "r")
    grid_size = int(f1.readline())
    grid = [[-1 for x in range(grid_size)] for y in range(grid_size)]

    for i in range(grid_size):
        line = f1.readline().strip()
        for j in range(grid_size):
            grid[i][j] = int(line[j])
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
    # Upper 3
    for i in range(1, 4):
        if x-i >= 0 and grid[x-i][y] == State.WALL:
            break
        change_color(grid, grid_size, x-i, y, player)

    # Lower 3
    for i in range(1, 4):
        if x+i < grid_size and grid[x+i][y] == State.WALL:
            break
        change_color(grid, grid_size, x+i, y, player)

    # Left 3
    for i in range(1, 4):
        if y - i >= 0 and grid[x][y-i] == State.WALL:
            break
        change_color(grid, grid_size, x, y-i, player)

    # Right 3
    for i in range(1, 4):
        if y+i < grid_size and grid[x][y+i] == State.WALL:
            break
        change_color(grid, grid_size, x, y+i, player)

    # Left Top Diagonal
    for i in range(1, 4):
        if x-i >= 0 and y-i >= 0 and grid[x-i][y-i] == State.WALL:
            break
        change_color(grid, grid_size, x-i, y-i, player)

    # Right Top Diagonal
    for i in range(1,4):
        if x-i >= 0 and y+i < grid_size and grid[x-i][y+i] == State.WALL:
            break
        change_color(grid, grid_size, x-i, y+i, player)

    # Left Bottom Diagonal
    for i in range(1, 4):
        if x + i < grid_size and y - i >= 0 and grid[x + i][y - i] == State.WALL:
            break
        change_color(grid, grid_size, x+i, y-i, player)

    # Right Bottom Diagonal
    for i in range(1, 4):
        if x + i < grid_size and y + i < grid_size and grid[x + i][y + i] == State.WALL:
            break
        change_color(grid, grid_size, x+i, y+i, player)


def change_color(grid, grid_size, x, y, player):
    if x < 0 or x >= grid_size or y < 0 or y >= grid_size:
        return
    if grid[x][y] == player:
        return
    elif grid[x][y] == State.P1_LASER or grid[x][y] == State.P2_LASER:
        return
    elif grid[x][y] == State.EMPTY:
        grid[x][y] = player+3
    elif grid[x][y] == State.P1_AREA or grid[x][y] == State.P2_AREA:
        grid[x][y] = State.BOTH_AREA


def calculate_score(grid, grid_size):
    p1_score = 0
    p2_score = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == State.P1_AREA or grid[i][j] == State.P1_LASER:
                p1_score = p1_score + 1
            elif grid[i][j] == State.P2_AREA or grid[i][j] == State.P2_LASER:
                p2_score = p2_score + 1
            elif grid[i][j] == State.BOTH_AREA:
                p1_score = p1_score + 1
                p2_score = p2_score + 1

    return p1_score, p2_score


def minimax(grid, grid_size, player):
    print "=======inside minimax=========", str(player)
    print_grid(grid, grid_size)
    if check_game_over(grid, grid_size):
        print "Game over, returning", str(calculate_score(grid, grid_size))
        return [calculate_score(grid, grid_size), -1, -1]

    best_score = [-float('inf'), -float('inf'), -1, -1]

    player_laser = player - 6
    if player == State.AI:
        next_player = State.P1
    else:
        next_player = State.AI

    # place in every empty cell and then un-place
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == State.EMPTY:
                state = [row[:] for row in grid]
                state[i][j] = player_laser
                mark_player(state, grid_size, i, j, player-6)
                score = minimax(state, grid_size, next_player)
                state[i][j] = State.EMPTY

                if player == State.P1:
                    if best_score[0] < score[0]:
                        best_score[0] = score[0]
                        best_score[2] = i
                        best_score[3] = j
                if player == State.AI:
                    if best_score[1] < score[1]:
                        best_score[1] = score[1]
                        best_score[2] = i
                        best_score[3] = j
    print "returning score: ", str(best_score)
    return best_score



def my_turn(grid, grid_size):
    if check_game_over(grid, grid_size):
        print "Game over"
        print_grid(grid, grid_size)
        return

    move = minimax(grid, grid_size)



def main():
    grid, grid_size = read_file()
    apply_moves(grid, grid_size)
    print_grid(grid, grid_size)
    print calculate_score(grid, grid_size)

    print minimax(grid, grid_size, State.P1)



if __name__ == '__main__':
    main()