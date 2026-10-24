
import random
import time

from enviroment import Environment
from chromosome import Chromosome
from fitness import calculate_fitness


def run_random_search(environment, number_of_trials=5000):
    best_chromosome = None
    best_fitness = float("-inf")
    fitness_history = []

    start_time = time.time()

    for trial in range(number_of_trials):
        # Generate a completely random flight plan
        chromosome = Chromosome(environment)

        # Evaluate its fitness
        fitness = calculate_fitness(chromosome, environment)
        fitness_history.append(fitness)

        # Keep the best solution found
        if fitness > best_fitness:
            best_fitness = fitness
            best_chromosome = chromosome

        if (trial + 1) % 500 == 0:
            print(
                f"Trial {trial + 1}: "
                f"Best Fitness = {best_fitness:.3f}"
            )

    elapsed_time = time.time() - start_time

    print("\nRandom Search Completed!")
    print(f"Trials: {number_of_trials}")
    print(f"Best Fitness: {best_fitness:.3f}")
    print(f"Execution Time: {elapsed_time:.2f} seconds")

    return best_chromosome, best_fitness, fitness_history


if __name__ == "__main__":
    random.seed(42)

    environment = Environment()

    best_solution, best_score, history = run_random_search(
        environment,
        number_of_trials=5000
    )

    print("\nBest Random Flight Plan:")
    best_solution.display()
