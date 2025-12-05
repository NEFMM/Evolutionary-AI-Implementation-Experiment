# ============================================================
#  Algoritmo Genético – Visualização em Gráficos
#  Problema: Minimizar a espessura de isolamento t
#  com restrição Q(k,t) <= 120 W e k <= 0.084 W/m.K
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# ---------- PARÂMETROS FÍSICOS ----------
r1 = 0.5          # raio interno [m]
L = 2.0            # comprimento [m]
dT = 180            # diferença de temperatura [°C]
Q_max = 120.0      # limite máximo de fluxo de calor [W]
k_max = 0.084      # limite máximo da condutividade [W/m.K]

# ---------- FUNÇÃO DE CÁLCULO DO CALOR ----------
def heat_flow(k, t):
    """
    Fluxo de calor radial em um cilindro com isolamento:

    Q = 2 * pi * k * L * dT / ln(r2/r1)
    """
    r2 = r1 + t
    return (2 * np.pi * k * L * dT) / np.log(r2 / r1)

# ---------- FUNÇÃO OBJETIVO ----------
def objective(individual, penalty_factor=1e4):

    k, t = individual

    Q = heat_flow(k, t)
    fitness = t  # queremos espessura t a menor possível

    # Penalidade se Q passar do limite
    if Q > Q_max:
        fitness += penalty_factor * (Q - Q_max)**2

    # Penalidade se k passar do limite
    if k > k_max:
        fitness += penalty_factor * (k - k_max)**2

    return fitness

# ---------- ALGORITMO GENÉTICO ----------
def run_GA(
    bounds,
    pop_size=50,
    generations=100,
    crossover_rate=0.8,
    mutation_rate=0.3,
    mutation_scale=0.3,
    penalty_factor=1e4,
    seed=42
):
    """
    bounds: [(k_min, k_max), (t_min, t_max)]
    """

    np.random.seed(seed)
    n_var = len(bounds)

    # População inicial
    population = np.zeros((pop_size, n_var))
    for i in range(n_var):
        low, high = bounds[i]
        population[:, i] = np.random.uniform(low, high, size=pop_size)

    def evaluate(pop):
        return np.array([objective(ind, penalty_factor) for ind in pop])

    fitness = evaluate(population)

    best_hist = []
    worst_hist = []
    avg_hist = []

    # novos históricos para melhor t e melhor Q
    best_t_hist = []
    best_Q_hist = []

    for gen in range(generations):
        new_population = []

        # Estatísticas da geração
        best_idx = np.argmin(fitness)
        best_ind = population[best_idx].copy()
        best_fit = fitness[best_idx]

        best_hist.append(best_fit)
        worst_hist.append(fitness.max())
        avg_hist.append(fitness.mean())

        # registra melhor t e Q da geração
        best_k_gen, best_t_gen = best_ind
        best_Q_gen = heat_flow(best_k_gen, best_t_gen)
        best_t_hist.append(best_t_gen)
        best_Q_hist.append(best_Q_gen)

        # Elitismo: mantém o melhor indivíduo
        new_population.append(best_ind)

        # Função de seleção por torneio (2 indivíduos)
        def tournament_selection():
            i1, i2 = np.random.randint(0, pop_size, size=2)
            return population[i1] if fitness[i1] < fitness[i2] else population[i2]

        # Gerar o restante da população
        while len(new_population) < pop_size:
            parent1 = tournament_selection().copy()
            parent2 = tournament_selection().copy()

            # Crossover
            if np.random.rand() < crossover_rate:
                alpha = np.random.rand()
                child1 = alpha * parent1 + (1 - alpha) * parent2
                child2 = (1 - alpha) * parent1 + alpha * parent2
            else:
                child1 = parent1.copy()
                child2 = parent2.copy()

            # Mutação
            for child in (child1, child2):
                for i in range(n_var):
                    if np.random.rand() < mutation_rate:
                        low, high = bounds[i]
                        var_range = high - low
                        child[i] += np.random.normal(0, mutation_scale * var_range)
                        child[i] = np.clip(child[i], low, high)

                new_population.append(child)
                if len(new_population) >= pop_size:
                    break

        population = np.array(new_population)
        fitness = evaluate(population)

    # Resultado final
    best_idx = np.argmin(fitness)
    best_ind = population[best_idx]
    best_fit = fitness[best_idx]

    return {
        "best_individual": best_ind,
        "best_fitness": best_fit,
        "best_hist": np.array(best_hist),
        "worst_hist": np.array(worst_hist),
        "avg_hist": np.array(avg_hist),
        "best_t_hist": np.array(best_t_hist),
        "best_Q_hist": np.array(best_Q_hist),
    }

# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    # Variáveis de projeto: [k, t]
    # k de 0.02 até k_max; t de 0.005 m a 0.08 m
    bounds = [
        (0.02, k_max),
        (0.005, 0.08)
    ]

    result = run_GA(bounds=bounds)

    best_k, best_t = result["best_individual"]
    best_Q = heat_flow(best_k, best_t)

    print("==== Resultado do GA ====")
    print(f"Melhor k encontrado  : {best_k:.5f} W/m.K")
    print(f"Melhor t encontrado  : {best_t*1000:.3f} mm")
    print(f"Q(k,t)               : {best_Q:.3f} W")
    print(f"Restrição Q <= {Q_max} W -> {'OK' if best_Q <= Q_max else 'VIOLADA'}")

    generations = np.arange(len(result["best_hist"]))

    # ---------- GRÁFICO 1: melhor, média e pior fitness ----------
    plt.figure(figsize=(8, 5))
    plt.plot(generations, result["best_hist"], label="Melhor (mínimo)")
    plt.plot(generations, result["avg_hist"], label="Média", linestyle="--")
    plt.plot(generations, result["worst_hist"], label="Pior (máximo)", linestyle=":")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("GA – melhor e pior fitness")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

