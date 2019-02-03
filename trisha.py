import time

pinf = float("inf")
ninf = float("-inf")

def makeMatrix(fileName):
    input = open(fileName, "r")
    n = input.readline()
    n = int(n)
    mat = [[0 for i in range(n)] for i in range(n)]
    for x in range(n):
        row = input.readline().strip('\n')
        for y in range(n):
            mat[x][y] = int(row[y])
    return mat, n

def print_grid(grid, grid_size):
    s = ""
    for i in xrange(grid_size):
        for j in xrange(grid_size):
            s = s + str(grid[i][j]) + " "
        s += '\n'
    print s

def traverseInput(mat, n):
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 1:
                updateMatrix(mat, n, 1, i, j)
            elif mat[i][j] == 2:
                updateMatrix(mat, n, 2, i, j)
    return mat


def updateGrid(mat, n, p, x, y):
    if mat[x][y] == 0:
        if p == 1:
            mat[x][y] = 5
        else:
            mat[x][y] = 6
    elif mat[x][y] == 3:
        mat[x][y] = 3
    elif mat[x][y] != 0:
        if mat[x][y] == 5 and p == 1:
            mat[x][y] = 5
        elif mat[x][y] == 6 and p == 2:
            mat[x][y] = 6
        elif mat[x][y] == 5 and p == 2:
            mat[x][y] = 4
        elif mat[x][y] == 6 and p == 1:
            mat[x][y] = 4
        elif mat[x][y] == 4:
            mat[x][y] = 4
    return mat

# def updateMatrix(mat, n, p, x, y):
#     indices_list = []
#     score_ctr = 0
#     mat[x][y] = p
#     indices_list.append((x, y))
#     score_ctr = score_ctr + 1
#     for i in range(3):
#         if x-i >= 0 and mat[x-i][y] != 3:
#             mat = updateGrid(mat, n, p, x - i, y)
#             indices_list.append((x-i, y))
#             score_ctr = score_ctr + 1
#         if x+i < n and mat[x+i][y] != 3:
#             mat = updateGrid(mat, n, p, x + i, y)
#             indices_list.append((x + i, y))
#             score_ctr = score_ctr + 1
#         if y-i >= 0 and mat[x][y-i] != 3:
#             mat = updateGrid(mat, n, p, x, y - i)
#             indices_list.append((x, y - i))
#             score_ctr = score_ctr + 1
#         if y+i < n and mat[x][y+i] != 3:
#             mat = updateGrid(mat, n, p, x, y + i)
#             indices_list.append((x, y + i))
#             score_ctr = score_ctr + 1
#     #Diagonals
#         if x-i >=0 and y-i >= 0 and mat[x-i][y-i] != 3:
#             mat = updateGrid(mat, n, p, x - i, y - i)
#             indices_list.append((x - i, y - i))
#             score_ctr = score_ctr + 1
#         if x+i < n and y+i < n and mat[x+i][y+i] != 3:
#             mat = updateGrid(mat, n, p, x + i, y + i)
#             indices_list.append((x + i, y + i))
#             score_ctr = score_ctr + 1
#         if x+i < n and y-i >= 0 and mat[x+i][y-i] != 3:
#             mat = updateGrid(mat, n, p, x + i, y - i)
#             indices_list.append((x + i, y - i))
#             score_ctr = score_ctr + 1
#         if x-i >= 0 and y+i < n and mat[x-i][y+i] != 3:
#             mat = updateGrid(mat, n, p, x - i, y + i)
#             indices_list.append((x - i, y + i))
#             score_ctr = score_ctr + 1
#     return score_ctr, indices_list, mat

def updateMatrix(mat, n, p, x, y):
    indices_list = []
    score_ctr = 0
    mat[x][y] = p
    # indices_list.append((x, y))
    # score_ctr = score_ctr + 1
    if x-1 >= 0 and mat[x-1][y] != 3:
        mat = updateGrid(mat, n, p, x - 1, y)
        # indices_list.append((x-1, y))
        # score_ctr = score_ctr + 1
        if x-2 >= 0 and mat[x-2][y] != 3:
            mat = updateGrid(mat, n, p, x - 2, y)
            # indices_list.append((x - 2, y))
            # score_ctr = score_ctr + 1
            if x-3 >= 0 and mat[x-3][y] != 3:
                mat = updateGrid(mat, n, p, x - 3, y)
                # indices_list.append((x - 3, y))
                # score_ctr = score_ctr + 1
    if x+1 < n and mat[x+1][y] != 3:
        mat = updateGrid(mat, n, p, x + 1, y)
        # indices_list.append((x + 1, y))
        # score_ctr = score_ctr + 1
        if x+2 < n and mat[x+2][y] != 3:
            mat = updateGrid(mat, n, p, x + 2, y)
            # indices_list.append((x + 2, y))
            # score_ctr = score_ctr + 1
            if x+3 < n and mat[x+3][y] != 3:
                mat = updateGrid(mat, n, p, x + 3, y)
                # indices_list.append((x + 3, y))
                # score_ctr = score_ctr + 1
    if y-1 >= 0 and mat[x][y-1] != 3:
        mat = updateGrid(mat, n, p, x, y - 1)
        # indices_list.append((x, y - 1))
        # score_ctr = score_ctr + 1
        if y-2 >= 0 and mat[x][y-2] != 3:
            mat = updateGrid(mat, n, p, x, y - 2)
            # indices_list.append((x, y - 2))
            # score_ctr = score_ctr + 1
            if y-3 >= 0 and mat[x][y-2] != 3:
                mat = updateGrid(mat, n, p, x, y - 3)
                # indices_list.append((x, y - 3))
                # score_ctr = score_ctr + 1
    if y+1 < n and mat[x][y+1] != 3:
        mat = updateGrid(mat, n, p, x, y + 1)
        # indices_list.append((x, y + 1))
        # score_ctr = score_ctr + 1
        if y+2 < n and mat[x][y+2] != 3:
            mat = updateGrid(mat, n, p, x, y + 2)
            # indices_list.append((x, y + 2))
            # score_ctr = score_ctr + 1
            if y+3 < n and mat[x][y+3] != 3:
                mat = updateGrid(mat, n, p, x, y + 3)
                # indices_list.append((x, y + 3))
                # score_ctr = score_ctr + 1
    #Diagonals
    if x-1 >=0 and y-1 >= 0 and mat[x-1][y-1] != 3:
        mat = updateGrid(mat, n, p, x - 1, y - 1)
        # indices_list.append((x - 1, y - 1))
        # score_ctr = score_ctr + 1
        if x-2 >= 0 and y-2 >= 0 and mat[x-2][y-2] != 3:
            mat = updateGrid(mat, n, p, x - 2, y - 2)
            # indices_list.append((x - 2, y - 2))
            # score_ctr = score_ctr + 1
            if x-3 >= 0 and y-3 >= 0 and mat[x-3][y-3] != 3:
                mat = updateGrid(mat, n, p, x - 3, y - 3)
                # indices_list.append((x - 3, y - 3))
                # score_ctr = score_ctr + 1
    if x+1 < n and y+1 < n and mat[x+1][y+1] != 3:
        mat = updateGrid(mat, n, p, x + 1, y + 1)
        # indices_list.append((x + 1, y + 1))
        # score_ctr = score_ctr + 1
        if x+2 < n and y+2 < n and mat[x+2][y+2] != 3:
            mat = updateGrid(mat, n, p, x + 2, y + 2)
            # indices_list.append((x + 2, y + 2))
            # score_ctr = score_ctr + 1
            if x+3 < n and y+3 < n and mat[x+3][y+3] != 3:
                mat = updateGrid(mat, n, p, x + 3, y + 3)
                # indices_list.append((x + 3, y + 3))
                # score_ctr = score_ctr + 1
    if x+1 < n and y-1 >= 0 and mat[x+1][y-1] != 3:
        mat = updateGrid(mat, n, p, x + 1, y - 1)
        # indices_list.append((x + 1, y - 1))
        # score_ctr = score_ctr + 1
        if x+2 < n and y-2 >= 0 and mat[x+2][y-2] != 3:
            mat = updateGrid(mat, n, p, x + 2, y - 2)
            # indices_list.append((x + 2, y - 2))
            # score_ctr = score_ctr + 1
            if x+3 < n and y-3 >= 0 and mat[x+3][y-3] != 3:
                mat = updateGrid(mat, n, p, x + 3, y - 3)
                # indices_list.append((x + 3, y - 3))
                # score_ctr = score_ctr + 1
    if x-1 >= 0 and y+1 < n and mat[x-1][y+1] != 3:
        mat = updateGrid(mat, n, p, x - 1, y + 1)
        # indices_list.append((x - 1, y + 1))
        # score_ctr = score_ctr + 1
        if x-2 >= 0 and y+2 < n and mat[x-2][y+2] != 3:
            mat = updateGrid(mat, n, p, x - 2, y + 2)
            # indices_list.append((x - 2, y + 2))
            # score_ctr = score_ctr + 1
            if x-3 >= 0 and y+3 < n and mat[x-3][y+3] != 3:
                mat = updateGrid(mat, n, p, x - 3, y + 3)
                # indices_list.append((x - 3, y + 3))
                # score_ctr = score_ctr + 1
    return score_ctr, indices_list, mat

def restoreMatrix(grid, indices, player):
    if player == 1:
        for i in range(len(indices)):
            if grid[indices[i][0]][indices[i][1]] == 1 or grid[indices[i][0]][indices[i][1]] == 5:
                grid[indices[i][0]][indices[i][1]] = 0
            if grid[indices[i][0]][indices[i][1]] == 4:
                grid[indices[i][0]][indices[i][1]] = 6
    if player == 2:
        for i in range(len(indices)):
            if grid[indices[i][0]][indices[i][1]] == 2 or grid[indices[i][0]][indices[i][1]] == 6:
                grid[indices[i][0]][indices[i][1]] = 0
            if grid[indices[i][0]][indices[i][1]] == 4:
                grid[indices[i][0]][indices[i][1]] = 5
    return grid

def findScore(mat, n):
    score1 = 0
    score2 = 0
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 5 or mat[i][j] == 1:
                score1 = score1 + 1
            if mat[i][j] == 6 or mat[i][j] == 2:
                score2 = score2 + 1
            if mat[i][j] == 4:
                score1 = score1 + 1
                score2 = score2 + 1
    return score1 - score2

def isEnd(mat, n):
    for i in range(n):
        for j in range(n):
            if mat[i][j] == 0:
                return False
            else:
                continue
    return True

def max_value(grid, score, n, alpha, beta):
    print "inside max - "
    print_grid(grid, n)
    if isEnd(grid, n):
        score = findScore(grid, n)
        # print("End")
        if score > 0:
            return 5
        elif score < 0:
            return -5
        elif score == 0:
            return 0
        # return score1
    v = float("-inf")
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                # print(grid)
                copy = [row[:] for row in grid]
                (new_score, indices, copy) = updateMatrix(copy, n, 1, i, j)
                # print("Player 1")
                # print(grid)
                # v = findScore(grid, n)
                v = max(v, min_value(copy, score+new_score, n, alpha, beta))
                # if v >= beta:
                #     return v
                # alpha = max(alpha, v)
                # restoreMatrix(grid, indices, 1)
                # grid = [row[:] for row in copy]
    return v

def min_value(grid, score, n, alpha, beta):
    print "inside min_value - "
    print_grid(grid, n)
    if isEnd(grid, n):
        score = findScore(grid, n)
        # print("End")
        if score > 0:
            return 5
        elif score < 0:
            return -5
        elif score == 0:
            return 0
        # return score1
    v = float("inf")
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                # print(grid)
                copy = [row[:] for row in grid]
                (new_score, indices, copy) = updateMatrix(copy, n, 2, i, j)
                # print("Player 2")
                # print(grid)
                # v = findScore(grid, n)
                v = min(v, max_value(copy, score-new_score, n, alpha, beta))
                # if v <= alpha:
                #     return v
                # beta = min(beta, v)
                # restoreMatrix(grid, indices, 2)
                # grid = [row[:] for row in copy]
    return v

def minimax(grid, n):
    max = float("-inf")
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                copy = [row[:] for row in grid]
                (new_score, indices, copy) = updateMatrix(copy, n, 1, i, j)
                # print("Player 1")
                # print(grid)
                temp = min_value(copy, new_score, n, ninf, pinf)
                if max < temp:
                    max = temp
                    max_indices = (i,j)
                    # print(copy)
                    # if max == 5:
                    #     break
                # if temp == 5:
                #     max_indices = (i,j)
                    # break
                # grid = [row[:] for row in copy]
    return max_indices

(mat, n) = makeMatrix("input1.txt")
# print(mat)
newGrid = traverseInput(mat, n)
# print newGrid

start = time.time()
(i, j) = minimax(newGrid, n)
end = time.time()
# f = open("output.txt", "w")
# f.write(str(i)+" "+str(j))
print str(i)+" "+str(j)