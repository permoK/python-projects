# -*- coding: utf-8 -*-
"""Delivery_routes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oKDEa4X6LDm-3z-LS_oAdZV3CIRX6TCw
"""

# !pip install deap

import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools
from tqdm import tqdm

# problem parameters
num_customers = 50
customer_coords = np.random.uniform(0, 100, size=(num_customers, 2))
customer_demands = np.random.uniform(1, 10, size=num_customers)
time_windows = [(np.random.uniform(0, 4), np.random.uniform(4, 8)) for _ in range(num_customers)]
vehicle_capacity = 50
num_vehicles = 5
max_route_duration = 10

# Define objective functions
def obj1(routing, costs):
    # Minimize total costs
    return sum(costs)

def obj2(routing, freshness):
    # Maximize customer satisfaction in terms of product freshness
    return -np.mean(freshness)

def obj3(routing, time_penalties):
    # Minimize time penalty costs
    return sum(time_penalties)
def evaluate_solution(individual):
    # Decode individual to routing and compute objectives
    routing = decode_individual(individual)
    costs, freshness, time_penalties = compute_objectives(routing)
    return obj1(routing, costs), obj2(routing, freshness), obj3(routing, time_penalties)

# Define NSGA-II algorithm
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=num_customers)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate_solution)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)



def decode_individual(individual):
    # Decode individual to routing
    routing = []
    current_vehicle = 0
    current_load = 0
    current_time = 0
    route = []
    for i, x in enumerate(individual):
        if x == 1:
            if current_load + customer_demands[i] <= vehicle_capacity and current_time + travel_time(customer_coords[i]) <= max_route_duration:
                route.append(i)
                current_load += customer_demands[i]
                current_time += travel_time(customer_coords[i])
            else:
                routing.append(route)
                route = [i]
                current_vehicle += 1
                current_load = customer_demands[i]
                current_time = travel_time(customer_coords[i])
    if route:
        routing.append(route)
    return routing

def compute_objectives(routing):
    # Compute objective function values
    costs = []
    freshness = []
    time_penalties = []
    for route in routing:
        cost, freshness_score, time_penalty = compute_route_metrics(route)
        costs.append(cost)
        freshness.append(freshness_score)
        time_penalties.append(time_penalty)
    return costs, freshness, time_penalties

def compute_route_metrics(route):
    # Compute cost, freshness, and time penalty for a route
    cost = 0
    freshness_score = 0
    time_penalty = 0
    for i in range(len(route)):
        # Compute cost, freshness, and time penalty for each customer in the route
        pass
    return cost, freshness_score, time_penalty

def travel_time(coords):
    # Compute travel time between two coordinates
    return np.sqrt(np.sum((coords[0] - coords[1])**2))

# Run NSGA-II
pop = toolbox.population(n=100)
fits = [toolbox.evaluate(ind) for ind in pop]
for ind, fit in zip(pop, fits):
    ind.fitness.values = fit

NGEN = 200
for g in tqdm(range(NGEN)):
    # Select the next generation individuals
    offspring = toolbox.select(pop, len(pop))
    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if np.random.rand() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    for mutant in offspring:
        if np.random.rand() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # The population is entirely replaced by the offspring
    pop[:] = offspring

# Post-processing and visualization
pareto_front = tools.ParetoFront()
pareto_front.update(pop)


# Visualize optimal vehicle routes
best_routing = decode_individual(pareto_front[0])
plt.figure(figsize=(8, 6))
plt.scatter(customer_coords[:, 0], customer_coords[:, 1])
for route in best_routing:
    if route:  # Check if the route is not empty
        route_coords = [customer_coords[i] for i in route]
        x, y = zip(*route_coords)
        plt.plot(x, y, linewidth=2)
plt.title('Optimal Vehicle Routes')
plt.show()

