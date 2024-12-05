'''
Tree structure for TSP 

Given a set of cities and it's coordinates, what is the shortest possible tour that
visits each city exactly once, and returns to the starting city?


'''
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List, Set

@dataclass()
class City:
  name: str
  coordinates : Tuple[int, int]
  
  def distanceTo (self, city: City) -> float:
    x1, y1 = self.coordinates
    x2, y2 = city.coordinates
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
  
@dataclass
class Map:
  cities: List[City]
  distances: dict[Tuple[str, str], float] = field(init=False)
  
  def __post_init__(self):
    self.distances = {}
    for city1 in self.cities:
      for city2 in self.cities:
        if city1 == city2:
          continue
        self.distances[(city1.name, city2.name)] = city1.distanceTo(city2)
        
  def get_distance(self, cityName1 : str, cityName2: str) -> float:
    return self.distances.get((cityName1, cityName2),0.0)
  
@dataclass
class State:
  city : City
  visited: Set[str]
  path: List[str]
  cost : float = 0.0
  
  def isGoal(self, totalCities: int , startCity: str) -> bool:
    return len(self.visited) == totalCities and self.city.name == startCity
  
  def successors(self, map : Map):
    if len(self.visited) < len(map.cities):
      for nextCity in map.cities:
        if nextCity.name not in self.visited:
          distance = map.get_distance(self.city.name, nextCity.name)
          newVisited = self.visited.copy()
          newVisited.add(nextCity.name)
          newPath = self.path.copy()
          newPath.append(nextCity.name)
          newState = State(nextCity, newVisited, newPath, self.cost + distance)
          yield newState
    else:
      startCity = self.path[0]
      if self.city.name != startCity:
        distance = map.get_distance(self.city.name, startCity)
        newPath = self.path.copy()
        newPath.append(startCity)
        newState = State(map.cities[0], self.visited, newPath, self.cost + distance)
        yield newState

@dataclass
class Node: 
  parent: Node
  state: State
  action : str
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
    while node.parent is not None:
      solution.append(node)
      node = node.parent
    solution.reverse()
    return solution
  
  