def check_game_over(grid, grid_size):
    print 1
def read_file():
    f1 = open("input5.txt", "r")
    grid_size = int(f1.readline())
    print(grid_size)

    grid = [[-1 for x in range(grid_size)] for y in range(grid_size)]

    for i in range(grid_size):
        line = f1.readline().strip()
        for j in range(grid_size):
            grid[i][j] = int(line[j])
    return grid, grid_size

def apply_moves(grid_size):
    for i in range (grid_size):
        for j in range (grid_size):
            if grid[i][j]==1 or grid[i][j]==2:
                print "1"
                # mark_player(grid, i,j, grid[i][j])

# def mark_player(grid, x, y, player):
#     mark = player+3
#     if grid[x][y]==player:
#         for i in range(3):
#             if x-i>=0 and grid[x-i][y]==0



def calculate_first_move(grid, grid_size):
    currentScore=0
    maxScore=0
    print(check_valid_position_for_laser(grid, grid_size, 0,0))

def check_valid_position_for_laser(grid, grid_size, x,y):
    boundaries = x>=0 and x<=grid_size-1 and y>=0 and y<=grid_size-1
    neighbors = True

    for i in range(3):
        if x - i >= 0 and (grid[i][y] == 1 or grid[i][y] == 2):
            neighbors = False
            break

    for j in range(3):
        if y - j >= 0 and (grid[x][j] == 1 or grid[x][j] == 2):
            neighbors = False
            break

    for i in range(3):
        if x + i < grid_size and (grid[i][y] == 1 or grid[i][y] == 2):
            neighbors = False
            break

    for j in range(3):
        if y + j < grid_size and grid[x][j] != 0:
            neighbors = False
            break

    return boundaries and neighbors


(grid, grid_size) = read_file()
calculate_first_move(grid, grid_size)