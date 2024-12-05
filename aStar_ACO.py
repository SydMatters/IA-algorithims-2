from tree import Map, State, Node, City
from heuristicACO import ACO_heuristic
import heapq
import time
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass(order=True)
class PriorityNode:
  priority: float
  node: Node = field(compare=False)
  
def aStarACO(map : Map, start_city : str, iterations: int = 100):
  start = next(city for city in map.cities if city.name == start_city)
  initialState = State(city=start, visited={start.name}, path=[start.name], cost=0.0)
  initialNode = Node(parent=None, state=initialState, action=None, depth=0)
  
  frontier = []
  initialHeuristic = ACO_heuristic(map, iterations)
  initialPriority = initialState.cost + initialHeuristic
  heapq.heappush(frontier, PriorityNode(initialPriority, initialNode))
  
  explored = set()
  
  while frontier:
    currentPriorityNode = heapq.heappop(frontier)
    currentNode = currentPriorityNode.node
    currentState = currentNode.state
    
    if currentState.isGoal(totalCities=len(map.cities), startCity=start_city):
      return currentNode
    
    stateId = (currentState.city.name, tuple(sorted(currentState.visited)))
    if stateId in explored:
      continue
    explored.add(stateId)
    
    for child in currentNode.expand(map):
      childState = child.state
      if (childState.city.name, tuple(sorted(childState.visited))) in explored:
        continue
      heuristic = ACO_heuristic(map, iterations)
      priority = childState.cost + heuristic
      heapq.heappush(frontier, PriorityNode(priority, child))
      
    return None