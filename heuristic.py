from tree import *
import heapq

'''
This function calculates the minimum spanning tree of a set of cities.
It uses Prim's algorithm to find the minimum spanning tree of the cities.
The function receives a list of cities and a set of visited cities.
It returns the cost of the minimum spanning tree.
'''
def minimumSpanningTree(cities : List [City], visited : Set[str]) -> float:
  # If all cities have been visited, the cost of the minimum spanning tree is 0
  unvisited = [city for city in cities if city.name not in visited]
  
  # If all cities have been visited, the cost of the minimum spanning tree is 0
  if not unvisited:
    return 0.0
  
  
  mst_cost = 0.0
  visited_mst = set()
  edges = []
  
  start_city = unvisited[0]
  visited_mst.add(start_city.name)
  
  # Add the distances from the start city to all other unvisited cities to the heap
  for city in unvisited[1:]:
    distance = start_city.distanceTo(city)
    heapq.heappush(edges, (distance, city)) 
  
  # While there are edges to explore and not all cities have been visited  
  while edges and len(visited_mst) < len(unvisited):
    # Get the edge
    cost , city = heapq.heappop(edges)
    # If the city has not been visited, add it to the minimum spanning tree
    if city.name in visited_mst:
      visited_mst.add(city.name)
      mst_cost += cost
      # Add the distances from the city to all other unvisited cities to the heap
      for next_city in unvisited:
        # If the city has not been visited, add it to the heap
        if next_city.name not in visited_mst:
          distance = city.distanceTo(next_city)
          heapq.heappush(edges, (distance, next_city))
  # Return the cost of the minimum spanning tree  
  return mst_cost
  
