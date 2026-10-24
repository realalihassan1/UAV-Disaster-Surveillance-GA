
import matplotlib.pyplot as plt


def plot_drone_path(environment, chromosome):
    plt.figure(figsize=(10, 8))

    # Draw obstacles
    if environment.obstacles:
        ox, oy = zip(*environment.obstacles)
        plt.scatter(
            ox, oy, color="black", marker="s",
            s=100, label="Obstacles"
        )

    # Draw hazardous areas
    if environment.hazards:
        hx, hy = zip(*environment.hazards)
        plt.scatter(
            hx, hy, color="red", marker="X",
            s=120, label="Hazards"
        )

    # Draw disaster targets
    if environment.targets:
        tx, ty = zip(*environment.targets)
        plt.scatter(
            tx, ty, color="green", marker="*",
            s=200, label="Targets"
        )

    # Draw the drone's starting point
    start_x, start_y = environment.starts[0]
    plt.scatter(
        start_x, start_y, color="blue",
        marker="s", s=150, label="Drone Start"
    )

    # Extract the best route
    waypoints = chromosome.waypoints

    route_x = [start_x]
    route_y = [start_y]

    for waypoint in waypoints:
        route_x.append(waypoint["x"])
        route_y.append(waypoint["y"])

    # Draw route and waypoints
    plt.plot(
        route_x, route_y,
        color="orange", linewidth=2,
        marker="o", markersize=6,
        label="Drone Flight Path"
    )

    for i, waypoint in enumerate(waypoints, start=1):
        plt.annotate(
            str(i),
            (waypoint["x"], waypoint["y"]),
            xytext=(5, 5),
            textcoords="offset points"
        )

    plt.xlim(-0.5, environment.grid_size - 0.5)
    plt.ylim(-0.5, environment.grid_size - 0.5)

    plt.xticks(range(environment.grid_size))
    plt.yticks(range(environment.grid_size))

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Best UAV Flight Path")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig("uav_flight_path.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    from enviroment import Environment
    from chromosome import Chromosome

    environment = Environment()
    chromosome = Chromosome(environment)

    plot_drone_path(environment, chromosome)
