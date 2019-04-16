from copy import deepcopy
import time

wall_no = 0
terminal_no = 0
walls = []
terminals = []
neighbour = {}

optimal_path = []
terminal_reward = []
grid = []
states = set()
actions = ['U', 'D', 'R', 'L']
probDict = {}
sec = time.time()


def read_input(file_name):
    with open(file_name, 'r') as f:
        global grid_size
        grid_size = int(f.readline().rstrip('\n'))
        wall_no = int(f.readline().rstrip('\n'))
        for i in range(wall_no):
            x = f.readline().rstrip('\n').split(',')
            walls.append([int(x[0]) - 1, int(x[1]) - 1])

        terminal_no = int(f.readline().rstrip('\n'))
        for i in range(terminal_no):
            x = f.readline().rstrip('\n').split(',')
            terminals.append([int(x[0]) - 1, int(x[1]) - 1])
            terminal_reward.append(float(x[2]))
        global prob
        global Rp
        global gamma
        prob = float(f.readline().rstrip('\n'))
        Rp = float(f.readline().rstrip('\n'))
        gamma = float(f.readline().rstrip('\n'))
        for i in range(grid_size):
            li = []
            op = []

            for x in range(grid_size):
                if [i, x] not in terminals and [i, x] not in walls:
                    states.add((i, x))
                    li.append(Rp)
                    op.append('')

                if [i, x] in terminals:
                    inde = terminals.index([i, x])
                    v = terminal_reward[inde]
                    li.append(v)
                    op.append('E')

                if [i, x] in walls:
                    li.append(0.0)
                    op.append('N')

            grid.append(li)
            optimal_path.append(op)


def preprocessProb():
    for s in states:
        x = s[0]
        y = s[1]
        probDict[s] = {'U': [0, 0, 0, 0, 0, 0], 'D': [0, 0, 0, 0, 0, 0], 'L': [0, 0, 0, 0, 0, 0],
                       'R': [0, 0, 0, 0, 0, 0]}
        neighbour[s] = []

        for action in actions:
            if action == 'U':
                if x - 1 >= 0 and [x - 1, y] not in walls:
                    probDict[s]['U'][0] = prob
                    probDict[s]['U'][1] = 0
                    if [x - 1, y] not in terminals:
                        neighbour[s].append((x - 1, y))
                else:
                    probDict[s]['U'][0] = 0
                    probDict[s]['U'][1] = prob

                if x - 1 >= 0 and y - 1 >= 0 and [x - 1, y - 1] not in walls:
                    probDict[s]['U'][2] = 0.5 * (1 - prob)
                    probDict[s]['U'][3] = 0
                    if [x - 1, y - 1] not in terminals:
                        neighbour[s].append((x - 1, y - 1))
                else:
                    probDict[s]['U'][2] = 0
                    probDict[s]['U'][3] = 0.5 * (1 - prob)
                if x - 1 >= 0 and y + 1 < grid_size and [x - 1, y + 1] not in walls:
                    probDict[s]['U'][4] = 0.5 * (1 - prob)
                    probDict[s]['U'][5] = 0
                    if [x - 1, y + 1] not in terminals:
                        neighbour[s].append((x - 1, y + 1))
                else:
                    probDict[s]['U'][4] = 0
                    probDict[s]['U'][5] = 0.5 * (1 - prob)

            elif action == 'D':
                if x + 1 < grid_size and [x + 1, y] not in walls:
                    probDict[s]['D'][0] = prob
                    probDict[s]['D'][1] = 0
                    if [x + 1, y] not in terminals:
                        neighbour[s].append((x + 1, y))
                else:
                    probDict[s]['D'][0] = 0
                    probDict[s]['D'][1] = prob
                if x + 1 < grid_size and y - 1 >= 0 and [x + 1, y - 1] not in walls:
                    probDict[s]['D'][3] = 0
                    probDict[s]['D'][2] = 0.5 * (1 - prob)
                    if [x + 1, y - 1] not in terminals:
                        neighbour[s].append((x + 1, y - 1))
                else:
                    probDict[s]['D'][2] = 0
                    probDict[s]['D'][3] = 0.5 * (1 - prob)
                if x + 1 < grid_size and y + 1 < grid_size and [x + 1, y + 1] not in walls:
                    probDict[s]['D'][4] = 0.5 * (1 - prob)
                    probDict[s]['D'][5] = 0
                    if [x + 1, y + 1] not in terminals:
                        neighbour[s].append((x + 1, y + 1))
                else:
                    probDict[s]['D'][4] = 0
                    probDict[s]['D'][5] = 0.5 * (1 - prob)


            elif action == 'L':
                if y - 1 >= 0 and [x, y - 1] not in walls:
                    probDict[s]['L'][0] = prob
                    probDict[s]['L'][1] = 0
                    if [x, y - 1] not in terminals:
                        neighbour[s].append((x, y - 1))
                else:
                    probDict[s]['L'][0] = 0
                    probDict[s]['L'][1] = prob
                if x - 1 >= 0 and y - 1 >= 0 and [x - 1, y - 1] not in walls:
                    probDict[s]['L'][2] = 0.5 * (1 - prob)
                    probDict[s]['L'][3] = 0
                    if [x - 1, y - 1] not in terminals:
                        neighbour[s].append((x - 1, y - 1))
                else:
                    probDict[s]['L'][2] = 0
                    probDict[s]['L'][3] = 0.5 * (1 - prob)
                if y - 1 >= 0 and x + 1 < grid_size and [x + 1, y - 1] not in walls:
                    probDict[s]['L'][4] = 0.5 * (1 - prob)
                    probDict[s]['L'][5] = 0
                    if [x + 1, y - 1] not in terminals:
                        neighbour[s].append((x + 1, y - 1))
                else:
                    probDict[s]['L'][4] = 0
                    probDict[s]['L'][5] = 0.5 * (1 - prob)

            elif action == 'R':
                if y + 1 < grid_size and [x, y + 1] not in walls:
                    probDict[s]['R'][0] = prob
                    probDict[s]['R'][1] = 0
                    if [x, y + 1] not in terminals:
                        neighbour[s].append((x, y + 1))
                else:
                    probDict[s]['R'][0] = 0
                    probDict[s]['R'][1] = prob
                if x - 1 >= 0 and y + 1 < grid_size and [x - 1, y + 1] not in walls:
                    probDict[s]['R'][2] = 0.5 * (1 - prob)
                    probDict[s]['R'][3] = 0
                    if [x - 1, y + 1] not in terminals:
                        neighbour[s].append((x - 1, y + 1))
                else:
                    probDict[s]['R'][2] = 0
                    probDict[s]['R'][3] = 0.5 * (1 - prob)
                if x + 1 < grid_size and y + 1 < grid_size and [x + 1, y + 1] not in walls:
                    probDict[s]['R'][4] = 0.5 * (1 - prob)
                    probDict[s]['R'][5] = 0
                    if [x + 1, y + 1] not in terminals:
                        neighbour[s].append((x + 1, y + 1))
                else:
                    probDict[s]['R'][4] = 0
                    probDict[s]['R'][5] = 0.5 * (1 - prob)



def value_iteration(epsilon=0.0001):
    global states
    count = 0
    m = (1 - gamma) / gamma
    changedStates = set(states)
    diff = float("inf")
    while (diff > epsilon * m and len(changedStates) > 0):
        diff = 0
        count += 1

        states = list(changedStates)
        print len(states)
        changedStates = set()
        for s in states:
            x = s[0]
            y = s[1]
            util_max = float("-inf")
            l1 = probDict[s]['U']
            l2 = probDict[s]['D']
            l3 = probDict[s]['L']
            l4 = probDict[s]['R']
            sum1 = 0.0
            sum2 = 0.0
            sum3 = 0.0
            sum4 = 0.0

            if l1[0] != 0:
                sum1 = sum1 + l1[0] * grid[x - 1][y]
            else:
                sum1 = sum1 + l1[1] * grid[x][y]
            if l2[0] != 0:
                sum2 = sum2 + l2[0] * grid[x + 1][y]
            else:
                sum2 = sum2 + l2[1] * grid[x][y]
            if l3[0] != 0:
                sum3 = sum3 + l3[0] * grid[x][y - 1]
            else:
                sum3 = sum3 + l3[1] * grid[x][y]
            if l4[0] != 0:
                sum4 = sum4 + l4[0] * grid[x][y + 1]
            else:
                sum4 = sum4 + l4[1] * grid[x][y]
            if l1[2] != 0:
                sum1 = sum1 + l1[2] * grid[x - 1][y - 1]
            else:
                sum1 = sum1 + l1[3] * grid[x][y]
            if l2[2] != 0:
                sum2 = sum2 + l2[2] * grid[x + 1][y - 1]
            else:
                sum2 = sum2 + l2[3] * grid[x][y]
            if l3[2] != 0:
                sum3 = sum3 + l3[2] * grid[x - 1][y - 1]
            else:
                sum3 = sum3 + l3[3] * grid[x][y]
            if l4[2] != 0:
                sum4 = sum4 + l4[2] * grid[x - 1][y + 1]
            else:
                sum4 = sum4 + l4[3] * grid[x][y]

            if l1[4] != 0:
                sum1 = sum1 + l1[4] * grid[x - 1][y + 1]
            else:
                sum1 = sum1 + l1[5] * grid[x][y]
            if l2[4] != 0:
                sum2 = sum2 + l2[4] * grid[x + 1][y + 1]
            else:
                sum2 = sum2 + l2[5] * grid[x][y]
            if l3[4] != 0:
                sum3 = sum3 + l3[4] * grid[x + 1][y - 1]
            else:
                sum3 = sum3 + l3[5] * grid[x][y]
            if l4[4] != 0:
                sum4 = sum4 + l4[4] * grid[x + 1][y + 1]
            else:
                sum4 = sum4 + l4[5] * grid[x][y]

            sum1 = Rp + (gamma) * sum1
            sum2 = Rp + (gamma) * sum2
            sum3 = Rp + (gamma) * sum3
            sum4 = Rp + (gamma) * sum4
            if sum1 > util_max:
                util_max = sum1
                optimal_path[x][y] = 'U'

            if sum2 > util_max:
                util_max = sum2
                optimal_path[x][y] = 'D'

            if sum3 > util_max:
                util_max = sum3
                optimal_path[x][y] = 'L'

            if sum4 > util_max:
                util_max = sum4
                optimal_path[x][y] = 'R'

            if grid[x][y] < util_max:
                diff = max(diff, abs(util_max - grid[x][y]))
                grid[x][y] = util_max
                changedStates.add((x, y))
                for (n1, n2) in neighbour[(x, y)]:
                    changedStates.add((n1, n2))
        # print(grid)
        # if(diff <= epsilon*m or len(states)==0):
        #   break
    print(count)


def writeToFile():
    with open("output.txt", 'w') as outputFile:
        for i in range(grid_size):
            for j in range(grid_size):
                outputFile.write(optimal_path[i][j])
                if (j < grid_size - 1):
                    outputFile.write(",")
            if (i < grid_size - 1):
                outputFile.write("\n")


def main():
    file_name = "input4.txt"
    read_input(file_name)
    preprocessProb()
    sec1 = time.time()
    print(sec1 - sec)
    value_iteration()
    sec1 = time.time()
    print(sec1 - sec)
    writeToFile()


if __name__ == "__main__":
    main()
