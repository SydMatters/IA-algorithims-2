'''
Tree structure for TSP 

Given a set of cities and it's coordinates, what is the shortest possible tour that
visits each city exactly once, and returns to the starting city?


'''
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List, Set, Optional
import heapq

@dataclass()
class City:
  name: str
  coordinates : Tuple[int, int]
  
  # Euclidean distance between two cities
  def distanceTo (self, city: City) -> float:
    x1, y1 = self.coordinates
    x2, y2 = city.coordinates
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
  
@dataclass
class Map:
  cities: List[City]
  # distances between cities, is a dictionary of tuples
  distances: dict[Tuple[str, str], float] = field(init=False)
  
  # Initialize the distances between cities
  def __post_init__(self):
    self.distances = {}
    for city1 in self.cities:
      for city2 in self.cities:
        if city1 == city2:
          continue
        distance = city1.distanceTo(city2)
        self.distances[(city1.name, city2.name)] = distance
        self.distances[(city2.name, city1.name)] = distance
  
  # Get the distance between two cities      
  def get_distance(self, cityName1 : str, cityName2: str) -> float:
    return self.distances.get((cityName1, cityName2), float('inf'))
  
@dataclass
class State:
  city : City
  # Set of visited cities
  visited: Set[str]
  # List of cities visited in order
  path: List[str]
  # Cost of the path
  cost : float = 0.0
  
  # Check if the state is a goal state, that is, if all cities have been visited
  def isGoal(self, totalCities: int , startCity: str) -> bool:
    return len(self.visited) == totalCities and self.city.name == startCity and len(self.path) == totalCities + 1
  
  # Generate the successors of the state
  def successors(self, map : Map):
    # If not all cities have been visited, generate the successors
    if len(self.visited) < len(map.cities):
      # For each city in the map
      for nextCity in map.cities:
        # If the city has not been visited
        if nextCity.name not in self.visited:
          # Calculate the distance between the current city and the next city
          distance = map.get_distance(self.city.name, nextCity.name)
          # Create a new state with the next city visited
          newVisited = self.visited.copy()
          newVisited.add(nextCity.name)
          newPath = self.path.copy()
          newPath.append(nextCity.name)
          newState = State(nextCity, newVisited, newPath, self.cost + distance)
          yield (nextCity.name,newState)
    # If all cities have been visited, generate the successor with the start city
    else:
      startCity = self.path[0]
      # If the current city is not the start city, create a successor with the start city
      if self.city.name != startCity:
        distance = map.get_distance(self.city.name, startCity)
        newPath = self.path.copy()
        newPath.append(startCity)
        startCity = next(city for city in map.cities if city.name == startCity)
        newState = State(startCity, self.visited, newPath, self.cost + distance)
        yield (startCity,newState)

@dataclass
class Node: 
  parent: Optional[Node]
  state: State
  action : Optional[str]
  depth: int
  
  def expand(self, map : Map):
    for (action, succ_state) in self.state.successors(map):
      succ_node = Node(
        parent = self,
        state = succ_state,
        action = action,
        depth = self.depth + 1)
      yield succ_node
      
  def extract_solution(self):
    solution = []
    node = self
    while node.parent is not None and node.action is not None:
      solution.append(node.action)
      node = node.parent
    solution.reverse()
    return solution
  
  