# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 07:54:27 2019

@author: User
"""
from sortedcontainers import SortedSet
import final_code_old
import final_version


planeList=[]
solutionSet=[]
number_landing_runways=[]
number_gates=[]
number_takeOff_runway=[]
LGT=[]
minutes=1000

class Plane:
    def __init__(self,I,R,M,S,O,C):
        self.index=I
        self.R=R
        self.M=M
        self.S=S
        self.O=O
        self.C=C
        self.landing=SortedSet([0,R])
        self.takeOff=SortedSet([M+S,R+M+C])
        self.land_updated=True
        self.takeOff_updated=True
        self.schedule=[]

def read_input_file(input_file):
    file = open(input_file,"r")
    s=file.readline()
    arr=s.split()
    global LGT
    for i in range(len(arr)):
        LGT.append(int(arr[i]))
    
    n_planes=int(file.readline())
    
    global planeList
    
    for i in range(n_planes):
        var=file.readline()
        R,M,S,O,C=var.split()
        planeList.append(Plane(i,int(R),int(M),int(S),int(O),int(C)))

def read_output_file():
    file = open(r"output.txt")
    global planeList
    n_planes=len(planeList)
    global solutionSet
    global solutionSet
    global number_landing_runways
    global number_gates
    global number_takeOff_runway
    global LGT
    global minutes
    planeList = []
    solutionSet = []
    number_landing_runways = []
    number_gates = []
    number_takeOff_runway = []
    minutes = 1000
    
    for i in range(n_planes):
        var=file.readline()
        if len(var)!=0:
            str = var.split()
            land = str[0]
            takeOff  = str[1]
            temp=[]
            temp.append(int(land))
            temp.append(int(takeOff))
            solutionSet.append(temp)

def initialize_arrays():
    global number_landing_runways
    global number_gates
    global number_takeoff_runways
    number_landing_runways = [LGT[0]] * minutes
    number_gates = [LGT[1]] * minutes
    number_takeoff_runways = [LGT[2]] * minutes
    
def mark_lr_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_landing_runways[i] -= 1


def mark_gates_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_gates[i] -= 1


def mark_tr_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_takeoff_runways[i] -= 1


def verify_solution():
    n=len(planeList)
    for i in range(n):
        mark_lr_as_busy(solutionSet[i][0],solutionSet[i][0]+planeList[i].M)
        mark_gates_as_busy(solutionSet[i][0]+planeList[i].M,solutionSet[i][1])
        mark_tr_as_busy(solutionSet[i][1],solutionSet[i][1]+planeList[i].O)
    
    for i in range(minutes):
        if number_landing_runways[i]<0 or number_gates[i]<0 or number_takeoff_runways[i]<0:
            return False
    
    for i in range(n):
        if 0<=solutionSet[i][0]<=planeList[i].R and solutionSet[i][0]+planeList[i].M+planeList[i].S<=solutionSet[i][1]<=solutionSet[i][0]+planeList[i].M+planeList[i].C:
            continue
        else:
            return False
    return True

def main():
    for i in range(11):
        print("Testing for input file",i)
        input_file="input"+str(i)+".txt"
        with open(input_file) as f:
            with open("input.txt", "w") as f1:
                for line in f:
                    f1.write(line)
        final_version.main()
        
        read_input_file(input_file)
        read_output_file()
        initialize_arrays()
        
        print("INPUT FILE for this iteration")
        print("number of landing runways",LGT[0])
        print("number of gates",LGT[1])
        print("number of takeOff runways",LGT[2])
        print("-----set of N planes----")
        
        for plane in planeList:
            print(plane.R," ",plane.M," ",plane.S," ",plane.O," ",plane.C)
        if verify_solution():
            print("This is a valid assignment")
        else:
            print("This is an infeasible assignment")
        print("oitput for the given input")
        print(solutionSet)
    
    
if __name__=='__main__':
    main()