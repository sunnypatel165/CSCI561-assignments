import itertools
import time
from multiprocessing import Queue

from copy import deepcopy

debug = True
minutes = 300


class Flight:

    def _init_(self, id, max_air_time, landing_time, minimum_service_time, takeoff_time, maximum_service_time):
        self.id = "P" + str(id)
        self.dom_air_time = []
        self.dom_service_time = []
        self.assignment = []
        self.new_land_domain = []
        self.new_takeoff_domain = []
        self.max_air_time = max_air_time
        self.landing_time = landing_time
        self.minimum_service_time = minimum_service_time
        self.takeoff_time = takeoff_time
        self.maximum_service_time = maximum_service_time
        self.update_dom_air_time()
        self.update_dom_service_time()
        self.l_set = set()
        self.t_set = set()

    def print_flight(self):
        dprint(self.id + " " +
               str(self.max_air_time) + " " +
               str(self.landing_time) + " " +
               str(self.minimum_service_time) + " " +
               str(self.takeoff_time) + " " +
               str(self.maximum_service_time) + " " +
               # str(self.dom_air_time) + " " +
               # str(self.dom_service_time) + " " +
               # str(self.new_land_domain) + " " +
               # str(self.new_takeoff_domain) + " " +
               str(self.l_set) + " " +
               str(self.t_set) + " " +
               str(self.assignment))

    def print_assignment(self):
        print(self.id +
              " assigned " + str(self.assignment[0]) +
              " Lands " + str(self.assignment[1]) +
              " Takes off " + str(self.assignment[2]))

    def update_dom_air_time(self):
        for i in range(0, self.max_air_time + 1, 1):
            self.dom_air_time.append(i)

    def update_dom_service_time(self):
        for i in range(self.minimum_service_time, self.maximum_service_time + 1, 1):
            self.dom_service_time.append(i)

    def reset_flight(self):
        self.assignment = []

    def _eq_(self, other):
        return self.max_air_time == other.max_air_time and \
               self.landing_time == other.landing_time and \
               self.minimum_service_time == other.minimum_service_time and \
               self.takeoff_time == other.takeoff_time and \
               self.maximum_service_time == other.maximum_service_time

    def _hash_(self):
        return hash((self.max_air_time, self.landing_time, self.minimum_service_time, self.takeoff_time,
                     self.maximum_service_time))


def print_flights(flights):
    if not debug:
        return
    for i in flights:
        i.print_flight()


def reset_flights(flights):
    for i in flights:
        i.reset_flight()


def print_flights_assignments(flights):
    if not debug:
        return
    for i in flights:
        i.print_assignment()


if debug == True:
    def dprint(line):
        if debug == True:
            print line
else:
    def dprint(line):
        return


def read_file():
    f1 = open("input0.txt", "r")
    line = f1.readline().s…
Slept late .. coming in 1 hour
Np
Chala kya?
Kuch
Nhi yr backtracking m error tha
Ok😔😔
Tera fast hua backtracking m change karke
[0]
[0, 10, 20]
[0, 10, 20, 30, 40, 50, 60]
[0, 10, 20, 30, 40, 50, 60, 70, 80]
[60, 65, 70, 75, 80]
[60, 65, 70, 75, 80, 85, 90, 95, 100]
[80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145]
[40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170]
def update_plane_l_domains():
    for p in p_list:
        p.l_set.add(0)
        p.l_set.add(p.r)

    landing_queue = list()

    landing_queue.append(p_list[0])
    while len(landing_queue) > 0:
        plane = landing_queue[0]
        del landing_queue[0]
        l_set = plane.l_set
        for l in l_set:
            for plane_in in p_list:
                if plane == plane_in:
                    continue
                else:
                    if l + plane.m >= max(plane_in.l_set) or l + plane.m <= min(plane_in.l_set):
                        continue
                    else:
                        if l + plane.m in plane_in.l_set:
                            continue
                        else:
                            plane_in.l_set.add(l + plane.m)
                            if plane_in not in landing_queue:
                                landing_queue.append(plane_in)
            for plane_in in p_list:
                if plane == plane_in:
                    continue
                else:
                    if l - plane_in.m >= max(plane_in.l_set) or l - plane_in.m <= min(plane_in.l_set):
                        continue
                    else:
                        if l - plane_in.m in plane_in.l_set:
                            continue
                        else:
                            plane_in.l_set.add(l - plane_in.m)
                            if plane_in not in landing_queue:

                                landing_queue.append(plane_in)


def update_plane_t_domains():
    for p in p_list:
        p.t_set.add(p.m + p.s)
        p.t_set.add(p.r + p.m + p.c)

    take_off_queue = list()
    take_off_queue.append(p_list[0])
    while len(take_off_queue) > 0:
        plane = take_off_queue[0]
        del take_off_queue[0]
        t_set = plane.t_set
        for t in t_set:
            for plane_in in p_list:
                if plane == plane_in:
                    continue
                else:
                    if t + plane.o >= max(plane_in.t_set) or t + plane.o <= min(plane_in.t_set):
                        continue
                    else:
                        if t + plane.o in plane_in.t_set:
                            continue
                        else:
                            plane_in.t_set.add(t + plane.o)
                            if plane_in not in take_off_queue:
                                take_off_queue.append(plane_in)
            for plane_in in p_list:
                if plane == plane_in:
                    continue
                else:
                    if t - plane_in.o >= max(plane_in.t_set) or t - plane_in.o <= min(plane_in.t_set):
                        continue
                    else:
                        if t - plane_in.o in plane_in.t_set:
                            continue
                        else:
                            plane_in.t_set.add(t - plane_in.o)
                            if plane_in not in take_off_queue:
                                take_off_queue.append(plane_in)


def update_t_to_l():
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(p_list[0])
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        t_set = plane.t_set
        is_updated = False
        for t in t_set:
            max_val = t - plane.c - plane.m
            min_val = t - plane.s - plane.m
            if 0 < min_val < max(plane.l_set):
                if min_val not in plane.l_set:
                    plane.l_set.add(min_val)
                    is_updated = True
            if 0 < max_val < max(plane.l_set):
                if max_val not in plane.l_set:
                    plane.l_set.add(max_val)
                    is_updated = True

        if is_updated is True:
            landing_queue = list()
            landing_queue.append(plane)
            while len(landing_queue) > 0:
                plane = landing_queue[0]
                del landing_queue[0]
                l_set = plane.l_set
                for l in l_set:
                    for plane_in in p_list:
                        if plane == plane_in:
                            continue
                        else:
                            if l + plane.m >= max(plane_in.l_set) or l + plane.m <= min(plane_in.l_set):
                                continue
                            else:
                                if l + plane.m in plane_in.l_set:
                                    continue
                                else:
                                    plane_in.l_set.add(l + plane.m)
                                    if plane_in not in landing_queue:
                                        landing_queue.append(plane_in)


def update_l_to_t():
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(p_list[0])
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        l_set = plane.l_set
        is_updated = False
        for l in l_set:
            min_val = l + plane.m + plane.s
            max_val = l + plane.m + plane.c
            if min_val > 0 and min(plane.t_set) < min_val < max(plane.t_set):
                if min_val not in plane.t_set:
                    plane.t_set.add(min_val)
                    is_updated = True
            if max_val > 0 and min(plane.t_set) < max_val < max(plane.t_set):
                if max_val not in plane.t_set:
                    plane.t_set.add(max_val)
                    is_updated = True

        if is_updated is True:
            take_off_queue = list()
            take_off_queue.append(plane)
            while len(take_off_queue) > 0:
                plane = take_off_queue[0]
                del take_off_queue[0]
                t_set = plane.t_set
                for t in t_set:
                    for plane_in in p_list:
                        if plane == plane_in:
                            continue
                        else:
                            if t + plane.o >= max(plane_in.t_set) or t + plane.o <= min(plane_in.t_set):
                                continue
                            else:
                                if t + plane.o in plane_in.t_set:
                                    continue
                                else:
                                    plane_in.t_set.add(t + plane.o)
                                    if plane_in not in take_off_queue:
                                        take_off_queue.append(plane_in)

