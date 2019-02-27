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


def main():
    flight = Flight(0, 10, 50, 20, 70)
    flight.print_flight()


if __name__ == '__main__':
    main()