from copy import deepcopy
import time
debug = False
minutes = 2000


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
        self.l_set = set()
        self.t_set = set()

    def __eq__(self, other):
        return self.max_air_time == other.max_air_time and \
               self.landing_time == other.landing_time and \
               self.minimum_service_time == other.minimum_service_time and \
               self.takeoff_time == other.takeoff_time and \
               self.maximum_service_time == other.maximum_service_time

    def __hash__(self):
        return hash((self.max_air_time, self.landing_time, self.minimum_service_time, self.takeoff_time,
                     self.maximum_service_time))


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
    for i in range(start, end, 1):
        if landing_runways_available[i] <= 0:
            return False
    return True


def check_gates_available(start, end):
    for i in range(start, end, 1):
        if gates_available[i] <= 0:
            return False
    return True


def check_takeoff_runways_available(start, end):
    for i in range(start, end, 1):
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
    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_landing_domains_for_other_flights(flights):
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
    for i in range(minutes):
        if takeoff_runways_available[i] == 0:
            for flight in flights:
                if update_takeoff_domain_for_flight(flight, i):
                    return True
    return False


def schedule2(landing, gates, takingoff, unscheduled):
    if len(unscheduled) == 0:
        f2 = open("output.txt", "w")
        str2 = ""
        for f in flights_for_assignment:
            str2 += str(f.assignment[1]) + " " + str(f.assignment[2]) + "\n"
        f2.write(str2)
        return True
    copied = deepcopy(unscheduled)
    unsch = unscheduled[0]
    unsch.new_land_domain = deepcopy(reorder_by_overlap(unsch, unscheduled))
    for dom in unsch.new_land_domain:
        if check_landing_runway_available(dom, dom + unsch.landing_time):
            eligible = find_eligible_takeoff_times(unsch, dom)
            if len(eligible) > 0:
                for e in eligible:
                    if check_gates_available(dom + unsch.landing_time, e) and check_takeoff_runways_available(e,
                                                                                                              e + unsch.takeoff_time):
                        mark_landing_runway_busy(dom, dom + unsch.landing_time)

                        mark_gates_busy(dom + unsch.landing_time, e)
                        mark_takeoff_runways_busy(e, e + unsch.takeoff_time)
                        if update_landing_domains_for_other_flights(unscheduled):
                            just_remove_landing_and_take_off_entries_from_time_arrays(unsch, dom, e)
                            continue
                        if update_gate_domains_for_other_flights(unscheduled):
                            just_remove_landing_and_take_off_entries_from_time_arrays(unsch, dom, e)
                            continue
                        if update_takeoff_domains_for_other_flights(unscheduled):
                            just_remove_landing_and_take_off_entries_from_time_arrays(unsch, dom, e)
                            continue
                        unsch.assignment = [True, dom, e]

                        for original in flights_for_assignment:
                            if original.id == unsch.id:
                                original.assignment = deepcopy([True, dom, e])

                        unscheduled.remove(unsch)

                        unscheduled = sorted(unscheduled, key=lambda f: len(f.new_land_domain))
                        answer = schedule2(landing, gates, takingoff, unscheduled)
                        if not answer:
                            unschedule_flight(unsch)
                            for original in flights_for_assignment:
                                if original.id == unsch.id:
                                    original.assignment = deepcopy([False, -1, -1])

                            mark_landing_runway_busy(dom, dom + unsch.landing_time)
                            unscheduled = deepcopy(copied)

                        if answer:
                            return True
                for i in range(dom, dom + unsch.landing_time):
                    landing_runways_available[i] = landing_runways_available[i] + 1

    return False


def just_remove_landing_and_take_off_entries_from_time_arrays(plane, landing_time, take_off_time):
    chosen_landing_start_time = landing_time
    for i in range(chosen_landing_start_time, chosen_landing_start_time + plane.landing_time):
        landing_runways_available[i] = landing_runways_available[i] + 1

    chosen_service_end_time = take_off_time
    for i in range(chosen_landing_start_time + plane.landing_time, chosen_service_end_time):
        gates_available[i] = gates_available[i] + 1

    for i in range(chosen_service_end_time, chosen_service_end_time + plane.takeoff_time):
        takeoff_runways_available[i] = takeoff_runways_available[i] + 1



def unschedule_flight(flight):
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
            og.assignment = deepcopy([False, -1])


def update_plane_l_domains():
    for p in p_list:
        for i in range(0, p.max_air_time + 1):
            p.l_set.add(i)


def update_plane_t_domains():
    for p in p_list:
        for i in range(p.landing_time + p.minimum_service_time, p.max_air_time + p.landing_time + p.maximum_service_time):
            p.t_set.add(i)


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
    return sorted(map_const)


def main():
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)
    global flights_for_assignment
    global p_list
    p_list = deepcopy(flights)

    update_plane_l_domains()
    update_plane_t_domains()

    flights = deepcopy(p_list)

    flights_for_assignment = deepcopy(flights)
    for flight in flights:
        flight.new_takeoff_domain = deepcopy(flight.t_set)
        flight.new_takeoff_domain = sorted(flight.new_takeoff_domain)
        flight.new_land_domain = deepcopy(flight.l_set)
        flight.new_land_domain = sorted(flight.new_land_domain)
    flights = sorted(flights, key=lambda f: len(f.new_land_domain))
    for flight in flights:
        flight.new_land_domain = deepcopy(reorder_by_overlap(flight, flights))
    res = schedule2(landing, gates, takingoff, flights)
    print res


if __name__ == '__main__':
    time1 = time.time()
    main()
    time2 = time.time()
    print time2 - time1
