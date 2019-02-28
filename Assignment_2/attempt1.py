debug = True


class Flight:

    def __init__(self, max_air_time, landing_time, minimum_service_time, takeoff_time, max_service_time):
        self.dom_air_time = []
        self.dom_service_time = []
        self.max_air_time = max_air_time
        self.landing_time = landing_time
        self.minimum_service_time = minimum_service_time
        self.takeoff_time = takeoff_time
        self.maximum_service_time = max_service_time
        self.update_dom_air_time()
        self.update_dom_service_time()

    def print_flight(self):
        print(str(self.max_air_time) + " " +
              str(self.landing_time) + " " +
              str(self.minimum_service_time) + " " +
              str(self.takeoff_time) + " " +
              str(self.maximum_service_time) + " " +
              str(self.dom_air_time) + " " +
              str(self.dom_service_time))

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


def read_file():
    f1 = open("input0.txt", "r")
    line = f1.readline().strip().split()
    landing, gates, takingoff = int(line[0]), int(line[1]), int(line[2])
    n = int(f1.readline())
    flights = []
    for i in xrange(n):
        line = f1.readline().strip().split()
        flight = Flight(int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]))
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
    landing_runways_available = [landing] * 1000
    gates_available = [gates] * 1000
    takeoff_runways_available = [takeoff] * 1000

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
    schedule_landing(flight)


def schedule_landing(flight):
    # For every possible domain of air time
    for dom in flight.dom_air_time:
        # Check if runway is available for the entire time needed
        if check_landing_runway_available(dom, dom + flight.landing_time):
            chosen_landing_start = dom
            chosen_landing_end = dom + flight.landing_time
            if schedule_service(flight, chosen_landing_end):
                return [True, chosen_landing_start]


def schedule_service(flight, chosen_landing_end_time):
    # For every possible domain of service time
    for dom in flight.dom_service_time:
        if check_gates_available(chosen_landing_end_time, chosen_landing_end_time + dom):
            if schedule_takeoff(flight, chosen_landing_end_time + dom):
                return True


def schedule_takeoff(flight, chosen_service_end_time):
    return check_takeoff_runways_available(chosen_service_end_time, chosen_service_end_time + flight.takeoff_time)


# Schedule a flight
def schedule(flights):
    for flight in flights:

        # try every possible land start time
        chosen_land_start_time = -1
        for i in range(0, flight.max_air_time):
            if check_landing_runway_available(i, i + flight.landing_time):
                chosen_land_start_time = i
                break

        # try a service time
        chosen_land_end_time = chosen_land_start_time + flight.landing_time
        for i in range(flight.minimum_service_time, flight.maximum_service_time, 1):
            if check_gates_available(chosen_land_end_time,
                                     i + chosen_land_end_time) and check_takeoff_runways_available(
                i + chosen_land_start_time, i + chosen_land_end_time):
                chosen_service_end_time = i
                break

    # ===
    # try to assign the available land time
    # If the landing time assignment is valid, try to assign the take off time
    # If there is valid assignment for both, go ahead to the next plane,
    # else backtrack

    # # Find the next available landing time
    # chosen_landing_start = 0
    # for landing_time in flight.dom_air_time:
    #     available = True
    #     for time in range(landing_time, landing_time + landing + 1, 1):
    #         if landing_runways_available[time] <= 0:
    #             available = False
    #             break
    #     if available:
    #         # If this domain value is a valid land time
    #         chosen_landing_start = time
    #         for time in range(landing_time, landing_time + landing + 1, 1):
    #             landing_runways_available[time] = landing_runways_available[time]-1
    #         break
    #
    # # Find the next right service time
    # for service_time in flight.dom_service_time:
    #     available = True
    #     for time in range(0, service_time, 1):
    #         if gates_available[time + chosen_landing_start] <= 0:
    #             available = False
    #     if available:
    #         # If this domain value is a valid land time
    #         for time in range(0, service_time, 1):
    #             gates_available[time] = gates_available[time] - 1
    #         break


def main():
    flight = Flight(0, 10, 50, 20, 70)
    flight.print_flight()
    landing, gates, takingoff, flights = read_file()
    initialise_time(landing, gates, takingoff)


if __name__ == '__main__':
    main()
