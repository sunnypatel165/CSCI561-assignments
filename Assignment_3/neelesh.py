import string
import time
time0 = time.time()
fp = open("input4.txt", "r")
inf = -float("inf")
grid_size = int(fp.readline())
matrix = [[-9999 for x in range(0, grid_size)] for y in range(0, grid_size)]
policy = [['' for x in range(0, grid_size)] for y in range(0, grid_size)]
walls_no = int(fp.readline())
wall_cells = set()
terminals = set()
non_terminals = set()

for i in range(0, walls_no):
    line = fp.readline()
    a = int(string.split(line, ',')[0]) - 1
    b = int(string.split(line, ',')[1]) - 1
    matrix[a][b] = inf
    wall_cells.add((a, b))
terminal_state = int(fp.readline())

for i in range(0, terminal_state):
    line = fp.readline()
    a = int(string.split(line, ',')[0]) - 1
    b = int(string.split(line, ',')[1]) - 1
    r = float(string.split(line, ',')[2])
    terminals.add((a, b))
    matrix[a][b] = r

p = float(fp.readline())
q = float((1.0 - p)/2.0)
reward = float(fp.readline())
for i in range(0, grid_size):
    for j in range(0, grid_size):
        if matrix[i][j] == -9999:
            matrix[i][j] = reward
        if (i,j) not in terminals and (i,j) not in wall_cells:
            non_terminals.add((i, j))


gamma = float(fp.readline())
discount_factor = gamma


def check_boundary(i, j):
    if(0 <= i < grid_size) and (0 <= j < grid_size):
        return True
    else:
        return False


def up_move(matrix, i, j):
    utility_same = 0
    utility_up = 0
    utility_left = 0
    utility_right = 0
    # Checking if wall is present or not in upper cell
    if i == 0:
        return float(1) * matrix[i][j]

    if check_boundary(i-1, j) is True:
        if matrix[i-1][j] != inf:
            utility_up = p * matrix[i - 1][j]
        else:
            utility_same = utility_same + p * matrix[i][j]
    else:
        utility_same = utility_same + p * matrix[i][j]

        # Checking if wall is present or not in diagonal right cell
    if check_boundary(i-1, j+1) is True:
        if matrix[i-1][j+1] != inf:
            utility_right = q * matrix[i - 1][j + 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

        # Checking if wall is present or not in diagonal left cell
    if check_boundary(i-1, j-1) is True:
        if matrix[i-1][j-1] != inf:
            utility_left = q * matrix[i - 1][j - 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    utility_move_up = utility_up + utility_right + utility_left + utility_same
    return utility_move_up


def down_move(matrix, i, j):
    utility_same = 0
    utility_down = 0
    utility_left = 0
    utility_right = 0
    if i == grid_size - 1:
        return float(1) * matrix[i][j]
    # Checking if wall is present or not in below cell
    if check_boundary(i + 1, j) is True:
        if matrix[i + 1][j] != inf:
            utility_down = p * matrix[i + 1][j]
        else:
            utility_same = utility_same + p * matrix[i][j]
    else:
        utility_same = utility_same + p * matrix[i][j]

    # Checking if wall is present or not in diagonal right cell
    if check_boundary(i + 1, j + 1) is True:
        if matrix[i + 1][j + 1] != inf:
            utility_right = q * matrix[i + 1][j + 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    # Checking if wall is present or not in diagonal left cell
    if check_boundary(i + 1, j - 1) is True:
        if matrix[i + 1][j - 1] != inf:
            utility_left = q * matrix[i + 1][j - 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    utility_move_down = utility_down + utility_right + utility_left + utility_same
    return utility_move_down


def right_move(matrix, i, j):
    utility_same = 0
    utility_right = 0
    utility_d_left = 0
    utility_d_right = 0
    if j == grid_size - 1:
        return float(1) * matrix[i][j]
    # Checking if wall is present or not in below cell
    if check_boundary(i, j+1) is True:
        if matrix[i][j+1] != inf:
            utility_right = p * matrix[i][j+1]
        else:
            utility_same = utility_same + p * matrix[i][j]
    else:
        utility_same = utility_same + p * matrix[i][j]

    # Checking if wall is present or not in diagonal right cell
    if check_boundary(i + 1, j + 1) is True:
        if matrix[i + 1][j + 1] != inf:
            utility_d_right = q * matrix[i + 1][j + 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    # Checking if wall is present or not in diagonal left cell
    if check_boundary(i - 1, j + 1) is True:
        if matrix[i - 1][j + 1] != inf:
            utility_d_left = q * matrix[i - 1][j + 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    utility_move_right = utility_right + utility_d_right + utility_d_left + utility_same
    return utility_move_right


def left_move(matrix, i, j):
    utility_same = 0
    utility_left = 0
    utility_d_left = 0
    utility_d_right = 0
    if j == 0:
        return float(1) * matrix[i][j]
    # Checking if wall is present or not in below cell
    if check_boundary(i, j-1) is True:
        if matrix[i][j-1] != inf:
            utility_left = p * matrix[i][j-1]
        else:
            utility_same = utility_same + p * matrix[i][j]
    else:
        utility_same = utility_same + p * matrix[i][j]

    # Checking if wall is present or not in diagonal right cell
    if check_boundary(i - 1, j - 1) is True:
        if matrix[i - 1][j - 1] != inf:
            utility_d_right = q * matrix[i - 1][j - 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    # Checking if wall is present or not in diagonal left cell
    if check_boundary(i + 1, j - 1) is True:
        if matrix[i + 1][j - 1] != inf:
            utility_d_left = q * matrix[i + 1][j - 1]
        else:
            utility_same = utility_same + q * matrix[i][j]
    else:
        utility_same = utility_same + q * matrix[i][j]

    utility_move_left = utility_left + utility_d_right + utility_d_left + utility_same
    return utility_move_left


def max_action_utility(matrix, i, j):
    ut_up = up_move(matrix, i, j)
    ut_down = down_move(matrix, i, j)
    ut_left = left_move(matrix, i, j)
    ut_right = right_move(matrix, i, j)
    util = max(ut_up, ut_down, ut_left, ut_right)
    if util == ut_up:
        action = "U"
    elif util == ut_down:
        action = "D"
    elif util == ut_left:
        action = "L"
    elif util == ut_right:
        action = "R"
    final = reward + (gamma * util)
    return final, action


def calc_utility():
    global policy
    global non_terminals
    diff = 1
    list_temp = list(non_terminals)
    for x in range(0, grid_size):
        for y in range(0, grid_size):
            if (x, y) in wall_cells:
                policy[x][y] = "N"
            elif (x, y) in terminals:
                policy[x][y] = "E"
    while len(list_temp) > 0 and diff > 0.00006:
        diff = 0
        list_nodes = list(list_temp)
        list_temp = set()
        for (x, y) in list_nodes:
            utility, action = max_action_utility(matrix, x, y)
            policy[x][y] = action
            if matrix[x][y] < utility:
                list_temp.add((x, y))
                diff = max(diff, abs(matrix[x][y] - utility))
                list_temp = add_neighbour_states(list_temp, x, y)
                matrix[x][y] = utility



    with open('output.txt', 'w') as the_file:
        for i in range(0, grid_size, 1):
            for j in range(0, grid_size, 1):
                the_file.write(str(policy[i][j]))
                if j != grid_size - 1:
                    the_file.write(",")
            if i != grid_size - 1:
                the_file.write("\n")

    the_file.close()


neighbor_map = {}


def add_neighbour_states(list_temp, i, j):
    for (n1, n2) in neighbor_map[(i, j)]:
        list_temp.add((n1, n2))
    return list_temp


def precompute_neighbour_states():
    for i in range(grid_size):
        for j in range(grid_size):
            list_temp = set()
            list_temp.add((i,j))
            if check_boundary(i + 1, j) and (i + 1, j) in non_terminals:
                list_temp.add((i + 1, j))
            if check_boundary(i -1, j) and (i -1, j) in non_terminals:
                list_temp.add((i - 1, j))
            if check_boundary(i, j -1) and (i, j - 1) in non_terminals:
                list_temp.add((i , j -1))
            if check_boundary(i, j + 1) and (i, j + 1) in non_terminals:
                list_temp.add((i, j + 1))
            if check_boundary(i + 1, j -1) and (i + 1, j -1) in non_terminals:
                list_temp.add((i + 1, j -1))
            if check_boundary(i + 1, j + 1) and (i + 1, j + 1) in non_terminals:
                list_temp.add((i + 1, j + 1))
            if check_boundary(i - 1, j - 1) and (i - 1, j -1) in non_terminals:
                list_temp.add((i - 1, j -1))
            if check_boundary(i - 1, j + 1) and (i - 1, j + 1) in non_terminals:
                list_temp.add((i - 1, j + 1))
            neighbor_map[(i,j)] = list_temp


print "Time to compute neighbours"
precompute_neighbour_states()
time1 = time.time()
print (time1 - time0)
calc_utility()
time2 = time.time()
print time2 - time0