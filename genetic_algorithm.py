
import random
import matplotlib.pyplot as plt

from enviroment import Environment
from chromosome import Chromosome
from fitness import calculate_fitness
from path_visualization import plot_drone_path
from coverage_visualization import plot_coverage


class GeneticAlgorithm:
    def __init__(
        self,
        environment,
        population_size=50,
        generations=100,
        mutation_rate=0.10,
        crossover_rate=0.80,
        elite_size=2,
        tournament_size=3
    ):
        self.environment = environment
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.tournament_size = tournament_size

        self.population = []
        self.best_fitness_history = []
        self.average_fitness_history = []

    def initialize_population(self):
        self.population = [
            Chromosome(self.environment)
            for _ in range(self.population_size)
        ]

    def evaluate(self, chromosome):
        return calculate_fitness(chromosome, self.environment)

    def selection(self):
        candidates = random.sample(
            self.population,
            min(self.tournament_size, len(self.population))
        )
        return max(candidates, key=self.evaluate)

    def crossover(self, parent1, parent2):
        child = Chromosome(self.environment)

        route1 = parent1.waypoints
        route2 = parent2.waypoints

        if random.random() < self.crossover_rate:
            point = random.randint(1, len(route1) - 1)
            new_route = route1[:point] + route2[point:]
        else:
            new_route = route1[:]

        child.waypoints = [
            waypoint.copy() for waypoint in new_route
        ]

        return child

    def mutation(self, chromosome):
        valid_cells = [
            (x, y)
            for x in range(self.environment.grid_size)
            for y in range(self.environment.grid_size)
            if (x, y) not in self.environment.obstacles
        ]

        for waypoint in chromosome.waypoints:

            if random.random() < self.mutation_rate:
                x, y = random.choice(valid_cells)
                waypoint["x"] = x
                waypoint["y"] = y

            if random.random() < self.mutation_rate:
                waypoint["speed"] = round(
                    random.uniform(1.0, 3.0), 2
                )

            if random.random() < self.mutation_rate:
                waypoint["sensor_power"] = round(
                    random.uniform(0.5, 1.0), 2
                )

            if random.random() < self.mutation_rate:
                waypoint["sensor_on"] = random.randint(0, 1)

        return chromosome

    def run(self):
        self.initialize_population()

        for generation in range(self.generations):

            scores = [
                self.evaluate(chromosome)
                for chromosome in self.population
            ]

            best_score = max(scores)
            average_score = sum(scores) / len(scores)

            self.best_fitness_history.append(best_score)
            self.average_fitness_history.append(average_score)

            if generation % 10 == 0:
                print(
                    f"Generation {generation}: "
                    f"Best Fitness = {best_score:.3f}, "
                    f"Average Fitness = {average_score:.3f}"
                )

            ranked_population = sorted(
                self.population,
                key=self.evaluate,
                reverse=True
            )

            new_population = []

            # Preserve the best chromosomes (elitism)
            for chromosome in ranked_population[:self.elite_size]:
                elite = Chromosome(self.environment)
                elite.waypoints = [
                    waypoint.copy()
                    for waypoint in chromosome.waypoints
                ]
                new_population.append(elite)

            # Create the remaining population
            while len(new_population) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()

                child = self.crossover(parent1, parent2)
                self.mutation(child)

                new_population.append(child)

            self.population = new_population

        # Select the best chromosome from the final population
        best_solution = max(
            self.population,
            key=self.evaluate
        )

        print("\nGenetic Algorithm Completed!")
        print(
            f"Final Best Fitness: "
            f"{self.evaluate(best_solution):.3f}"
        )

        return best_solution

    def plot_fitness(self):
        plt.figure(figsize=(10, 6))

        plt.plot(
            self.best_fitness_history,
            label="Best Fitness",
            linewidth=2
        )

        plt.plot(
            self.average_fitness_history,
            label="Average Fitness",
            linewidth=2
        )

        plt.xlabel("Generation")
        plt.ylabel("Fitness Score")
        plt.title("Genetic Algorithm Fitness Convergence")

        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        plt.savefig("fitness_convergence.png", dpi=300)
        plt.show()


if __name__ == "__main__":
    environment = Environment()

    ga = GeneticAlgorithm(
        environment=environment,
        population_size=50,
        generations=100,
        mutation_rate=0.10,
        crossover_rate=0.80,
        elite_size=2,
        tournament_size=3
    )

    best_solution = ga.run()

    ga.plot_fitness()

    plot_drone_path(environment, best_solution)

    plot_coverage(environment, best_solution)

    print("\nBest Drone Flight Plan:")
    best_solution.display()
