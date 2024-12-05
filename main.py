# main.py
from tree import City, Map
from aStar_mst import aStarMST
from aStar_ACO import aStarACO
from aStar_combined import aStarCombined

import time
import random
import matplotlib.pyplot as plt


def generate_cities(num_cities: int, grid_size: int = 1000) -> list:
    cities = []
    for i in range(num_cities):
        x = random.randint(0, grid_size)
        y = random.randint(0, grid_size)
        cities.append(City(name=f"C{i}", coordinates=(x, y)))
    return cities

def evaluate_algorithms(cities: list, start_city: str, aco_iterations: int = 100):
    map_obj = Map(cities=cities)
    
    # A* con MST
    start_time = time.time()
    solution_mst = aStarMST(map_obj, start_city)
    end_time = time.time()
    time_mst = end_time - start_time
    cost_mst = solution_mst.state.cost if solution_mst else float('inf')
    
    # A* con ACO
    start_time = time.time()
    solution_aco = aStarACO(map_obj, start_city, iterations=aco_iterations)
    end_time = time.time()
    time_aco = end_time - start_time
    cost_aco = solution_aco.state.cost if solution_aco else float('inf')
    
    # A* con heurísticas combinadas
    start_time = time.time()
    solution_combined = aStarCombined(map_obj, start_city, iterations=aco_iterations)
    end_time = time.time()
    time_combined = end_time - start_time
    cost_combined = solution_combined.state.cost if solution_combined else float('inf')
    
    return {
        'MST': {'time': time_mst, 'cost': cost_mst},
        'ACO': {'time': time_aco, 'cost': cost_aco},
        'Combined': {'time': time_combined, 'cost': cost_combined}
    }

def main():
    num_cities_list = [5, 10, 15, 20]  # Puedes ajustar los tamaños
    results = {'MST': [], 'ACO': [], 'Combined': []}
    
    for num_cities in num_cities_list:
        print(f"Evaluando con {num_cities} ciudades...")
        cities = generate_cities(num_cities)
        start_city = cities[0].name
        res = evaluate_algorithms(cities, start_city)
        results['MST'].append((num_cities, res['MST']['time'], res['MST']['cost']))
        results['ACO'].append((num_cities, res['ACO']['time'], res['ACO']['cost']))
        results['Combined'].append((num_cities, res['Combined']['time'], res['Combined']['cost']))
    
    # Mostrar resultados
    for key in results:
        print(f"\nResultados para {key}:")
        for entry in results[key]:
            print(f"Ciudades: {entry[0]}, Tiempo: {entry[1]:.4f}s, Costo: {entry[2]:.2f}")
    
    # Graficar resultados
    plt.figure(figsize=(12, 6))
    
    # Tiempo de ejecución
    plt.subplot(1, 2, 1)
    for key in results:
        plt.plot([x[0] for x in results[key]], [x[1] for x in results[key]], label=key)
    plt.xlabel('Número de Ciudades')
    plt.ylabel('Tiempo de Ejecución (s)')
    plt.title('Tiempo de Ejecución vs Número de Ciudades')
    plt.legend()
    
    # Costo de la solución
    plt.subplot(1, 2, 2)
    for key in results:
        plt.plot([x[0] for x in results[key]], [x[2] for x in results[key]], label=key)
    plt.xlabel('Número de Ciudades')
    plt.ylabel('Costo de la Solución')
    plt.title('Costo de la Solución vs Número de Ciudades')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
