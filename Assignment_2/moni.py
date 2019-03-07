# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:54:38 2019

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:55:11 2019

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 04:06:14 2019

@author: User
"""
import copy
import time
from collections import defaultdict

planeList=[]
setList=[] #used as a queue
minutes=1000
number_landing_runways=[]
number_gates=[]
number_takeoff_runways=[]
LGT=[]
flights_for_assignment=[]

class Plane:
    def __init__(self,I,R,M,S,O,C):
        self.index=I
        self.R=R
        self.M=M
        self.S=S
        self.O=O
        self.C=C
        self.landing=[]
        self.takeoff=[]
        self.land_updated=True
        self.takeoff_updated=True
        self.schedule=[]
        self.landing_to_takeoff=defaultdict(list)
    
    def __eq__(self, other):
        return self.R == other.R and \
               self.M == other.M and \
               self.S == other.S and \
               self.O == other.O and \
               self.C == other.C and\
               self.index==other.index

    def __hash__(self):
        return hash((self.R, self.M, self.S, self.O,self.C,self.index))


def read_input():
    file = open(r"input3.txt")
    s=file.readline()
    arr=s.split()
    global LGT
    global planeList
    for i in range(len(arr)):
        LGT.append(int(arr[i]))
    
    n_planes=int(file.readline())
    planeList=[]
    
    for i in range(n_planes):
        var=file.readline()
        R,M,S,O,C=var.split()
        planeList.append(Plane(i,int(R),int(M),int(S),int(O),int(C)))

def initialize_arrays():
    global number_landing_runways
    global number_gates
    global number_takeoff_runways
    global flights_for_assignment
    flights_for_assignment=[]
    number_landing_runways = [LGT[0]] * minutes
    number_gates = [LGT[1]] * minutes
    number_takeoff_runways = [LGT[2]] * minutes

def find_availability_lr(begin, end):
    for i in range(begin, end, 1):
        if number_landing_runways[i] <= 0:
            return False
    return True


def find_availability_gates(begin, end):
    for i in range(begin, end, 1):
        if number_gates[i] <= 0:
            return False
    return True


def find_availability_tr(begin, end):
    for i in range(begin, end, 1):
        if number_takeoff_runways[i] <= 0:
            return False
    return True


# mark busy
def mark_lr_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_landing_runways[i] -= 1


def mark_gates_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_gates[i] -= 1


def mark_tr_as_busy(begin, end):
    for i in range(begin, end, 1):
        number_takeoff_runways[i] -= 1

#free resources
def free_lr(begin, end):
    for i in range(begin, end, 1):
        number_landing_runways[i] += 1


def free_gates(begin, end):
    for i in range(begin, end, 1):
        number_gates[i] += 1


def free_tr(begin, end):
    for i in range(begin, end, 1):
        number_takeoff_runways[i] += 1

def find_corresponding_takeoff_times(plane, land_time):
    possible_takeoff = []
    for val in plane.takeoff:
        if land_time + plane.M + plane.S <= val <= land_time + plane.M + plane.C:
            possible_takeoff.append(val)
#    possible_takeoff=plane.landing_to_takeoff[land_time]
    return possible_takeoff


def change_and_check_landing_domain_for_one_plane(plane, time):
    for val in plane.landing:
        if val <= time <val + plane.M:
            plane.landing.remove(val)
            
    if len(plane.landing) == 0:
        return True
    return False


def change_and_check_takeoff_domain_for_one_plane(plane, time):
    for val in plane.takeoff:
        if val <= time < val + plane.O:
            plane.takeoff.remove(val)
            
    if len(plane.takeoff) == 0:
        return True
    return False

def change_and_check_gate_domain_for_one_plane(plane, time):
    for val in plane.landing:
        if val + plane.M <= time < val + plane.M + plane.S:
            plane.landing.remove(val)
    if len(plane.landing) == 0:
        return True
    return False

def change_landing_domains_for_other_planes(planes):
    for i in range(minutes):
        if number_landing_runways[i] == 0:
            for plane in planes:
                if change_and_check_landing_domain_for_one_plane(plane,i):
                    return True  # indicates empty
    return False


def change_gate_domains_for_other_planes(planes):
    for i in range(minutes):
        if number_gates[i] == 0:
            for plane in planes:
                if change_and_check_gate_domain_for_one_plane(plane, i):
                    return True  # indicates empty
    return False

def change_takeoff_domains_for_other_planes(planes):
    for i in range(minutes):
        if number_takeoff_runways[i] == 0:
            for plane in planes:
                if change_and_check_takeoff_domain_for_one_plane(plane, i):
                    return True  # indicates empty
    return False

def create_exhaustive_domain():
    global planeList
    for plane in planeList:
        for i in range(plane.R+1):
            plane.landing.append(i)
        for i in range(plane.M+plane.S,plane.R+plane.M+plane.C+1,1):
            plane.takeoff.append(i)

def map_landing_to_takeoff():
    for plane in planeList:
        for val in plane.landing:
            for take_val in plane.takeoff:
                if val+plane.M+plane.S<=take_val<=val+plane.M+plane.C and plane.landing_to_takeoff[val].count(take_val)==0:
                      plane.landing_to_takeoff[val].append(take_val)

def most_constrained_variable(flightList):
    constrained_variable = sorted(flightList, key=lambda f: len(f.landing))
    return constrained_variable
 
def getOverlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))           

def arrange_in_order_LCV(plane,constrained_variable):
    dictionary1={}
    for j in range(len(plane.landing)):
        count=0
        intrvl1=[plane.landing[j],plane.landing[j]+plane.M]
        for k in range(len(constrained_variable)):
            if constrained_variable[k].index!=plane.index:
                for l in range(len(constrained_variable[k].landing)):
                    intrvl2=[constrained_variable[k].landing[l],constrained_variable[k].landing[l]+constrained_variable[k].M]
                    if getOverlap(intrvl1,intrvl2)>0:
                        count+=1
                        break
       
        dictionary1[plane.landing[j]]=count
    return sorted(dictionary1)

def assigning_flight_schedule(unassigned_flights):
    if (len(unassigned_flights) == 0):
        print("DONE")
        f2 = open("output.txt", "w")
        str2 = ""
        for f in flights_for_assignment:
            str2 += str(f.schedule[1]) + " " + str(f.schedule[2]) + "\n"
        f2.write(str2)
        return True
    original_unassignment = copy.deepcopy(unassigned_flights)
    unassigned = unassigned_flights[0]
    unassigned.landing = copy.deepcopy(arrange_in_order_LCV(unassigned, unassigned_flights))
    
    for val in unassigned.landing:
        is_scheduled=False
        if find_availability_lr(val, val + unassigned.M):
            possible_takeoffs = find_corresponding_takeoff_times(unassigned, val)
            if len(possible_takeoffs) > 0:
                for pt in possible_takeoffs:
                    if find_availability_gates(val + unassigned.M, pt) and find_availability_tr(pt,pt + unassigned.O):
                        mark_lr_as_busy(val, val + unassigned.M)
                        mark_gates_as_busy(val + unassigned.M, pt)
                        mark_tr_as_busy(pt, pt + unassigned.O)
                        unassigned.schedule = [True, val, pt]
                        is_scheduled=True

                        for original in flights_for_assignment:
                            if original.index == unassigned.index:
                                original.schedule = copy.deepcopy([True, val, pt])

                        unassigned_flights.remove(unassigned)

                        if change_landing_domains_for_other_planes(unassigned_flights) or change_gate_domains_for_other_planes(unassigned_flights) or change_takeoff_domains_for_other_planes(unassigned_flights):
                            #unschedule_flight(unassigned)
                            if is_scheduled:
                                is_scheduled=False
                                unschedule_flight(unassigned)
                            unassigned_flights=copy.deepcopy(original_unassignment)
                            continue

                        unassigned_flights = most_constrained_variable(unassigned_flights)
                        result = assigning_flight_schedule(unassigned_flights)
                        if not result:
                            is_scheduled=False
                            unschedule_flight(unassigned)
                            for original in flights_for_assignment:
                                if original.index == unassigned.index:
                                    original.schedule = copy.deepcopy([False, -1, -1])
                            unassigned_flights= copy.deepcopy(original_unassignment)

                        if result:
                            return True
                # undo landing
                #free_lr(val,val+unassigned.M)
                if is_scheduled:
                    unschedule_flight(unassigned)
                unassigned_flights=copy.deepcopy(original_unassignment)

    return False   

def unschedule_flight(plane):
    
    if plane.schedule[0]:
        landing_start_time = plane.schedule[1]
        service_end_time = plane.schedule[2]
        
        free_lr(landing_start_time,landing_start_time+plane.M)
        free_gates(landing_start_time+plane.M,service_end_time)
        free_tr(service_end_time,service_end_time+plane.O)

    plane.schedule = [False, -1,-1]

    for og in flights_for_assignment:
        if og.index == plane.index:
            og.schedule = copy.deepcopy([False, -1,-1])

def driver():
    global flights_for_assignment
    global planeList
    start_time=time.time()
    read_input()
    initialize_arrays()
    create_exhaustive_domain()
    #map_landing_to_takeoff()

#    for plane in planeList:
#        print("landing times for plane ",plane.index," : ",plane.landing)
#        print("takeoff times for plane ",plane.index," : ",plane.takeoff)
#        print("mapping for plane",plane.index," : ",plane.landing_to_takeoff)
    
    flights_for_assignment = copy.deepcopy(planeList)
    planeList=most_constrained_variable(planeList)
    for plane in planeList:
        plane.landing=copy.deepcopy(arrange_in_order_LCV(plane,planeList))
    
    assigning_flight_schedule(planeList)
    
    final_time=time.time()
    print("total time:",final_time-start_time)

if __name__ == '__main__':
    driver()