import array


def Get_input(inp):
    global planes, L, G, T, N, inf, max_time, o_L, o_G, o_T
    inf = float('inf')
    myFile = open(inp)
    data = myFile.readlines()

    numbers = data[0].split(" ")
    if numbers[0] != '' and numbers[1] != '' and numbers[2] != '':
        L = int(numbers[0])
        G = int(numbers[1])
        T = int(numbers[2])

    numbers = data[1].split(" ")
    if numbers[0] != '':
        N = int(numbers[0])

    planes = []

    for k in range(N):
        numbers = data[k+2].split(" ")
        for _ in range(len(numbers)):
            if numbers[_] != '':
                numbers[_] = int(numbers[_])
        planes.append(numbers)

    max_time = int(N * (max([row[1] for row in planes]) + max([row[3] for row in planes]) +
                        max([row[4] for row in planes])) / min(L, G, T))

    o_L = array.array('H', [0 for _ in range(max_time)])
    o_G = array.array('H', [0 for _ in range(max_time)])
    o_T = array.array('H', [0 for _ in range(max_time)])


def Get_output(out):
    global output
    myFile = open(out)
    data = myFile.readlines()

    output = []

    for k in range(N):
        numbers = data[k].split(" ")
        for _ in range(len(numbers)):
            if numbers[_] != '':
                numbers[_] = int(numbers[_])
        output.append(numbers)


def Show_Conflicts():
    for _ in range(N):
        if output[_][0] > planes[_][0]:
            print("violation R")

        if output[_][1] > output[_][0] + planes[_][1] + planes[_][4]:
            print("violation C")

        if output[_][1] < output[_][0] + planes[_][1] + planes[_][2]:
            print("violation S")

    for _ in range(max_time):
        if o_L[_] > L:
            print("violation_o_L")
        if o_G[_] > G:
            print("violation_o_G")
        if o_T[_] > T:
            print("violation_o_T")


def Compile_LGT_arrays():
    global maxindex
    for _ in range(N):
        offset = output[_][0]
        for i in range(planes[_][1]):
            o_L[i + offset] += 1

        offset = output[_][0] + planes[_][1]
        for i in range(offset, output[_][1]):
            o_G[i] += 1

        offset = output[_][1]
        for i in range(planes[_][3]):
            o_T[i + offset] += 1
            if i + offset > maxindex:
                maxindex = i + offset


def Build_Output():
    global maxindex
    output_arrays = list([[0 for _ in range(maxindex + 1)] for _ in range(N)])
    for i in range(N):
        offset = output[i][0]
        for _ in range(planes[i][1]):
            output_arrays[i][_ + offset] = 1

        offset = output[i][0] + planes[i][1]
        for _ in range(offset, output[i][1]):
            output_arrays[i][_] = 2

        offset = output[i][1]
        for _ in range(planes[i][3]):
            output_arrays[i][_ + offset] = 3

    file = open("BO.txt", "w")
    for i in range(N):
        for _ in range(maxindex):
            file.write(str(output_arrays[i][_]) + " ")
        file.write("\n")
    file.write("\n")


maxindex = 0
Get_input("input21.txt")
Get_output("output.txt")
Compile_LGT_arrays()
Show_Conflicts()
Build_Output()

file = open("LGT.txt", "w")
for _ in range(max_time):
    file.write(str(o_L[_]) + " ")
file.write("\n")
for _ in range(max_time):
    file.write(str(o_G[_]) + " ")
file.write("\n")
for _ in range(max_time):
    file.write(str(o_T[_]) + " ")
file.write("\n")

file.close()
