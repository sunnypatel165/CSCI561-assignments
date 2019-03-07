from collections import OrderedDict
from copy import deepcopy

debug = False
minutes = 1000
flights_for_assignment = OrderedDict()
input_file = "input7.txt"
output_file = "output.txt"

LANDING_RUNWAY = 1
GATE = 2
TAKEOFF_RUNWAY = 3


class Flight:

    def __init__(self, flight_id, max_air_time, landing_time, minimum_service_time, takeoff_time, maximum_service_time):
        self.id = "P" + str(flight_id)
        self.assignment = []
        self.new_land_domain = []
        self.new_takeoff_domain = []
        self.max_air_time = max_air_time
        self.landing_time = landing_time
        self.minimum_service_time = minimum_service_time
        self.takeoff_time = takeoff_time
        self.maximum_service_time = maximum_service_time
        self.new_land_domain = set()
        self.new_takeoff_domain = set()
        self.new_land_domain_map = {}
        self.new_land_domain_map = {}

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

    def reset_flight(self):
        self.assignment = []

    def __eq__(self, other):
        return self.max_air_time == other.max_air_time and \
               self.landing_time == other.landing_time and \
               self.minimum_service_time == other.minimum_service_time and \
               self.takeoff_time == other.takeoff_time and \
               self.maximum_service_time == other.maximum_service_time and \
               self.id == other.id

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
    for id, f in flights.items():
        f.print_assignment()


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
    f1 = open(input_file, "r")
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
    for i in range(start, end - 1, 1):  # dumb - if [0, 10] then it should check for 0 to 9
        if landing_runways_available[i] <= 0:
            return False
    return True


def check_gates_available(start, end):
    for i in range(start, end - 1, 1):  # dumb - if [0, 10] then it should check for 0 to 9
        if gates_available[i] <= 0:
            return False
    return True


def check_takeoff_runways_available(start, end):
    for i in range(start, end - 1, 1):  # dumb - if [0, 10] then it should check for 0 to 9
        if takeoff_runways_available[i] <= 0:
            return False
    return True


# mark busy
def mark_resource_busy(start, end, resource):
    if resource == LANDING_RUNWAY:
        for i in range(start, end, 1):
            landing_runways_available[i] = landing_runways_available[i] - 1

    if resource == GATE:
        for i in range(start, end, 1):
            gates_available[i] = gates_available[i] - 1

    if resource == TAKEOFF_RUNWAY:
        for i in range(start, end, 1):
            takeoff_runways_available[i] = takeoff_runways_available[i] - 1


def mark_resource_available(start, end, resource):
    if resource == LANDING_RUNWAY:
        for i in range(start, end, 1):
            landing_runways_available[i] = landing_runways_available[i] + 1

    if resource == GATE:
        for i in range(start, end, 1):
            gates_available[i] = gates_available[i] + 1

    if resource == TAKEOFF_RUNWAY:
        for i in range(start, end, 1):
            takeoff_runways_available[i] = takeoff_runways_available[i] + 1


def find_eligible_takeoff_times(flight, selected_landing):
    eligible = []
    for dom in flight.new_takeoff_domain:
        if selected_landing + flight.landing_time + flight.minimum_service_time <= dom <= selected_landing + flight.landing_time + flight.maximum_service_time:
            eligible.append(dom)
    return eligible


def update_domain_for_flight(flight, t):
    for dom in flight.new_land_domain:
        if dom <= t < dom + flight.landing_time:  # dumb - if [0, 10] then it should check for 0 to 9
            flight.new_land_domain.remove(dom)
    if len(flight.new_land_domain) == 0:
        return True
    return False


def update_takeoff_domain_for_flight(flight, t):
    for dom in flight.new_takeoff_domain:
        if dom <= t < dom + flight.takeoff_time:  # dumb - if [0, 10] then it should check for 0 to 9
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
        if dom + flight.landing_time <= t < dom + flight.landing_time + flight.minimum_service_time:
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


def print_output():
    print_flights_assignments(flights_for_assignment)
    if not debug:
        f2 = open(output_file, "w")
        str2 = ""
        for id, f in flights_for_assignment.items():
            str2 += str(f.assignment[1]) + " " + str(f.assignment[2]) + "\n"
        f2.write(str2)
    else:
        for id, f in flights_for_assignment.items():
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
        was_scheduled = False  # dumb - otherwise will fail at bottom when it tries to unschedule
        print_state()
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

                        dprint("before schedule")
                        print_state()
                        schedule_flight(unsch, dom, eligible)
                        was_scheduled = True
                        dprint("after schedule")
                        print_state()
                        print_flights(unscheduled)
                        unscheduled.remove(unsch)
                        if not update_and_check_all_domains(unscheduled):
                            if was_scheduled:
                                was_scheduled = False
                                unschedule_flight(unsch)
                            unscheduled = deepcopy(copied)
                            continue
                            # return False # can not return false as this will disallow further landings to be tried!!!!
                        dprint("updated domains")
                        print_flights(unscheduled)
                        unscheduled = sort_flights_most_constrained_variable(unscheduled)

                        answer = schedule_flights(landing, gates, takingoff, unscheduled)
                        if not answer:
                            dprint("Trying next take off ")
                            unschedule_flight(unsch)
                            was_scheduled = False
                            unscheduled = deepcopy(copied)
                        if answer:
                            return True
                # undo landing
                dprint("Tried all take off, undo landing")
                if was_scheduled:
                    unschedule_flight(unsch)
                unscheduled = deepcopy(copied)
                # mark_resource_available(dom, dom + unsch.landing_time, LANDING_RUNWAY)
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
    mark_resource_busy(landing_start_time, landing_start_time + flight.landing_time, LANDING_RUNWAY)
    mark_resource_busy(landing_start_time + flight.landing_time, takeoff_start_time, GATE)
    mark_resource_busy(takeoff_start_time, takeoff_start_time + flight.takeoff_time, TAKEOFF_RUNWAY)

    flight.assignment = [True, landing_start_time, takeoff_start_time]
    update_flight_for_assignment(flight, True, landing_start_time, takeoff_start_time)


def update_flight_for_assignment(flight, found, landing_start_time, takeoff_start_time):
    flights_for_assignment[flight.id].assignment = deepcopy([True, landing_start_time, takeoff_start_time])


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

def least_constraining_value(flight, flights):
    overlaps = {}
    land_domains = flight.new_land_domain
    for val in land_domains:
        count = 0
        for plane in flights:
            if plane != flight:
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


def setup_initial_domains(flights):
    for flight in flights:
        for i in range(0, flight.max_air_time + 1, 1):
            flight.new_land_domain.add(i)

    for flight in flights:
        for i in range(flight.landing_time + flight.minimum_service_time,
                       flight.max_air_time + flight.landing_time + flight.maximum_service_time + 1):
            flight.new_takeoff_domain.add(i)

def main():
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)

    global flights_for_assignment

    setup_initial_domains(flights)

    print_flights(flights)

    # flights_for_assignment = deepcopy(flights)
    for flight in flights:
        flights_for_assignment[flight.id] = deepcopy(flight)
    dprint(flights_for_assignment)

    sort_domains(flights)
    flights = sort_flights_most_constrained_variable(flights)

    dprint("===sorted===")
    print_flights(flights)

    # for flight in flights:
    #     flight.new_land_domain = least_constraining_value(flight, flights)

    dprint("=============================================")

    dprint(schedule_flights(landing, gates, takingoff, flights))
    print_flights(flights)


if __name__ == '__main__':
    main()
