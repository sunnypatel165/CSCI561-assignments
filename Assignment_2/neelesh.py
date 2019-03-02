P1=Plane(30,54,33,56,153)
P2=Plane(103,33,23,13,143)
P3=Plane(100,13,8,21,128)
P4=Plane(76,43,84,13,204)
P5=Plane(163,22,72,2,192)
P6=Plane(140,40,111,29,231)
P7=Plane(50,15,5,21,125)
P8=Plane(41,2,107,59,227)
P9=Plane(68,5,31,51,151)
P10=Plane(86,16,38,38,158)
P11=Plane(7,59,89,59,209)
P12=Plane(49,13,27,58,147)
P13=Plane(107,31,72,4,192)
P14=Plane(75,4,91,25,211)
P15=Plane(155,30,74,48,194)
P16=Plane(59,9,59,27,179)
P17=Plane(45,12,115,49,235)
P18=Plane(120,46,85,11,205)
P19=Plane(85,18,77,26,197)
P20=Plane(41,58,91,37,211)
P21=Plane(32,56,82,36,202)
P22=Plane(13,5,85,8,205)
P23=Plane(72,10,45,59,165)
P24=Plane(98,50,76,58,196)
P25=Plane(120,21,36,25,156)
from multiprocessing import Queue
import time

L = 1
G = 2
T = 1


class Plane:

    def _init_(self, r, m, s, o, c):
        self.r = r
        self.m = m
        self.s = s
        self.o = o
        self.c = c
        self.l_set = set()
        self.t_set = set()

    def _eq_(self, other):
        return self.r == other.r and self.m == other.m and self.s == other.s and self.o == other.o and self.c == other.c

    def _hash_(self):
        return hash((self.r, self.m, self.s, self.o, self.c))


p1=Plane(30,54,33,56,153)
p2=Plane(103,33,23,13,143)
p3=Plane(100,13,8,21,128)
p4=Plane(76,43,84,13,204)
p5=Plane(163,22,72,2,192)
p6=Plane(140,40,111,29,231)
p7=Plane(50,15,5,21,125)
p8=Plane(41,2,107,59,227)
p9=Plane(68,5,31,51,151)
p10=Plane(86,16,38,38,158)
p11=Plane(7,59,89,59,209)
p12=Plane(49,13,27,58,147)
p13=Plane(107,31,72,4,192)
p14=Plane(75,4,91,25,211)
p15=Plane(155,30,74,48,194)
p16=Plane(59,9,59,27,179)
p17=Plane(45,12,115,49,235)
p18=Plane(120,46,85,11,205)
p19=Plane(85,18,77,26,197)
p20=Plane(41,58,91,37,211)
p21=Plane(32,56,82,36,202)
p22=Plane(13,5,85,8,205)
p23=Plane(72,10,45,59,165)
p24=Plane(98,50,76,58,196)
p25=Plane(120,21,36,25,156)

p_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25]


def update_plane_l_domains():
    for p in p_list:
        p.l_set.add(0)
        p.l_set.add(p.r)

    landing_queue = list()

    landing_queue.append(p1)
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



def update_plane_t_domains():

    for plane in p_list:
        plane.t_set.add(plane.m + plane.s)
        plane.t_set.add(plane.r + plane.m + plane.c)

    take_off_queue = list()

    take_off_queue.append(p1)
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


def update_t_to_l():
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(p1)
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        t_set = plane.t_set
        is_updated = False
        for t in t_set:
            max_val = t - plane.c - plane.m
            min_val = t - plane.s - plane.m
            if min_val > 0 and min_val < max(plane.l_set):
                if min_val not in plane.l_set:
                    plane.l_set.add(min_val)
                    is_updated = True
            if max_val > 0 and max_val < max(plane.l_set):
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
    take_off_to_landing_queue.append(p1)
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        l_set = plane.l_set
        is_updated = False
        for l in l_set:
            min_val = l + plane.m + plane.s
            max_val = l + plane.m + plane.c
            if min_val > 0 and min_val > min(plane.t_set) and min_val < max(plane.t_set):
                if min_val not in plane.t_set:
                    plane.t_set.add(min_val)
                    is_updated = True
            if max_val > 0 and max_val > min(plane.t_set) and max_val < max(plane.t_set):
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

    for plane in p_list:
        print sorted(plane.l_set)
    for plane in p_list:
        print sorted(plane.t_set)


def get_least_constrained_l(plane, most_constrained_l_list):
    l_list = plane.l_set
    max_val = 4
    assign_val = min(l_list)
    for val in l_list:
        count = 0
        for size, plane_i in most_constrained_l_list.iteritems():
            if plane == plane_i:
                continue
            p_l_list = plane_i.l_set
            for item in p_l_list:
                if item == val:
                    count = count + 1
            if count < max_val:
                max_val = count
                assign_val = val
    return assign_val


def get_least_constrained_t(plane, most_constrained_t_list):
    t_list = plane.t_set
    max_val = 4
    assign_val = min(t_list)
    for val in t_list:
        count = 0
        for size, plane_i in most_constrained_t_list.iteritems():
            if plane == plane_i:
                continue
            p_t_list = plane_i.t_set
            for item in p_t_list:
                if item == val:
                    count = count + 1
            if count < max_val:
                max_val = count
                assign_val = val
    return assign_val


def backtrack_and_assign():
    most_constrained_l_list = {}
    most_constrained_t_list = {}
    for plane in p_list:
        most_constrained_l_list[len(plane.l_set)] = plane
        most_constrained_t_list[len(plane.t_set)] = plane

    most_constrained_l_list = dict(sorted(most_constrained_l_list.items()))
    most_constrained_t_list = dict(sorted(most_constrained_t_list.items()))

    print most_constrained_l_list

    for size, plane in most_constrained_l_list.iteritems():
        least_constrained_val = get_least_constrained_l(plane, most_constrained_l_list)
        # above value will give you the least constrained value for the given plane in Landing Sets

    for size, plane in most_constrained_t_list.iteritems():
        least_constrained_val = get_least_constrained_t(plane, most_constrained_t_list)
        # above value will give you the least constrained value for the given plane in Takeoff Sets


time1 = time.time()
update_plane_l_domains()
print "update l done"
for plane in p_list:
    print sorted(plane.l_set)

update_plane_t_domains()
print "update t done"
for plane in p_list:
    print sorted(plane.t_set)
update_l_to_t()
print "update l to t done"
update_t_to_l()
print " update t to l done"
time2 = time.time()
print time2 - time1
# backtrack_and_assign()