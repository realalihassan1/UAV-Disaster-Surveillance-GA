
import random
import matplotlib.pyplot as plt

from enviroment import Environment
from genetic_algorithm import GeneticAlgorithm
from random_search import run_random_search


def compare_algorithms():
    environment = Environment()

    population_size = 50
    generations = 100
    random_trials = population_size * generations

    # Run Genetic Algorithm
    print("Running Genetic Algorithm...")
    random.seed(42)

    ga = GeneticAlgorithm(
        environment=environment,
        population_size=population_size,
        generations=generations,
        mutation_rate=0.10,
        crossover_rate=0.80,
        elite_size=2,
        tournament_size=3
    )

    ga.run()

    ga_fitness = ga.best_fitness_history

    # Run Random Search with the same number of candidates
    print("\nRunning Random Search...")
    random.seed(42)

    _, random_best, random_history = run_random_search(
        environment,
        number_of_trials=random_trials
    )

    # Convert random results into cumulative best fitness
    cumulative_best = []
    current_best = float("-inf")

    for score in random_history:
        current_best = max(current_best, score)
        cumulative_best.append(current_best)

    # Plot comparison
    ga_evaluations = [
        population_size * (i + 1)
        for i in range(len(ga_fitness))
    ]

    random_evaluations = list(
        range(1, len(cumulative_best) + 1)
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        ga_evaluations,
        ga_fitness,
        label="Genetic Algorithm",
        linewidth=2
    )

    plt.plot(
        random_evaluations,
        cumulative_best,
        label="Random Search",
        linewidth=2
    )

    plt.xlabel("Approximate Candidate Evaluations")
    plt.ylabel("Best Fitness Found")
    plt.title("Genetic Algorithm vs Random Search")

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("ga_vs_random_search.png", dpi=300)
    plt.show()

    print("\nComparison Results")
    print("------------------")
    print(f"GA Best Fitness: {max(ga_fitness):.3f}")
    print(f"Random Search Best Fitness: {random_best:.3f}")


if __name__ == "__main__":
    compare_algorithms()
