import random

# --- Title ---
print("Genetic Algorithm - Delivery Route Optimisation\n")

# Distance matrix (A=0, B=1, C=2, D=3, E=4, F=5, G=6)
distances = [
    [0, 4, 8, 6, 7, 9, 5],  # A
    [4, 0, 5, 7, 3, 8, 6],  # B
    [8, 5, 0, 4, 6, 3, 7],  # C
    [6, 7, 4, 0, 5, 6, 8],  # D
    [7, 3, 6, 5, 0, 4, 6],  # E
    [9, 8, 3, 6, 4, 0, 5],  # F
    [5, 6, 7, 8, 6, 5, 0],  # G
]
cities = ["A", "B", "C", "D", "E", "F", "G"]
idx = {c: i for i, c in enumerate(cities)}
depot = "A"
delivery = ["B", "C", "D", "E", "F", "G"]

random.seed(42)  # fixed seed for reproducibility

POP_SIZE = 100
GENERATIONS = 100
MUTATION_RATE = 0.2
ELITE_SIZE = 2

print(f"Seed 42 | population {POP_SIZE} | generations {GENERATIONS}\n")

def route_distance(route):
    """Total distance: depot -> deliveries -> depot."""
    full = [depot] + route + [depot]
    return sum(distances[idx[full[i]]][idx[full[i + 1]]]
               for i in range(len(full) - 1))

def random_route():
    r = delivery[:]
    random.shuffle(r)
    return r

def initial_population():
    return [random_route() for _ in range(POP_SIZE)]

def tournament_selection(pop):
    """Pick the best of 3 random candidates."""
    candidates = random.sample(pop, 3)
    return min(candidates, key=route_distance)

def order_crossover(p1, p2):
    """Order-preserving crossover -> valid child, no duplicates."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b + 1] = p1[a:b + 1]
    fill = [c for c in p2 if c not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[j]
            j += 1
    return child

def swap_mutation(route):
    """Swap two random positions -> valid route."""
    r = route[:]
    i, j = random.sample(range(len(r)), 2)
    r[i], r[j] = r[j], r[i]
    return r

def genetic_algorithm():
    pop = initial_population()
    best = min(pop, key=route_distance)

    for gen in range(GENERATIONS):
        # Elitism: keep best routes unchanged
        pop.sort(key=route_distance)
        new_pop = pop[:ELITE_SIZE]

        while len(new_pop) < POP_SIZE:
            parent1 = tournament_selection(pop)
            parent2 = tournament_selection(pop)
            child = order_crossover(parent1, parent2)
            if random.random() < MUTATION_RATE:
                child = swap_mutation(child)
            new_pop.append(child)

        pop = new_pop
        current_best = min(pop, key=route_distance)
        if route_distance(current_best) < route_distance(best):
            best = current_best

    return best, route_distance(best)

# Run the GA
best_route, best_distance = genetic_algorithm()

# Print final result
print("Best route found:", "A ->", " -> ".join(best_route), "-> A")
print("Total distance:", best_distance, "km")