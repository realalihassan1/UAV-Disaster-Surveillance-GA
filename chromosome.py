
import random


class Chromosome:
    def __init__(self, environment, num_waypoints=5):
        self.environment = environment
        self.num_waypoints = num_waypoints
        self.waypoints = []
        self.create_random_route()

    def create_random_route(self):
        self.waypoints = []

        # Generate random waypoints outside obstacles
        while len(self.waypoints) < self.num_waypoints:
            x = random.randint(0, self.environment.grid_size - 1)
            y = random.randint(0, self.environment.grid_size - 1)

            if (x, y) not in self.environment.obstacles:
                waypoint = {
                    "x": x,
                    "y": y,
                    "speed": round(random.uniform(1.0, 3.0), 2),
                    "sensor_power": round(random.uniform(0.5, 1.0), 2),
                    "sensor_on": random.randint(0, 1)
                }

                self.waypoints.append(waypoint)

    def display(self):
        for i, waypoint in enumerate(self.waypoints, start=1):
            print(f"Waypoint {i}: {waypoint}")


if __name__ == "__main__":
    from enviroment import Environment

    environment = Environment()
    chromosome = Chromosome(environment)

    print("Random Drone Flight Plan:")
    chromosome.display()
