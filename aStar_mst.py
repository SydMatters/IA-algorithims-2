from tree import Map, State, Node, City
from heuristic import minimumSpanningTree
import heapq
import time
from dataclasses import dataclass, field

#This class is used to store the priority of a node in the frontier
@dataclass(order=True)
class PriorityNode:
  priority: float
  node: Node = field(compare=False)

'''
This function receives a map and a start city and returns the path to the goal city using the
A* algorithm with the minimum spanning tree heuristic.
'''  
def aStarMST(map : Map, startCity: str):
  #Find the start city in the map
  start = next(city for city in map.cities if city.name == startCity)
  #Create the initial state and node
  initialState = State(city= start, visited=set([start.name]), path=[start.name], cost=0.0)
  initialNode = Node(parent=None, state=initialState, action=None, depth=0)
  
  #Create the frontier and add the initial node
  frontier = []
  #Calculate the priority of the initial node
  initialPriority = minimumSpanningTree(map.cities, initialState.visited) + initialNode.state.cost
  #Add the initial node to the frontier
  heapq.heappush(frontier, PriorityNode(priority=initialPriority, node=initialNode))
  
  explored = set()
  
  #While the frontier is not empty
  while frontier:
    #Get the node with the lowest priority
    currentPriorityNode = heapq.heappop(frontier)
    currentNode = currentPriorityNode.node
    currentState = currentNode.state
    #If the current state is the goal state, return the current node
    if currentState.isGoal(totalCities=len(map.cities), startCity=startCity):
      return currentNode
    #Add the current state to the explored set
    stateId = (currentState.city.name, tuple(sorted(currentState.visited)))
    #If the state is already in the explored set, continue
    if stateId in explored:
      continue
    explored.add(stateId)
    
    #Expand the current node
    for child in currentNode.expand(map):
      childState = child.state
      #If the child state is already in the explored set, continue
      if (childState.city.name, tuple(sorted(childState.visited))) in explored:
        continue
      #Calculate the priority of the child node
      heuristic = minimumSpanningTree(map.cities, childState.visited)
      priority = heuristic + childState.cost
      #Add the child node to the frontier
      heapq.heappush(frontier, PriorityNode(priority = priority, node = child))
      
    return None