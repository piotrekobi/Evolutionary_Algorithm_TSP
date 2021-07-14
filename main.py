# Created by Piotr Paturej

from evolutionary_algorithm import evolutionary_shortest_route
from evolutionary_algorithm import initialise_cities, initialise_population
import matplotlib.pyplot as plt
import json


def plot_route(route):
    plot_cities = [cities[index] for index in route]
    city_x_coords = [city[1] for city in plot_cities]
    city_y_coords = [city[2] for city in plot_cities]
    plt.scatter(city_x_coords, city_y_coords, s=250)
    plt.plot(city_x_coords, city_y_coords)
    for i in range(len(plot_cities) - 1):
        plt.text(
            city_x_coords[i],
            city_y_coords[i],
            i,
            horizontalalignment="center",
            verticalalignment="center",
            size=10,
            c="white",
        )
    # plt.savefig("graph")
    plt.show()


def average_route_length(num_cities, num_population, iterations):
    sum = 0
    for i in range(20):
        sum += evolutionary_shortest_route(population, iterations, cities)[1]
    return sum / 20


num_cities = 20
num_population = 50
iterations = 1000
start_city = 0

try:
    with open(f"cities_{num_cities}.json", "r") as f:
        cities = json.load(f)
except FileNotFoundError:
    cities = initialise_cities(num_cities)

population = initialise_population(num_cities, num_population)

# print(average_route_length(num_cities, num_population, iterations))

shortest_route_info = evolutionary_shortest_route(population, iterations,
                                                  cities)
shortest_route = shortest_route_info[0]
shortest_route_length = shortest_route_info[1]

start_index = shortest_route.index(start_city)
shortest_route = shortest_route[start_index:] + shortest_route[:start_index]
shortest_route.append(start_city)
print(f"Shortest route: {shortest_route}")
print(f"Shortest route length: {shortest_route_length}")
plot_route(shortest_route)
