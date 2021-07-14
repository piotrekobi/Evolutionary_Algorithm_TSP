# Created by Piotr Paturej

import random
import math


def initialise_cities(num_cities):
    x_coords = random.sample(range(1, 100), num_cities)
    y_coords = random.sample(range(1, 100), num_cities)
    cities = [(i, x_coords[i], y_coords[i]) for i in range(num_cities)]
    return cities


def initialise_population(num_cities, pop_size):
    population = [list(range(num_cities)) for i in range(pop_size)]
    for individual in population:
        random.shuffle(individual)
    return population


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def calculate_distances(route, cities):
    distances = []
    for i in range(len(route) - 1):
        current_city = (cities[route[i]][1], cities[route[i]][2])
        next_city = (cities[route[i + 1]][1], cities[route[i + 1]][2])
        distances.append(round(distance(current_city, next_city), 3))

    last_city = (cities[route[len(route) - 1]][1], cities[route[len(route) - 1]][2])
    first_city = (cities[route[0]][1], cities[route[0]][2])
    distances.append(round(distance(last_city, first_city), 3))
    return distances


def select_competitively(pop, cities):
    selection = []
    half_num_pop = len(pop) // 2
    for i in range(half_num_pop):
        route_1_length = sum(calculate_distances(pop[i], cities))
        route_2_length = sum(calculate_distances(pop[i + half_num_pop], cities))
        if route_1_length < route_2_length:
            selection.append(pop[i])
        else:
            selection.append(pop[i + half_num_pop])
    return selection


def mutate(route, num_cities):
    indices_to_swap = random.sample(range(num_cities), 4)
    mutation_1 = route.copy()
    mutation_2 = route.copy()
    mutation_1[indices_to_swap[0]], mutation_1[indices_to_swap[1]] = (
        mutation_1[indices_to_swap[1]],
        mutation_1[indices_to_swap[0]],
    )
    mutation_2[indices_to_swap[2]], mutation_2[indices_to_swap[3]] = (
        mutation_2[indices_to_swap[3]],
        mutation_2[indices_to_swap[2]],
    )
    return mutation_1, mutation_2


def evolutionary_shortest_route(population, iterations, cities):
    num_cities = len(cities)
    for _ in range(iterations):
        selected_routes = select_competitively(population, cities)
        new_population = selected_routes.copy()
        for route in selected_routes:
            mutations = mutate(route, num_cities)
            mutation_1_score = sum(calculate_distances(mutations[0], cities))
            mutation_2_score = sum(calculate_distances(mutations[1], cities))
            if mutation_1_score < mutation_2_score:
                new_population.append(mutations[0])
            else:
                new_population.append(mutations[1])

        route_lengths = []
        for route in population:
            route_lengths.append(round(sum(calculate_distances(route, cities)), 3))
        shortest_route_length = min(route_lengths)
        shortest_route = population[route_lengths.index(shortest_route_length)]
        population = new_population
    return shortest_route, shortest_route_length
