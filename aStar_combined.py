# a_star_combined.py
from tree import Map, State, Node, City
from heuristic import minimumSpanningTree
from heuristicACO import ACO_heuristic
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class PriorityNode:
    priority: float
    node: Node = field(compare=False)

def aStarCombined(map: Map, start_city: str, iterations: int = 100):
    # Inicializar el estado inicial
    start = next(city for city in map.cities if city.name == start_city)
    initialState = State(city=start, visited={start.name}, path=[start.name], cost=0.0)
    initialNode = Node(parent=None, state=initialState, action=None, depth=0)
    
    # Priority queue
    frontier = []
    MSTHeurist = minimumSpanningTree(map.cities, initialState.visited)
    ACOHeuristic = ACO_heuristic(map, iterations=iterations)
    initialPriority = MSTHeurist + ACOHeuristic + initialState.cost
    heapq.heappush(frontier, PriorityNode(priority=initialPriority, node=initialNode))
    
    # Explored set
    explored = set()
    
    while frontier:
      currentPriorityNode = heapq.heappop(frontier)
      currentNode = currentPriorityNode.node
      currentState = currentNode.state
      
      # Goal test
      if currentState.isGoal(totalCities=len(map.cities), startCity=start_city):
        return currentNode
      
      # Add to explored
      state_id = (currentState.city.name, tuple(sorted(currentState.visited)))
      if state_id in explored:
        continue
      explored.add(state_id)
      
      # Expand
      for child in currentNode.expand(map):
        childState = child.state
        if (childState.city.name, tuple(sorted(childState.visited))) in explored:
          continue
        # Heurística combinada
        MSTHeurist = minimumSpanningTree(map.cities, childState.visited)
        ACOHeuristic = ACO_heuristic(map, iterations=iterations)
        priority = childState.cost + MSTHeurist + ACOHeuristic
        heapq.heappush(frontier, PriorityNode(priority=priority, node=child))
    
      return None  # No solution found
