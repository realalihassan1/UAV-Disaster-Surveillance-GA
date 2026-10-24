
import matplotlib.pyplot as plt

def plot_fitness(best_history, average_history):
    plt.figure(figsize=(10, 6))

    plt.plot(best_history, label="Best Fitness", linewidth=2)
    plt.plot(average_history, label="Average Fitness", linewidth=2)

    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.title("Genetic Algorithm Fitness Convergence")

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("fitness_convergence.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    print("Run genetic_algorithm.py first, then connect this file to the GA.")

