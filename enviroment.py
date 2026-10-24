
import numpy as np
import matplotlib.pyplot as plt


class Environment:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size

        # Cells the drones cannot fly through
        self.obstacles = [
            (5, 5), (5, 6), (5, 7),
            (6, 7), (7, 7),
            (10, 12), (11, 12), (12, 12),
            (15, 4), (15, 5), (15, 6)
        ]

        # Dangerous areas: drones should avoid these
        self.hazards = [
            (8, 8), (8, 9), (9, 8),
            (13, 14), (14, 14), (14, 15)
        ]

        # Important locations that drones should survey
        self.targets = [
            (3, 15), (10, 5), (17, 16),
            (12, 3), (4, 10)
        ]

        # Starting positions of three drones
        self.starts = [
            (0, 0), (0, 19), (19, 0)
        ]

    def plot(self):
        grid = np.zeros(
            (self.grid_size, self.grid_size)
        )

        for x, y in self.obstacles:
            grid[y, x] = 1

        for x, y in self.hazards:
            grid[y, x] = 2

        for x, y in self.targets:
            grid[y, x] = 3

        plt.figure(figsize=(9, 7))
        plt.imshow(
            grid,
            origin="lower",
            cmap="viridis",
            interpolation="nearest"
        )

        plt.colorbar(
            ticks=[0, 1, 2, 3],
            label="Cell Type"
        )

        plt.xticks(range(self.grid_size))
        plt.yticks(range(self.grid_size))
        plt.grid(True, alpha=0.3)
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.title("UAV Disaster Management Environment")

        # Mark drone starting positions
        for i, (x, y) in enumerate(self.starts):
            plt.scatter(x, y, marker="s", s=100,
                        label=f"Drone {i + 1} Start")

        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    environment = Environment()
    environment.plot()
    