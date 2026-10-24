
import numpy as np
import matplotlib.pyplot as plt


def plot_coverage(environment, chromosome, sensor_radius=2):
    grid_size = environment.grid_size
    coverage = np.zeros((grid_size, grid_size))

    for waypoint in chromosome.waypoints:
        if waypoint["sensor_on"] == 1:
            x = waypoint["x"]
            y = waypoint["y"]
            power = waypoint["sensor_power"]

            for gx in range(grid_size):
                for gy in range(grid_size):
                    distance = np.sqrt(
                        (gx - x) ** 2 + (gy - y) ** 2
                    )

                    if distance <= sensor_radius:
                        coverage[gy, gx] = max(
                            coverage[gy, gx], power
                        )

    plt.figure(figsize=(10, 8))

    plt.imshow(
        coverage,
        origin="lower",
        cmap="hot",
        interpolation="nearest",
        vmin=0,
        vmax=1
    )

    plt.colorbar(label="Sensor Coverage Strength")

    if environment.obstacles:
        ox, oy = zip(*environment.obstacles)
        plt.scatter(
            ox, oy, color="cyan",
            marker="s", s=70, label="Obstacles"
        )

    if environment.targets:
        tx, ty = zip(*environment.targets)
        plt.scatter(
            tx, ty, color="lime",
            marker="*", s=180, label="Targets"
        )

    start_x, start_y = environment.starts[0]
    plt.scatter(
        start_x, start_y, color="blue",
        marker="s", s=120, label="Drone Start"
    )

    plt.xticks(range(grid_size))
    plt.yticks(range(grid_size))
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("UAV Sensor Coverage Heatmap")
    plt.legend()
    plt.tight_layout()

    plt.savefig("coverage_heatmap.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    from enviroment import Environment
    from chromosome import Chromosome

    environment = Environment()
    chromosome = Chromosome(environment)

    plot_coverage(environment, chromosome)
