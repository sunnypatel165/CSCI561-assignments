from copy import deepcopy

debug = True
minutes = 1000
flights_for_assignment = []
input = "input1.txt"
output = "output.txt"


class Flight:

    def __init__(self, flight_id, max_air_time, landing_time, minimum_service_time, takeoff_time, maximum_service_time):
        self.id = "P" + str(flight_id)
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
        self.new_land_domain = set()
        self.new_takeoff_domain = set()

    def print_flight(self):
        dprint(self.id + " " +
               str(self.max_air_time) + " " +
               str(self.landing_time) + " " +
               str(self.minimum_service_time) + " " +
               str(self.takeoff_time) + " " +
               str(self.maximum_service_time) + " " +
               str(self.new_land_domain) + " " +
               str(self.new_takeoff_domain) + " " +
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
    f1 = open(input, "r")
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
    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_takeoff_domain_for_flight(flight, t):
    for dom in flight.new_takeoff_domain:
        if dom <= t <= dom + flight.takeoff_time:
            flight.new_takeoff_domain.remove(dom)
    if len(flight.new_takeoff_domain) == 0:
        return True
    return False


def update_landing_domains_for_other_flights(flights):
    dprint("updating domain")
    for i in range(minutes):
        if landing_runways_available[i] == 0:
            for flight in flights:
                if update_domain_for_flight(flight, i):
                    return True
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
    dprint("updating take off domain")
    for i in range(minutes):
        if takeoff_runways_available[i] == 0:
            for flight in flights:
                if update_takeoff_domain_for_flight(flight, i):
                    return True  # indicates empty
    return False


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


def print_output():
    print_flights_assignments(flights_for_assignment)
    if not debug:
        f2 = open(output, "w")
        str2 = ""
        for f in flights_for_assignment:
            str2 += str(f.assignment[1]) + " " + str(f.assignment[2]) + "\n"
        f2.write(str2)
    else:
        for f in flights_for_assignment:
            print str(f.assignment[1]) + " " + str(f.assignment[2])


def schedule_flights(landing, gates, takingoff, unscheduled):
    dprint("Trying to schedule:")
    print_flights_ids(unscheduled)

    if len(unscheduled) == 0:
        dprint("DONE")
        print_output()
        return True

    copied = deepcopy(unscheduled)
    unsch = unscheduled[0]
    unsch.new_land_domain = deepcopy(least_constraining_value(unsch, unscheduled))

    for dom in unsch.new_land_domain:
        dprint(unsch.id + " Checking runway: " + str(dom) + " " + str(dom + unsch.landing_time))
        if check_landing_runway_available(dom, dom + unsch.landing_time):
            eligible_takeoff_times = find_eligible_takeoff_times(unsch, dom)
            dprint("Eligible takeoff times: " + str(eligible_takeoff_times))
            if len(eligible_takeoff_times) > 0:
                for eligible in eligible_takeoff_times:
                    dprint(unsch.id + " Checking gates: " + str(dom + unsch.landing_time) + " " + str(eligible))
                    dprint(unsch.id + " Checking takeo: " + str(eligible) + " " + str(eligible + unsch.takeoff_time))
                    if check_gates_available(dom + unsch.landing_time, eligible) and \
                            check_takeoff_runways_available(eligible, eligible + unsch.takeoff_time):

                        schedule_flight(unsch, dom, eligible)
                        unscheduled.remove(unsch)
                        if not update_and_check_all_domains(unscheduled):
                            return False

                        unscheduled = sort_flights_most_constrained_variable(unscheduled)

                        answer = schedule_flights(landing, gates, takingoff, unscheduled)
                        if not answer:
                            unschedule_flight(unsch)
                            mark_landing_runway_busy(dom, dom + unsch.landing_time)
                            unscheduled = deepcopy(copied)
                        if answer:
                            return True
                # undo landing
                dprint("Tried all take off, undo landing")

                mark_landing_runway_busy(dom, dom + unsch.landing_time)
    return False


def update_and_check_all_domains(unscheduled):
    if update_landing_domains_for_other_flights(unscheduled):
        return False
    if update_gate_domains_for_other_flights(unscheduled):
        return False
    if update_takeoff_domains_for_other_flights(unscheduled):
        return False
    return True


def schedule_flight(flight, landing_start_time, takeoff_start_time):
    mark_landing_runway_busy(landing_start_time, landing_start_time + flight.landing_time)

    mark_gates_busy(landing_start_time + flight.landing_time, takeoff_start_time)
    mark_takeoff_runways_busy(takeoff_start_time, takeoff_start_time + flight.takeoff_time)
    flight.assignment = [True, landing_start_time, takeoff_start_time]
    update_flight_for_assignment(flight, True, landing_start_time, takeoff_start_time)


def update_flight_for_assignment(flight, found, landing_start_time, takeoff_start_time):
    for original in flights_for_assignment:
        if original.id == flight.id:
            dprint("assigining original" + flight.id + str([found, landing_start_time, takeoff_start_time]))
            original.assignment = deepcopy([True, landing_start_time, takeoff_start_time])

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
    update_flight_for_assignment(flight, False, -1, -1)

    print_state()
    dprint("==========")


def setup_initial_landing_domains(flights):
    for flight in flights:
        flight.new_land_domain.add(0)
        flight.new_land_domain.add(flight.max_air_time)


def update_plane_l_domains(flights):
    setup_initial_landing_domains(flights)

    landing_queue = list()

    landing_queue.append(flights[0])
    while len(landing_queue) > 0:
        plane = landing_queue[0]
        del landing_queue[0]
        new_land_domain = plane.new_land_domain
        for l in new_land_domain:
            for plane_in in flights:
                if plane == plane_in:
                    continue
                else:
                    if l + plane.landing_time >= max(plane_in.new_land_domain) or l + plane.landing_time <= min(
                            plane_in.new_land_domain):
                        continue
                    else:
                        if l + plane.landing_time in plane_in.new_land_domain:
                            continue
                        else:
                            plane_in.new_land_domain.add(l + plane.landing_time)
                            if plane_in not in landing_queue:
                                landing_queue.append(plane_in)


def setup_initial_takeoff_domains(flights):
    for flight in flights:
        flight.new_takeoff_domain.add(flight.landing_time + flight.minimum_service_time)
        flight.new_takeoff_domain.add(flight.max_air_time + flight.landing_time + flight.maximum_service_time)


def update_plane_t_domains(flights):
    setup_initial_takeoff_domains(flights)

    take_off_queue = list()
    take_off_queue.append(flights[0])
    while len(take_off_queue) > 0:
        plane = take_off_queue[0]
        del take_off_queue[0]
        new_takeoff_domain = plane.new_takeoff_domain
        for t in new_takeoff_domain:
            for plane_in in flights:
                if plane == plane_in:
                    continue
                else:
                    if t + plane.takeoff_time >= max(plane_in.new_takeoff_domain) or t + plane.takeoff_time <= min(
                            plane_in.new_takeoff_domain):
                        continue
                    else:
                        if t + plane.takeoff_time in plane_in.new_takeoff_domain:
                            continue
                        else:
                            plane_in.new_takeoff_domain.add(t + plane.takeoff_time)
                            if plane_in not in take_off_queue:
                                take_off_queue.append(plane_in)


def update_t_to_l(flights):
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(flights[0])
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        new_takeoff_domain = plane.new_takeoff_domain
        is_updated = False
        for t in new_takeoff_domain:
            max_val = t - plane.maximum_service_time - plane.landing_time
            min_val = t - plane.minimum_service_time - plane.landing_time
            if 0 < min_val < max(plane.new_land_domain):
                if min_val not in plane.new_land_domain:
                    plane.new_land_domain.add(min_val)
                    is_updated = True
            if 0 < max_val < max(plane.new_land_domain):
                if max_val not in plane.new_land_domain:
                    plane.new_land_domain.add(max_val)
                    is_updated = True

        if is_updated is True:
            landing_queue = list()
            landing_queue.append(plane)
            while len(landing_queue) > 0:
                plane = landing_queue[0]
                del landing_queue[0]
                new_land_domain = plane.new_land_domain
                for l in new_land_domain:
                    for plane_in in flights:
                        if plane == plane_in:
                            continue
                        else:
                            if l + plane.landing_time >= max(plane_in.new_land_domain) or l + plane.landing_time <= min(
                                    plane_in.new_land_domain):
                                continue
                            else:
                                if l + plane.landing_time in plane_in.new_land_domain:
                                    continue
                                else:
                                    plane_in.new_land_domain.add(l + plane.landing_time)
                                    if plane_in not in landing_queue:
                                        landing_queue.append(plane_in)


def update_l_to_t(flights):
    take_off_to_landing_queue = list()
    take_off_to_landing_queue.append(flights[0])
    while len(take_off_to_landing_queue) > 0:
        plane = take_off_to_landing_queue[0]
        del take_off_to_landing_queue[0]
        new_land_domain = plane.new_land_domain
        is_updated = False
        for l in new_land_domain:
            min_val = l + plane.landing_time + plane.minimum_service_time
            max_val = l + plane.landing_time + plane.maximum_service_time
            if min_val > 0 and min(plane.new_takeoff_domain) < min_val < max(plane.new_takeoff_domain):
                if min_val not in plane.new_takeoff_domain:
                    plane.new_takeoff_domain.add(min_val)
                    is_updated = True
            if max_val > 0 and min(plane.new_takeoff_domain) < max_val < max(plane.new_takeoff_domain):
                if max_val not in plane.new_takeoff_domain:
                    plane.new_takeoff_domain.add(max_val)
                    is_updated = True

        if is_updated is True:
            take_off_queue = list()
            take_off_queue.append(plane)
            while len(take_off_queue) > 0:
                plane = take_off_queue[0]
                del take_off_queue[0]
                new_takeoff_domain = plane.new_takeoff_domain
                for t in new_takeoff_domain:
                    for plane_in in flights:
                        if plane == plane_in:
                            continue
                        else:
                            if t + plane.takeoff_time >= max(
                                    plane_in.new_takeoff_domain) or t + plane.takeoff_time <= min(
                                    plane_in.new_takeoff_domain):
                                continue
                            else:
                                if t + plane.takeoff_time in plane_in.new_takeoff_domain:
                                    continue
                                else:
                                    plane_in.new_takeoff_domain.add(t + plane.takeoff_time)
                                    if plane_in not in take_off_queue:
                                        take_off_queue.append(plane_in)


def least_constraining_value(flight, flights):
    overlaps = {}
    land_domains = flight.new_land_domain
    for val in land_domains:
        count = 0
        for plane in flights:
            if plane == flight:
                continue
            else:
                if detect_overlaps_with_val(plane, val):
                    count = count + 1
        overlaps[val] = count
    return sorted(overlaps)


def overlap_in_range(x1, y1, x2, y2):
    return max(x1, y1) <= min(x2, y2)


def detect_overlaps_with_val(flight, val):
    plane_dom_list = flight.new_land_domain
    for item in plane_dom_list:
        if overlap_in_range(item, item + flight.landing_time, val, val + flight.landing_time) != 0:
            return True
    return False


def sort_domains(flights):
    for flight in flights:
        flight.new_takeoff_domain = sorted(flight.new_takeoff_domain)
        flight.new_land_domain = sorted(flight.new_land_domain)


def sort_flights_most_constrained_variable(flights):
    return sorted(flights, key=lambda f: len(f.new_land_domain))


def main():
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)

    global flights_for_assignment

    update_plane_l_domains(flights)
    update_plane_t_domains(flights)
    update_l_to_t(flights)
    update_t_to_l(flights)

    print_flights(flights)

    flights_for_assignment = deepcopy(flights)

    sort_domains(flights)
    flights = sort_flights_most_constrained_variable(flights)

    dprint("===sorted===")
    print_flights(flights)

    for flight in flights:
        flight.new_land_domain = least_constraining_value(flight, flights)

    dprint("=============================================")

    dprint(schedule_flights(landing, gates, takingoff, flights))
    print_flights(flights)


if __name__ == '__main__':
    main()
