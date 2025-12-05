import numpy as np
import matplotlib.pyplot as plt   # <--- IMPORT PARA GRÁFICOS

# ============================================
#  PARÂMETROS FÍSICOS DO PROBLEMA
# ============================================
r_i = 0.03        # raio interno [m] (30 mm)
L   = 1.0         # comprimento [m]
T_i = 500.0       # temperatura interna [°C]
T_inf = 75.0      # temperatura externa [°C]
dT  = T_i - T_inf

# Coeficiente de convecção externo (ajuste se o professor deu outro)
h = 10.0          # [W/m².K] (exemplo)

# Limite de calor
Q_max = 120.0     # [W]
# ============================================  
# Faixas de busca para t e k 
t_min, t_max = 0.025, 0.200   # [m] 25 mm a 200 mm
k_min, k_max = 0.050, 0.084   # [W/m.K] (intervalo típico de materiais isolantes)


# ============================================
#  FUNÇÃO DE CÁLCULO DO CALOR (Eq. 1)
#  Q = 2π L ΔT / [ ln(r_o/r_i)/k + 1/(h r_o) ]
# ============================================
def heat_flow(k, t):
    r_o = r_i + t
    denom = np.log(r_o / r_i) / k + 1.0 / (h * r_o)
    return 2.0 * np.pi * L * dT / denom


# ============================================
#  FUNÇÃO DE FITNESS
#  - Queremos t pequeno e k pequeno
#  - Mas Q(k,t) <= Q_max
#  -> multiobjetivo simplificado: minimizar t_norm + k_norm
# ============================================
def fitness(individual, penalty_factor=1e6):
    t, k = individual

    # Repara limites (se fugir, fitness bem ruim)
    if not (t_min <= t <= t_max) or not (k_min <= k <= k_max):
        return 1e9

    Q = heat_flow(k, t)

    # Normalização simples de t e k para 0–1
    t_norm = (t - t_min) / (t_max - t_min)
    k_norm = (k - k_min) / (k_max - k_min)

    base_obj = t_norm + k_norm  # quanto menor, melhor (camada fina + material bom)

    # Penaliza se ultrapassar Q_max
    if Q > Q_max:
        penalty = (Q - Q_max)**2 * penalty_factor
    else:
        penalty = 0.0

    return base_obj + penalty


# ============================================
#  OPERADORES DO GA
# ============================================
def init_population(pop_size):
    """
    Cromossomo: [t, k]
    """
    pop = np.zeros((pop_size, 2))
    pop[:, 0] = np.random.uniform(t_min, t_max, size=pop_size)  # t
    pop[:, 1] = np.random.uniform(k_min, k_max, size=pop_size)  # k
    return pop

def tournament_selection(pop, fitnesses, k_tour=3):
    idxs = np.random.randint(0, len(pop), size=k_tour)
    best_idx = idxs[np.argmin(fitnesses[idxs])]
    return pop[best_idx].copy()

def crossover(parent1, parent2, pc=0.9):
    """
    Crossover aritmético em cada gene (t e k)
    """
    c1, c2 = parent1.copy(), parent2.copy()
    if np.random.rand() < pc:
        alpha = np.random.rand()
        c1 = alpha * parent1 + (1 - alpha) * parent2
        c2 = alpha * parent2 + (1 - alpha) * parent1
    return c1, c2

def mutate(individual, pm=0.1, sigma_t=0.005, sigma_k=0.002):
    """
    Mutação gaussiana em t e k
    """
    t, k = individual

    if np.random.rand() < pm:
        t += np.random.normal(0, sigma_t)
    if np.random.rand() < pm:
        k += np.random.normal(0, sigma_k)

    # Garante dentro dos limites
    t = np.clip(t, t_min, t_max)
    k = np.clip(k, k_min, k_max)

    individual[0], individual[1] = t, k
    return individual


# ============================================
#  LOOP PRINCIPAL DO GA (k e t OTIMIZADOS JUNTOS)
#  + HISTÓRICO PARA PLOTAR GRÁFICOS
#  + MELHOR / PIOR / MÉDIA DA POPULAÇÃO
# ============================================
def run_GA(
    pop_size=16,
    generations=100,
    pc=0.9,
    pm=0.1,
    penalty_factor=1e6,
    verbose=True
):
    pop = init_population(pop_size)
    fitnesses = np.array([fitness(ind, penalty_factor) for ind in pop])

    # Listas pra salvar evolução do MELHOR indivíduo
    best_t_hist = []
    best_k_hist = []
    best_Q_hist = []

    # Listas pra MELHOR, PIOR e MÉDIA de fitness da população
    best_fit_hist  = []
    worst_fit_hist = []
    mean_fit_hist  = []

    for gen in range(generations):
        new_pop = []

        # Estatísticas da população nesta geração
        best_idx   = np.argmin(fitnesses)
        worst_idx  = np.argmax(fitnesses)
        best_fit   = fitnesses[best_idx]
        worst_fit  = fitnesses[worst_idx]
        mean_fit   = np.mean(fitnesses)

        best_ind = pop[best_idx].copy()

        # Salva histórico desta geração
        t_best, k_best = best_ind
        Q_best = heat_flow(k_best, t_best)

        best_t_hist.append(t_best)
        best_k_hist.append(k_best)
        best_Q_hist.append(Q_best)

        best_fit_hist.append(best_fit)
        worst_fit_hist.append(worst_fit)
        mean_fit_hist.append(mean_fit)

        # Elitismo: guarda o melhor
        new_pop.append(best_ind)

        # Gera o resto
        while len(new_pop) < pop_size:
            p1 = tournament_selection(pop, fitnesses)
            p2 = tournament_selection(pop, fitnesses)

            c1, c2 = crossover(p1, p2, pc=pc)
            c1 = mutate(c1, pm=pm)
            c2 = mutate(c2, pm=pm)

            new_pop.append(c1)
            if len(new_pop) < pop_size:
                new_pop.append(c2)

        pop = np.array(new_pop)
        fitnesses = np.array([fitness(ind, penalty_factor) for ind in pop])

        if verbose and (gen % 10 == 0 or gen == generations - 1):
            print(
                f"Geração {gen:3d} | "
                f"t* = {t_best*1000:.2f} mm | "
                f"k* = {k_best:.5f} W/m.K | "
                f"Q(t*,k*) = {Q_best:.3f} W | "
                f"BestFit = {best_fit:.3e} | "
                f"MeanFit = {mean_fit:.3e} | "
                f"WorstFit = {worst_fit:.3e}"
            )

    # Resultado final
    best_idx = np.argmin(fitnesses)
    t_best, k_best = pop[best_idx]
    Q_best = heat_flow(k_best, t_best)

    print("\n===== RESULTADO FINAL DO GA (k e t) =====")
    print(f"Espessura ótima t* : {t_best*1000:.3f} mm")
    print(f"Condutividade ótima k*: {k_best:.5f} W/m.K")
    print(f"Fluxo de calor Q(t*,k*): {Q_best:.3f} W (limite {Q_max} W)")

    history = {
        "t": np.array(best_t_hist),
        "k": np.array(best_k_hist),
        "Q": np.array(best_Q_hist),
        "best_fit":  np.array(best_fit_hist),
        "mean_fit":  np.array(mean_fit_hist),
        "worst_fit": np.array(worst_fit_hist),
    }
    return t_best, k_best, Q_best, history


# ============================================
#  EXECUTAR + PLOTAR GRÁFICOS
# ============================================
if __name__ == "__main__":
    t_best, k_best, Q_best, history = run_GA(
        pop_size=16,
        generations=100,
        pc=0.9,
        pm=0.1,
        penalty_factor=1e6,
        verbose=True
    )

    gens = np.arange(len(history["best_fit"]))

    # Gráfico 1: Fitness (melhor, média, pior)
    plt.figure(figsize=(8, 5))
    plt.plot(gens, history["best_fit"],  label="Melhor fitness")
    plt.plot(gens, history["mean_fit"],  label="Média da população")
    plt.plot(gens, history["worst_fit"], label="Pior fitness")
    plt.xlabel("Geração")
    plt.ylabel("Fitness")
    plt.title("Convergência do GA - Melhor, Média e Pior Fitness")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Gráfico 2: t e k
    plt.figure(figsize=(8, 5))
    plt.plot(gens, history["t"] * 1000, label="t (mm)")
    plt.plot(gens, history["k"],         label="k (W/m.K)")
    plt.xlabel("Geração")
    plt.ylabel("Valores")
    plt.title("Evolução de t e k do melhor indivíduo")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Gráfico 3: Q
    plt.figure(figsize=(8, 5))
    plt.plot(gens, history["Q"], label="Q(k,t)")
    plt.axhline(Q_max, linestyle="--", label="Q_max = 120 W")
    plt.xlabel("Geração")
    plt.ylabel("Fluxo de calor [W]")
    plt.title("Evolução do fluxo de calor Q(k,t)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()
