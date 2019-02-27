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
    f1 = open("input5.txt", "r")
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

    return p1_score, p2_score


def minimax2(grid, grid_size, player, alpha, beta):
    dprint("======inside minimax ========= " + str(player) + str(player==AI) + " " + str(player==P1))
    print_grid(grid, grid_size)
    if check_game_over(grid, grid_size):
        p1_score, p2_score = calculate_score(grid, grid_size)
        dprint("terminal score: " + str(p1_score) + " " + str(p2_score))
        return [p1_score, p2_score, -1, -1, -1, -1, p1_score-p2_score]

    available_moves = get_empty_slots(grid, grid_size)
    dprint("empty slots")
    dprint(str(available_moves))
    moves = []
    for i in range(len(available_moves)):
        move = [-1]*7
        state = [row[:] for row in grid]
        state[available_moves[i][0]][available_moves[i][1]] = player-6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player-6)

        if player == P1:
            result = minimax2(state, grid_size, AI, alpha, beta)
            dprint("Comparing alpha " + str(result[0]) + " " + str(result[1]) + " " + str(alpha) + " " + str(beta))
            if result[0] - result[1] >= alpha:
                alpha = result[0] - result[1]

            move[0] = result[0]
            move[1] = result[1]
            move[2] = available_moves[i][0]
            move[3] = available_moves[i][1]
            move[6] = result[6]

        else:
            result = minimax2(state, grid_size, P1, alpha, beta)
            dprint("Comparing beta " + str(result[0]) + " " + str(result[1]) + " " + str(alpha) + " " + str(beta))
            if result[0] - result[1] < beta:
                beta = result[0] - result[1]

            move[0] = result[0]
            move[1] = result[1]
            move[4] = available_moves[i][0]
            move[5] = available_moves[i][1]
            move[6] = result[6]

        moves.append(move)
        print "alpha beta " + str(alpha) + " " + str(beta)
        if alpha >= beta:
            break

    best_move = 0
    if player == P1:
        best_score = -10000
        for i in range(len(moves)):
            if moves[i][0] > best_score:
                best_score = moves[i][0]
                best_move = i
    else:
        best_score = 10000
        for i in range(len(moves)):
            if moves[i][1] > best_score:
                best_score = moves[i][1]
                best_move = i

    dprint("==== moves ====")
    dprint(str(moves))
    dprint("==== moves done ====")
    return moves[best_move]


def get_empty_slots(grid, grid_size):
    dprint("getting empty slots on ")
    dprint(str(grid))
    moves = []
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == EMPTY:
                moves.append((i, j))
    return moves

# def minimax(grid, grid_size, player):
#     dprint("=======inside minimax=========" + str(player))
#     if debug==True:
#         print_grid(grid, grid_size)
#     if check_game_over(grid, grid_size):
#         p1_score, p2_score = calculate_score(grid, grid_size)
#         dprint("Game over, returning " + str(p1_score) + " " + str(p2_score) + " -1 - 1 -1 -1")
#         return [p1_score, p2_score, -1, -1, -1, -1]
#
#     best_score = [-float('inf'), -float('inf'), -1, -1, -1, -1]
#
#     player_laser = player - 6
#     if player == AI:
#         next_player = P1
#     else:
#         next_player = AI
#
#     # place in every empty cell and then un-place
#     for i in range(grid_size):
#         for j in range(grid_size):
#             if grid[i][j] == EMPTY:
#
#                 state = [row[:] for row in grid]
#                 state[i][j] = player_laser
#                 mark_player(state, grid_size, i, j, player-6)
#
#                 score = minimax(state, grid_size, next_player)
#
#                 state = [row[:] for row in grid]
#                 dprint("Player: " + str(player) + str(score))
#
#                 if player == P1:
#                     state[score[2]][score[3]] = 1
#                     mark_player(state, grid_size, i, j, 1)
#
#                 else:
#                     state[score[4]][score[5]] = 2
#                     mark_player(state, grid_size, i, j, 2)
#
#                 if best_score[0] < score[0]:
#                     best_score[0] = score[0]
#                     if player == P1:
#                         best_score[2] = i
#                         best_score[3] = j
#                     if player == AI:
#                         best_score[4] = i
#                         best_score[5] = j
#
#                 if best_score[1] < score[1]:
#                     best_score[1] = score[1]
#                     if player == P1:
#                         best_score[2] = i
#                         best_score[3] = j
#                     if player == AI:
#                         best_score[4] = i
#                         best_score[5] = j
#
#
#                 dprint("current best score: " + str(best_score))
#                 dprint("returning score: " + str(best_score))
#     return best_score


def init_minimax(grid, grid_size, player):
    ans1 = -1
    x = -1
    y = -1
    available_moves = get_empty_slots(grid, grid_size)
    for i in range(len(available_moves)):
        dprint(str(available_moves[i]))
        state = [row[:] for row in grid]
        state[available_moves[i][0]][available_moves[i][1]] = player - 6
        mark_player(state, grid_size, available_moves[i][0], available_moves[i][1], player-6)
        dprint("=========Starting minimax================ with ")
        curr_ans = minimax2(state, grid_size, AI, -float('inf'), float('inf'))
        dprint("Final score for placing on: " + str(available_moves[i]) + " " + str(curr_ans))
        # if curr_ans[0] > curr_ans[1]:
        #     x = available_moves[i][0]
        #     y = available_moves[i][1]
        #     if debug == False:
        #         f2 = open("output.txt", "w")
        #         str2 = str(x) + " " + str(y) + "\n"
        #         f2.write(str2)
        #     else:
        #         print str(x) + " " + str(y)
        #     break

        if ans1 < curr_ans[0]:
            ans1 = curr_ans[0]
            x = available_moves[i][0]
            y = available_moves[i][1]

    if debug == False:
        f2 = open("output.txt", "w")
        str2 = str(x) + " " + str(y) + "\n"
        f2.write(str2)
    else:
        print str(x) + " " + str(y)

def dprint(line):
    if debug == True:
        print line


def main():
    grid, grid_size = read_file()
    apply_moves(grid, grid_size)
    # print_grid(grid, grid_size)
    dprint(calculate_score(grid, grid_size))
    init_minimax(grid, grid_size, 7)
    #move = minimax(grid, grid_size, 7)



if __name__ == '__main__':
    main()