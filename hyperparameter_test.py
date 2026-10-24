
import random
import statistics
import matplotlib.pyplot as plt

from enviroment import Environment
from genetic_algorithm import GeneticAlgorithm


def test_mutation_rates():
    environment = Environment()

    mutation_rates = [0.05, 0.10, 0.20]
    population_size = 30
    generations = 50
    repeats = 3

    results = {}

    for rate in mutation_rates:
        scores = []

        print(f"\nTesting mutation rate: {rate}")

        for run in range(repeats):
            random.seed(100 + run)

            ga = GeneticAlgorithm(
                environment=environment,
                population_size=population_size,
                generations=generations,
                mutation_rate=rate,
                crossover_rate=0.80,
                elite_size=2,
                tournament_size=3
            )

            best_solution = ga.run()
            best_score = ga.evaluate(best_solution)
            scores.append(best_score)

            print(
                f"Run {run + 1}: "
                f"Best fitness = {best_score:.3f}"
            )

        results[rate] = scores

    # Calculate mean and standard deviation
    means = [
        statistics.mean(results[rate])
        for rate in mutation_rates
    ]

    deviations = [
        statistics.stdev(results[rate])
        for rate in mutation_rates
    ]

    print("\nHYPERPARAMETER RESULTS")
    print("-" * 40)

    for rate in mutation_rates:
        print(
            f"Mutation rate {rate:.2f}: "
            f"Mean = {statistics.mean(results[rate]):.3f}, "
            f"Std Dev = {statistics.stdev(results[rate]):.3f}"
        )

    # Plot results
    plt.figure(figsize=(9, 6))

    plt.errorbar(
        mutation_rates,
        means,
        yerr=deviations,
        marker="o",
        capsize=5,
        linewidth=2
    )

    plt.xlabel("Mutation Rate")
    plt.ylabel("Final Best Fitness")
    plt.title("Mutation Rate Sensitivity Analysis")
    plt.xticks(mutation_rates)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig("hyperparameter_sensitivity.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    test_mutation_rates()
