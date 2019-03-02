import itertools
import time
from multiprocessing import Queue

from copy import deepcopy

debug = True
minutes = 300


class Flight:

    def __init__(self, id, max_air_time, landing_time, minimum_service_time, takeoff_time, maximum_service_time):
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


def schedule_landing(flight):
    # For every possible value in the  domain of air time
    for dom in flight.new_land_domain:
        dprint(flight.id + " Checking runway: " + str(dom) + " " + str(dom + flight.landing_time))
        if check_landing_runway_available(dom, dom + flight.landing_time):
            eligible = find_eligible_takeoff_times(flight, dom)
            dprint("Eligible takeoff times: " + str(eligible))
            if len(eligible) > 0:
                for e in eligible:
                    dprint(flight.id + " Checking gates: " + str(dom + flight.landing_time) + " " + str(e))
                    dprint(flight.id + " Checking takeo: " + str(e) + " " + str(e + flight.takeoff_time))
                    if check_gates_available(dom + flight.landing_time, e) and check_takeoff_runways_available(e,
                                                                                                               e + flight.takeoff_time):
                        mark_landing_runway_busy(dom, dom + flight.landing_time)
                        mark_gates_busy(dom + flight.landing_time, e)
                        mark_takeoff_runways_busy(e, e + flight.takeoff_time)
                        flight.assignment = [True, dom, e]
                        return [True, dom, e]
    return [False, -1]

    #     dprint(flight.id + " Trying landing time: " + str(dom) + "  " + str(dom + flight.landing_time))
    #     if check_landing_runway_available(dom, dom + flight.landing_time):
    #         chosen_landing_start = dom
    #         chosen_landing_end = dom + flight.landing_time
    #         service_possibility = schedule_service(flight, chosen_landing_end)
    #
    #         if service_possibility[0] and service_possibility[1] != -1:
    #             mark_landing_runway_busy(dom, dom + flight.landing_time)
    #             answer = [True, chosen_landing_start, service_possibility[1]]
    #             flight.assignment = [True, chosen_landing_start, service_possibility[1]]
    #             return answer
    # answer = deepcopy([False, -1])
    # flight.assignment = [False, -1]
    # return answer


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


def schedule(landing, gates, takingoff, flights):
    global flights_for_assignment
    # dprint("Trying to schedule " + str(flights))
    dprint("=============")
    print_state()
    for sch in itertools.permutations(flights):
        all_possible = True
        for flight in sch:
            schedule_found = schedule_single_flight_backtrack(flight)
            if not schedule_found[0]:
                all_possible = False
                reset_flights(flights)
                initialise_time(landing, gates, takingoff)
                break
            else:
                for original in flights_for_assignment:
                    if original.id == flight.id:
                        dprint("assigining original" + flight.id + str(schedule_found))
                        original.assignment = deepcopy(schedule_found)

        if all_possible:
            dprint("all possible")
            print_flights_assignments(flights)
            if debug == False:
                f2 = open("output.txt", "w")
                str2 = ""
                for flight in flights_for_assignment:
                    str2 += str(flight.assignment[1]) + " " + str(flight.assignment[2]) + "\n"
                f2.write(str2)
            else:
                for flight in flights_for_assignment:
                    print str(flight.assignment[1]) + " " + str(flight.assignment[2])

            break
    return True


def update_plane_l_domains():
    for plane in p_list:
        plane.l_set.add(0)
        plane.l_set.add(plane.max_air_time)

    landing_queue = Queue()

    landing_queue.put(p_list[0])
    time.sleep(0.001)
    while not landing_queue.empty():
        plane = landing_queue.get()
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
                            landing_queue.put(plane_in)
                            time.sleep(0.001)


def update_plane_t_domains():
    for plane in p_list:
        plane.t_set.add(plane.landing_time + plane.minimum_service_time)
        plane.t_set.add(plane.max_air_time + plane.landing_time + plane.maximum_service_time)

    take_off_queue = Queue()

    take_off_queue.put(p_list[0])
    time.sleep(0.001)
    while not take_off_queue.empty():
        plane = take_off_queue.get()
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
                            take_off_queue.put(plane_in)
                            time.sleep(0.001)


def update_t_to_l():
    take_off_to_landing_queue = Queue()
    take_off_to_landing_queue.put(p_list[0])
    time.sleep(0.001)
    while not take_off_to_landing_queue.empty():
        plane = take_off_to_landing_queue.get()
        t_set = plane.t_set
        is_updated = False
        for t in t_set:
            max_val = t - plane.maximum_service_time - plane.landing_time
            min_val = t - plane.minimum_service_time - plane.landing_time
            if min_val > 0 and min_val < max(plane.l_set):
                if min_val not in plane.l_set:
                    plane.l_set.add(min_val)
                    is_updated = True
            if max_val > 0 and max_val < max(plane.l_set):
                if max_val not in plane.l_set:
                    plane.l_set.add(max_val)
                    is_updated = True

        if is_updated is True:
            landing_queue = Queue()
            landing_queue.put(plane)
            time.sleep(0.001)
            while landing_queue.qsize() > 0:
                plane = landing_queue.get()
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
                                    landing_queue.put(plane_in)
                                    time.sleep(0.001)


def update_l_to_t():
    take_off_to_landing_queue = Queue()
    take_off_to_landing_queue.put(p_list[0])
    time.sleep(0.001)
    while not take_off_to_landing_queue.empty():
        plane = take_off_to_landing_queue.get()
        l_set = plane.l_set
        is_updated = False
        for l in l_set:
            min_val = l + plane.landing_time + plane.minimum_service_time
            max_val = l + plane.landing_time + plane.maximum_service_time
            if min_val > 0 and min_val > min(plane.t_set) and min_val < max(plane.t_set):
                if min_val not in plane.t_set:
                    plane.t_set.add(min_val)
                    is_updated = True
            if max_val > 0 and max_val > min(plane.t_set) and max_val < max(plane.t_set):
                if max_val not in plane.t_set:
                    plane.t_set.add(max_val)
                    is_updated = True

        if is_updated is True:
            take_off_queue = Queue()
            take_off_queue.put(plane)
            time.sleep(0.001)
            while take_off_queue.qsize() > 0:
                plane = take_off_queue.get()
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
                                    take_off_queue.put(plane_in)
                                    time.sleep(0.001)

    for plane in p_list:
        dprint(sorted(plane.l_set))
    for plane in p_list:
        dprint(sorted(plane.t_set))


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


flights_for_assignment = []
p_list = []


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
    # flights[0].new_land_domain = [0]
    # flights[1].new_land_domain = [0, 10, 20]
    # flights[2].new_land_domain = [0, 10, 20, 30, 40, 50, 60]
    # flights[3].new_land_domain = [0, 10, 20, 30, 40, 50, 60, 70, 80]
    #
    # flights[0].new_takeoff_domain = [60, 70, 80]
    # flights[1].new_takeoff_domain = [60, 70, 80, 90, 100]
    # flights[2].new_takeoff_domain = [80, 90, 100, 110, 120, 130, 140]
    # flights[3].new_takeoff_domain = [40, 80, 90, 100, 110, 120, 130, 140, 150, 160, 165, 170]

    p_list = deepcopy(flights)

    time2 = time.time()
    update_plane_l_domains()
    update_plane_t_domains()
    update_l_to_t()
    update_t_to_l()
    print time.time()-time2

    flights = deepcopy(p_list)
    print_flights(flights)
    for flight in flights:
        flight.new_takeoff_domain = deepcopy(flight.t_set)
        #flight.new_takeoff_domain = sorted(flight.new_takeoff_domain)
        flight.new_land_domain = deepcopy(flight.l_set)
        #flight.new_land_domain = sorted(flight.new_land_domain)
    flights_for_assignment = deepcopy(flights)

    dprint("=============================================")

    dprint(schedule(landing, gates, takingoff, flights))
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
