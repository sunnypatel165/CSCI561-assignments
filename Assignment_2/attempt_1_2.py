from copy import deepcopy

debug = True
minutes = 200


class Flight:

    def __init__(self, id, max_air_time, landing_time, minimum_service_time, takeoff_time, max_service_time):
        self.id = "P" + str(id)
        self.dom_air_time = []
        self.dom_service_time = []
        self.assignment = []
        self.max_air_time = max_air_time
        self.landing_time = landing_time
        self.minimum_service_time = minimum_service_time
        self.takeoff_time = takeoff_time
        self.maximum_service_time = max_service_time
        self.update_dom_air_time()
        self.update_dom_service_time()

    def print_flight(self):
        print(self.id + " " +
              str(self.max_air_time) + " " +
              str(self.landing_time) + " " +
              str(self.minimum_service_time) + " " +
              str(self.takeoff_time) + " " +
              str(self.maximum_service_time) + " " +
              str(self.dom_air_time) + " " +
              str(self.dom_service_time) + " " +
              str(self.assignment))

    def update_dom_air_time(self):
        for i in range(0, self.max_air_time + 1, 1):
            self.dom_air_time.append(i)

    def update_dom_service_time(self):
        for i in range(self.minimum_service_time, self.maximum_service_time + 1, 1):
            self.dom_service_time.append(i)


def print_flights(flights):
    if not debug:
        return
    for i in flights:
        i.print_flight()


if debug == True:
    def dprint(line):
        if debug == True:
            print line
else:
    def dprint(line):
        return


def read_file():
    f1 = open("input0.txt", "r")
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
    for i in range(start, end + 1, 1):
        landing_runways_available[i] = landing_runways_available[i] - 1


def mark_gates_busy(start, end):
    for i in range(start, end + 1, 1):
        gates_available[i] = gates_available[i] - 1


def mark_takeoff_runways_busy(start, end):
    for i in range(start, end + 1, 1):
        takeoff_runways_available[i] = takeoff_runways_available[i] - 1


def schedule_single_flight_backtrack(flight):
    return schedule_landing(flight)


def schedule_landing(flight):
    # For every possible value in the  domain of air time
    for dom in flight.dom_air_time:
        # Check if runway is available for the entire time needed
        dprint(flight.id + " Trying landing time: " + str(dom) + "  " + str(dom + flight.landing_time))
        if check_landing_runway_available(dom, dom + flight.landing_time):
            chosen_landing_start = dom
            chosen_landing_end = dom + flight.landing_time
            service_possibility = schedule_service(flight, chosen_landing_end)

            if service_possibility[0] and service_possibility[1] != -1:
                mark_landing_runway_busy(dom, dom + flight.landing_time)
                answer = [True, chosen_landing_start, service_possibility[1]]
                flight.assignment = answer
                return answer
    return [False, -1]


def schedule_service(flight, chosen_landing_end_time):
    # For every possible domain of service time
    for dom in flight.dom_service_time:

        dprint(
            flight.id + " Trying gate time: " + str(chosen_landing_end_time) + "  " + str(
                chosen_landing_end_time + dom))

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


def schedule(flights):
    dprint("Trying to schedule " + str(flights))
    dprint("=============")
    print_state()
    unscheduled = deepcopy(flights)
    for flight in unscheduled:
        schedule_found = schedule_single_flight_backtrack(flight)
        if schedule_found[0]:
            unscheduled.remove(flight)
            if len(unscheduled) == 0:
                print "YES"
                return True
            if not schedule(unscheduled):
                dprint("unscheduling=====")

                unschedule_flight(flight)
                unscheduled.insert(0, flight)
        if not schedule_found[0]:
            print "NO"
            return False


def unschedule_flight(flight):
    dprint("==========")
    print_state()
    dprint("Unscheduling: ")
    dprint(flight.print_flight())

    if flight.assignment[0]:
        chosen_landing_start_time = flight.assignment[1]
        for i in range(chosen_landing_start_time, chosen_landing_start_time + flight.landing_time + 1):
            landing_runways_available[i] = landing_runways_available[i] + 1

        chosen_service_end_time = flight.assignment[2]
        for i in range(chosen_landing_start_time + flight.landing_time, chosen_service_end_time + 1):
            gates_available[i] = gates_available[i] + 1

        for i in range(chosen_service_end_time, chosen_service_end_time + flight.takeoff_time + 1):
            takeoff_runways_available[i] = takeoff_runways_available[i] + 1
    print_state()
    dprint("==========")


def main():
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)
    # print schedule_single_flight_backtrack(flights[0])
    # print_state()
    # print schedule_single_flight_backtrack(flights[1])
    # print_state()
    #
    schedule(flights)


if __name__ == '__main__':
    main()
