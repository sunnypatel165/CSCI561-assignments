import itertools
import time
from multiprocessing import Queue

from copy import deepcopy

debug = True
minutes = 1000


class Flight:

    def __init__(self, id, max_air_time, landing_time, minimum_service_time, takeoff_time, maximum_service_time):
        self.id = "P" + str(id)
        self.dom_air_time = []
        self.dom_service_time = []
        self.assignment = []
        self.new_land_domain =[]
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
               str(self.new_land_domain) + " " +
               str(self.new_takeoff_domain) + " " +
               # str(self.l_set) + " " +
               # str(self.t_set) + " " +
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

    def __eq__(self, other):
        return self.max_air_time == other.max_air_time and \
               self.landing_time == other.landing_time and \
               self.minimum_service_time == other.minimum_service_time and \
               self.takeoff_time == other.takeoff_time and \
               self.maximum_service_time == other.maximum_service_time

    def __hash__(self):
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


def print_flights_ids(flights):
    if not debug:
        return
    st = ""
    for i in flights:
        st = st + i.id + " "
    dprint(st)


if debug == True:
    def dprint(line):
        if debug == True:
            print line
else:
    def dprint(line):
        return


def read_file():
    f1 = open("input3.txt", "r")
    line = f1.readline().strip().split()
    landing, gates, takingoff = int(line[0]), int(line[1]), int(line[2])
    n = int(f1.readline())
    flights = []
    for i in xrange(n):
        line = f1.readline().strip().split()
        flight = Flight(i, int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))
        flights.append(flight)
    print_flights(flights)
    return landing, gates, takingoff, flights


landing_runways_available = []
gates_available = []
takeoff_runways_available = []


def initialise_time(landing, gates, takeoff):
    global landing_runways_available
    global gates_available
    global takeoff_runways_available
    landing_runways_available = [landing] * minutes
    gates_available = [gates] * minutes
    takeoff_runways_available = [takeoff] * minutes

    # return landing_runway, gates, takeoff_runway


# check availablity
def check_landing_runway_available(start, end):
    for i in range(start, end + 1, 1):
        if landing_runways_available[i] <= 0:
            return False
    return True


def check_gates_available(start, end):
    for i in range(start, end + 1, 1):
        if gates_available[i] <= 0:
            return False
    return True


def check_takeoff_runways_available(start, end):
    for i in range(start, end + 1, 1):
        if takeoff_runways_available[i] <= 0:
            return False
    return True


# mark busy
def mark_landing_runway_busy(start, end):
    for i in range(start, end, 1):
        landing_runways_available[i] = landing_runways_available[i] - 1


def mark_gates_busy(start, end):
    for i in range(start, end, 1):
        gates_available[i] = gates_available[i] - 1


def mark_takeoff_runways_busy(start, end):
    for i in range(start, end, 1):
        takeoff_runways_available[i] = takeoff_runways_available[i] - 1


def schedule_single_flight_backtrack(flight):
    return schedule_landing(flight)


def find_eligible_takeoff_times(flight, selected_landing):
    eligible = []
    for dom in flight.new_takeoff_domain:
        if selected_landing + flight.landing_time + flight.minimum_service_time <= dom <= selected_landing + flight.landing_time + flight.maximum_service_time:
            eligible.append(dom)
    return eligible


def update_domain_for_flight(flight, t):
    for dom in flight.new_land_domain:
        if dom <= t <= dom + flight.landing_time:
            flight.new_land_domain.remove(dom)
            # eligible = find_eligible_takeoff_times(flight, dom)
            # flight.new_takeoff_domain = set(flight.new_takeoff_domain) - set(eligible)

    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_takeoff_domain_for_flight(flight, t):
    for dom in flight.new_takeoff_domain:
        if dom <= t <= dom + flight.takeoff_time:
            flight.new_takeoff_domain.remove(dom)
            # eligible = find_eligible_takeoff_times(flight, dom)
            # flight.new_takeoff_domain = set(flight.new_takeoff_domain) - set(eligible)

    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_landing_domains_for_other_flights(flights):
    print("updating domain")
    for i in range(minutes):
        if landing_runways_available[i] == 0:
            for flight in flights:
                if update_domain_for_flight(flight, i):
                    return True  # indicates empty
    return False


def update_gate_domain_for_flight(flight, t):
    for dom in flight.new_land_domain:
        if dom + flight.landing_time <= t <= dom + flight.landing_time + flight.minimum_service_time:
            flight.new_land_domain.remove(dom)
    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_gate_domains_for_other_flights(flights):
    for i in range(minutes):
        if gates_available[i] == 0:
            for flight in flights:
                if update_gate_domain_for_flight(flight, i):
                    return True  # indicates empty
    return False

def update_takeoff_domains_for_other_flights(flights):
    print("updating take off domain")
    for i in range(minutes):
        if takeoff_runways_available[i] == 0:
            for flight in flights:
                if update_takeoff_domain_for_flight(flight, i):
                    return True  # indicates empty
    return False


def schedule_landing(flight, unscheduled):
    # For every possible value in the  domain of air time
    for dom in flight.new_land_domain:
        # dprint(flight.id + " Checking runway: " + str(dom) + " " + str(dom + flight.landing_time))
        if check_landing_runway_available(dom, dom + flight.landing_time):
            eligible = find_eligible_takeoff_times(flight, dom)
            dprint("Eligible takeoff times: " + str(eligible))
            if len(eligible) > 0:
                for e in eligible:
                    #           dprint(flight.id + " Checking gates: " + str(dom + flight.landing_time) + " " + str(e))
                    #          dprint(flight.id + " Checking takeo: " + str(e) + " " + str(e + flight.takeoff_time))
                    if check_gates_available(dom + flight.landing_time, e) and check_takeoff_runways_available(e,
                                                                                                               e + flight.takeoff_time):
                        mark_landing_runway_busy(dom, dom + flight.landing_time)
                        # if update_landing_domains_for_other_flights(unscheduled):
                        #     return [False, -1]

                        mark_gates_busy(dom + flight.landing_time, e)
                        # if update_gate_domains_for_other_flights(unscheduled):
                        #     return [False, -1]
                        mark_takeoff_runways_busy(e, e + flight.takeoff_time)
                        # if update_takeoff_domains_for_other_flights(unscheduled):
                        #     return [False, -1]

                        flight.assignment = [True, dom, e]
                        return [True, dom, e]
    return [False, -1]


def schedule_service(flight, chosen_landing_end_time):
    # For every possible domain of service time
    for dom in flight.dom_service_time:

        # dprint(flight.id + " Trying gate time: " + str(chosen_landing_end_time) + "  " + str(chosen_landing_end_time + dom))

        if check_gates_available(chosen_landing_end_time, chosen_landing_end_time + dom):
            chosen_service_end_time = chosen_landing_end_time + dom
            takeoff_possibility = schedule_takeoff(flight, chosen_service_end_time)

            if takeoff_possibility[0] and takeoff_possibility[1] != -1:
                mark_gates_busy(chosen_landing_end_time, chosen_landing_end_time + dom)
                return [True, chosen_service_end_time]

    return [False, -1]


def print_state():
    dprint("Landing: " + str(landing_runways_available))
    dprint("Gates  : " + str(gates_available))
    dprint("Takeoff: " + str(takeoff_runways_available))


def schedule_takeoff(flight, chosen_service_end_time):
    dprint(flight.id + " Trying takeoff time: " + str(chosen_service_end_time) + "  " + str(
        chosen_service_end_time + flight.takeoff_time))
    if check_takeoff_runways_available(chosen_service_end_time, chosen_service_end_time + flight.takeoff_time):
        chosen_takeoff_start_time = chosen_service_end_time

        mark_takeoff_runways_busy(chosen_takeoff_start_time, chosen_service_end_time + flight.takeoff_time)
        return [True, chosen_takeoff_start_time]
    return [False, -1]


def schedule2(landing, gates, takingoff, unscheduled):
    dprint("Trying to schedule:")
    print_flights_ids(unscheduled)
    if (len(unscheduled) == 0):
        dprint("DONE")
        return True
    copied = deepcopy(unscheduled)
    unsch = unscheduled[0]
    if unsch.id=='P24':
        print unsch.new_land_domain
        print unsch.new_takeoff_domain
    # For every possible value in the  domain of air time
    b = False
    unsch.new_land_domain = deepcopy(reorder_by_overlap(unsch, unscheduled))
    print unsch.new_land_domain
    for dom in unsch.new_land_domain:
        if b:
            break
        dprint(unsch.id + " Checking runway: " + str(dom) + " " + str(dom + unsch.landing_time))
        if check_landing_runway_available(dom, dom + unsch.landing_time):
            eligible = find_eligible_takeoff_times(unsch, dom)
            dprint("Eligible takeoff times: " + str(eligible))
            if len(eligible) > 0:
                for e in eligible:
                    dprint(unsch.id + " Checking gates: " + str(dom + unsch.landing_time) + " " + str(e))
                    dprint(unsch.id + " Checking takeo: " + str(e) + " " + str(e + unsch.takeoff_time))
                    if check_gates_available(dom + unsch.landing_time, e) and check_takeoff_runways_available(e,
                                                                                                              e + unsch.takeoff_time):
                        mark_landing_runway_busy(dom, dom + unsch.landing_time)

                        mark_gates_busy(dom + unsch.landing_time, e)
                        mark_takeoff_runways_busy(e, e + unsch.takeoff_time)
                        unsch.assignment = [True, dom, e]

                        unscheduled.remove(unsch)

                        if update_landing_domains_for_other_flights(unscheduled):
                            return False
                        if update_gate_domains_for_other_flights(unscheduled):
                            return False
                        if update_takeoff_domains_for_other_flights(unscheduled):
                            return False


                        unscheduled = sorted(unscheduled, key=lambda f: len(f.new_land_domain))
                        answer = schedule2(landing, gates, takingoff, unscheduled)
                        if not answer:
                            unschedule_flight(unsch)
                            mark_landing_runway_busy(dom, dom + unsch.landing_time)
                            # unscheduled.insert(0, unsch)
                            unscheduled = deepcopy(copied)

                        if answer:
                            dprint("done2")
                            return True
                # undo landing
                dprint("Tried all take off, undo landing")
                for i in range(dom, dom + unsch.landing_time):
                    landing_runways_available[i] = landing_runways_available[i] + 1

    return False


def schedule(landing, gates, takingoff, flights):
    dprint("inside")
    print_flights_ids(flights)
    unscheduled = deepcopy(flights)
    all_possible = True
    for unsch in unscheduled:
        schedule_found = schedule_single_flight_backtrack(unsch)
        dprint("trying to schedule " + unsch.id + str(schedule_found))
        if schedule_found[0]:
            unscheduled.remove(unsch)
            if len(unscheduled) == 0:
                dprint("YES")
                all_possible = True
                break
            if not schedule(landing, gates, takingoff, unscheduled):
                dprint("unscheduling=====")
                unschedule_flight(unsch)
                unscheduled.append(unsch)  # inserting at 0 will lead to infinite
                return False
                # schedule(unscheduled)
                # return False

            if not schedule_found[0]:
                dprint("NO")
                return False
    if all_possible:
        dprint("returning")
        return True


def unschedule_flight(flight):
    dprint("==========")
    print_state()
    dprint("Unscheduling: ")
    dprint(flight.print_flight())

    if flight.assignment[0]:
        chosen_landing_start_time = flight.assignment[1]
        for i in range(chosen_landing_start_time, chosen_landing_start_time + flight.landing_time):
            landing_runways_available[i] = landing_runways_available[i] + 1

        chosen_service_end_time = flight.assignment[2]
        for i in range(chosen_landing_start_time + flight.landing_time, chosen_service_end_time):
            gates_available[i] = gates_available[i] + 1

        for i in range(chosen_service_end_time, chosen_service_end_time + flight.takeoff_time):
            takeoff_runways_available[i] = takeoff_runways_available[i] + 1
    flight.assignment = [False, -1]

    for og in flights_for_assignment:
        if og.id == flight.id:
            dprint("assigining original")
            og.assignment = deepcopy([False, -1])
    print_state()
    dprint("==========")


#
# def schedule(landing, gates, takingoff, flights):
#     global flights_for_assignment
#     # dprint("Trying to schedule " + str(flights))
#     dprint("=============")
#     print_state()
#     # for sch in itertools.permutations(flights):
#     #     all_possible = True
#     for flight in flights:
#
#         all_possible = True
#         schedule_found = schedule_single_flight_backtrack(flight)
#         if not schedule_found[0]:
#             all_possible = False
#             reset_flights(flights)
#             initialise_time(landing, gates, takingoff)
#             break
#         else:
#             for original in flights_for_assignment:
#                 if original.id == flight.id:
#                     dprint("assigining original" + flight.id + str(schedule_found))
#                     original.assignment = deepcopy(schedule_found)
#
#     if all_possible:
#         dprint("all possible")
#         print_flights_assignments(flights)
#         if debug == False:
#             f2 = open("output.txt", "w")
#             str2 = ""
#             for flight in flights_for_assignment:
#                 str2 += str(flight.assignment[1]) + " " + str(flight.assignment[2]) + "\n"
#             f2.write(str2)
#         else:
#             for flight in flights_for_assignment:
#                 print str(flight.assignment[1]) + " " + str(flight.assignment[2])
#         break
# return True
def update_plane_l_domains():
    for p in p_list:
        p.l_set.add(0)
        p.l_set.add(p.max_air_time)

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
                    if l + plane.landing_time >= max(plane_in.l_set) or l + plane.landing_time <= min(plane_in.l_set):
                        continue
                    else:
                        if l + plane.landing_time in plane_in.l_set:
                            continue
                        else:
                            plane_in.l_set.add(l + plane.landing_time)
                            if plane_in not in landing_queue:
                                landing_queue.append(plane_in)
            # for plane_in in p_list:
            #     if plane == plane_in:
            #         continue
            #     else:
            #         if l - plane_in.landing_time >= max(plane_in.l_set) or l - plane_in.landing_time <= min(plane_in.l_set):
            #             continue
            #         else:
            #             if l - plane_in.landing_time in plane_in.l_set:
            #                 continue
            #             else:
            #                 plane_in.l_set.add(l - plane_in.landing_time)
            #                 if plane_in not in landing_queue:
            #
            #                     landing_queue.append(plane_in)


def update_plane_t_domains():
    for p in p_list:
        p.t_set.add(p.landing_time + p.minimum_service_time)
        p.t_set.add(p.max_air_time + p.landing_time + p.maximum_service_time)

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
                    if t + plane.takeoff_time >= max(plane_in.t_set) or t + plane.takeoff_time <= min(plane_in.t_set):
                        continue
                    else:
                        if t + plane.takeoff_time in plane_in.t_set:
                            continue
                        else:
                            plane_in.t_set.add(t + plane.takeoff_time)
                            if plane_in not in take_off_queue:
                                take_off_queue.append(plane_in)
            # for plane_in in p_list:
            #     if plane == plane_in:
            #         continue
            #     else:
            #         if t - plane_in.takeoff_time >= max(plane_in.t_set) or t - plane_in.takeoff_time <= min(plane_in.t_set):
            #             continue
            #         else:
            #             if t - plane_in.takeoff_time in plane_in.t_set:
            #                 continue
            #             else:
            #                 plane_in.t_set.add(t - plane_in.takeoff_time)
            #                 if plane_in not in take_off_queue:
            #                     take_off_queue.append(plane_in)


def update_t_to_l():
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(p_list[0])
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        t_set = plane.t_set
        is_updated = False
        for t in t_set:
            max_val = t - plane.maximum_service_time - plane.landing_time
            min_val = t - plane.minimum_service_time - plane.landing_time
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
                            if l + plane.landing_time >= max(plane_in.l_set) or l + plane.landing_time <= min(
                                    plane_in.l_set):
                                continue
                            else:
                                if l + plane.landing_time in plane_in.l_set:
                                    continue
                                else:
                                    plane_in.l_set.add(l + plane.landing_time)
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
            min_val = l + plane.landing_time + plane.minimum_service_time
            max_val = l + plane.landing_time + plane.maximum_service_time
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
                            if t + plane.takeoff_time >= max(plane_in.t_set) or t + plane.takeoff_time <= min(
                                    plane_in.t_set):
                                continue
                            else:
                                if t + plane.takeoff_time in plane_in.t_set:
                                    continue
                                else:
                                    plane_in.t_set.add(t + plane.takeoff_time)
                                    if plane_in not in take_off_queue:
                                        take_off_queue.append(plane_in)


flights_for_assignment = []
p_list = []


def overlap(x1, y1, x2, y2):
    # return max(0, min(b, d) - max(a, c))
    return max(x1, y1) <= min(x2, y2)


def reorder_by_overlap(flight, flights):
    map_const = {}
    land_domains = flight.new_land_domain
    for val in land_domains:
        count = 0
        for plane in flights:
            if plane == flight:
                continue
            else:
                plane_dom_list = plane.new_land_domain
                for item in plane_dom_list:
                    if overlap(item, item + plane.landing_time, val, val + flight.landing_time) != 0:
                        count = count + 1
                        break
        map_const[val] = count
    return sorted(map_const, reverse= True)


def main():
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)
    # print schedule_single_flight_backtrack(flights[0])
    # print_state()
    # print schedule_single_flight_backtrack(flights[1])
    # print_state()
    #
    global flights_for_assignment
    global p_list
    # flights[0].l_set = [0]
    # flights[1].l_set = [0, 10, 20]
    # flights[2].l_set = [0, 10, 20, 30, 40, 50, 60]
    # flights[3].l_set = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    #
    # flights[0].t_set = [60, 70, 80]
    # flights[1].t_set = [60, 70, 80, 90, 100]
    # flights[2].t_set = [80, 90, 100, 110, 120, 130, 140]
    # flights[3].t_set = [40, 80, 90, 100, 110, 120, 130, 140, 150, 160, 165, 170]

    p_list = deepcopy(flights)

    time2 = time.time()
    update_plane_l_domains()
    update_plane_t_domains()
    update_l_to_t()
    update_t_to_l()
    print time.time() - time2

    flights = deepcopy(p_list)
    print_flights(flights)
    for flight in flights:
        flight.new_takeoff_domain = deepcopy(flight.t_set)
        flight.new_takeoff_domain = sorted(flight.new_takeoff_domain)
        flight.new_land_domain = deepcopy(flight.l_set)
        flight.new_land_domain = sorted(flight.new_land_domain)
    flights = sorted(flights, key=lambda f: len(f.new_land_domain))
    dprint("===sorted===")
    print_flights(flights)
    # moves.sort(key=lambda move: check_move_value(grid, grid_size, move[0], move[1], player), reverse=True)

    for flight in flights:
        flight.new_land_domain = deepcopy(reorder_by_overlap(flight, flights))

    flights_for_assignment = deepcopy(flights)

    dprint("=============================================")

    dprint(schedule2(landing, gates, takingoff, flights))
    print_flights(flights)
    # print_flights_assignments(flights_for_assignment)

    # if debug == False:
    #     f2 = open("output.txt", "w")
    #     str2 = ""
    #     for flight in flights_for_assignment:
    #         str2 += str(flight.assignment[1]) + " " + str(flight.assignment[2]) + "\n"
    #     f2.write(str2)
    # else:
    #     for flight in flights_for_assignment:
    #         print str(flight.assignment[1]) + " " + str(flight.assignment[2])


if __name__ == '__main__':
    main()
