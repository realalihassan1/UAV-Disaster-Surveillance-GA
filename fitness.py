
import math


def calculate_fitness(chromosome, environment):
    coverage = set()
    detected_targets = set()

    total_distance = 0
    energy = 0
    hazard_exposure = 0
    violations = 0

    # Flight constraints
    max_flight_range = 50
    previous_x, previous_y = environment.starts[0]

    for waypoint in chromosome.waypoints:
        x = waypoint["x"]
        y = waypoint["y"]
        speed = waypoint["speed"]
        sensor_power = waypoint["sensor_power"]
        sensor_on = waypoint["sensor_on"]

        # Check grid boundaries
        if not (
            0 <= x < environment.grid_size
            and 0 <= y < environment.grid_size
        ):
            violations += 1
            continue

        # Calculate distance from previous position
        distance = math.hypot(
            x - previous_x,
            y - previous_y
        )

        total_distance += distance

        # Estimate energy consumption
        energy += distance * (
            1 + sensor_power * sensor_on
        )

        # Estimate sensor coverage
        if sensor_on:
            for gx in range(environment.grid_size):
                for gy in range(environment.grid_size):
                    sensor_distance = math.hypot(
                        gx - x, gy - y
                    )

                    if sensor_distance <= 2:
                        coverage.add((gx, gy))

            # Detect targets within sensor radius
            for target in environment.targets:
                tx, ty = target

                if math.hypot(tx - x, ty - y) <= 2:
                    detected_targets.add(target)

        # Check whether the waypoint is in a hazard
        if (x, y) in environment.hazards:
            hazard_exposure += 1

        # Check whether the waypoint is in an obstacle
        if (x, y) in environment.obstacles:
            violations += 1

        previous_x, previous_y = x, y

    # Penalize exceeding the maximum flight range
    if total_distance > max_flight_range:
        violations += 1

    number_of_targets = max(1, len(environment.targets))

    coverage_score = len(coverage) / (
        environment.grid_size ** 2
    )

    detection_score = (
        len(detected_targets) / number_of_targets
    )

    energy_score = energy / 100
    time_score = total_distance / 100

    risk_score = hazard_exposure / max(
        1, len(chromosome.waypoints)
    )

    fitness = (
        10 * coverage_score
        + 5 * detection_score
        - 2 * energy_score
        - time_score
        - 8 * risk_score
        - 100 * violations
    )

    return fitness


if __name__ == "__main__":
    from enviroment import Environment
    from chromosome import Chromosome

    environment = Environment()
    chromosome = Chromosome(environment)

    score = calculate_fitness(chromosome, environment)

    print("Flight Plan:")
    chromosome.display()
    print(f"\nFitness Score: {score:.3f}")