from tree import City, Map
from typing import List
import random

#Class that represents an ant
class Ant:
  #Constructor
  def __init__(self, map: Map, start: City):
    self.map = map
    self.start = start
    self.reset()
  
  #Method that resets the ant  
  def reset(self):
    self.currentCity = self.start
    self.visited = set([self.start.name])
    self.path = [self.start.name]
    self.totalCoast = 0.0
    
  #Method that makes the ant visit a city  
  def visitCity(self, city: City):
    self.currentCity = city
    self.visited.add(city.name)
    self.path.append(city.name)
    #If the ant has visited at least two cities
    # add the distance between the last two cities to the total coast
    self.totalCoast += self.map.get_distance(self.path[-2], city.name)
    
def ACO_heuristic(map: Map, iterations : int = 100, alpha : float = 1.0, beta: float = 5.0) -> float:
  #initialize the pheromone matrix
  pheromones = {(city1.name, city2.name): 1.0 for city1 in map.cities for city2 in map.cities if city1 != city2}
  
  for _ in range(iterations):
    #initialize the ants
    ants = [Ant(map,random.choice(map.cities)) for _ in range(len(map.cities))]
    for ant in ants:
      ant.reset()
      while len(ant.visited) < len(map.cities):
        current = ant.currentCity
        #calculate the probability of visiting each city
        probabilities = []
        total = 0.0
        #this for loop calculates the probability of visiting each city
        for city in map.cities:
          #if the city has not been visited
          if city.name not in ant.visited:
            #calculate the probability of visiting the city
            pheromone = pheromones[(current.name, city.name)]
            distance = current.distanceTo(city)
            #calculate the probability of visiting the city
            prob = (pheromone ** alpha) * ((1.0 / distance) ** beta)
            probabilities.append((city, prob))
            total += prob
        #if there are no cities to visit
        if not probabilities:
          break
        #select the next city to visit
        r = random.uniform(0.0, total)
        cumulative = 0.0
        #this for loop selects the next city to visit
        for city, prob in probabilities:
          cumulative += prob
          #if the cumulative probability is greater than r
          if cumulative >= r:
            ant.visitCity(city)
            break
      #if the ant has visited all cities
        if ant.currentCity.name != ant.path[0]:
          #add the distance between the last city and the first city to the total coast
          ant.totalCoast += map.get_distance(ant.currentCity.name, ant.path[0])
      #update the pheromone matrix
        for i in range(len(ant.path)-1):
          pair = (ant.path[i], ant.path[i+1])
          pheromones[pair] += 1.0 / ant.totalCoast
          pheromones[(ant.path[i+1], ant.path[i])] += 1.0 / ant.totalCoast
  #return the best ant
  #the best ant is the one with the smallest total coast
  best_ant = min(ants, key = lambda ant: ant.totalCoast)
  return best_ant.totalCoast