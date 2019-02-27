class Flight:
  def __init__(self, max_air_time, landing_time, minimum_service_time, takeoff_time, max_service_time):
    self.max_air_time = max_air_time
    self.landing_time = landing_time
    self.minimum_service_time = minimum_service_time
    self.takeoff_time = takeoff_time
    self.max_service_time = max_service_time

  def print_flight(self):
    print(str(self.max_air_time) + " " +
          str(self.landing_time) + " " +
          str(self.minimum_service_time) + " " +
          str(self.takeoff_time) + " " +
          str(self.max_service_time) + " ")


def print_flights(flights):
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


def main():
    flight = Flight(0, 10, 50, 20, 70)
    flight.print_flight()

    read_file()


if __name__ == '__main__':
    main()
