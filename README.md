# Airline-Graph

- [x] 1 Find if an airport can be reached from another using only a single airline company. You should compare
- [x] Breadth-first
- [x] Depth-first
- [x] Compare BFS & DFS


- [x] 2 Finding shortest path (distance) from one location to another (Dijk-stra's Algorithm)

- [x] 3 Finding shortest path (time) from one location to another, assuming that each transfer takes one hour. 

- [ ] 4 Finding airline that has widest coverage (Minimum Spanning Tree)

- [x] Defend the choice of datastructure with regard of time and space complexity (Big O)




### BFS and DFS Comparison
BFS == stack
DFS == queue
If you know a solution is not far from the root of the tree, a breadth first search (BFS) might be better. If the tree is very deep and solutions are rare, depth first search (DFS) might take an extremely long time, but BFS could be faster. If the tree is very wide, a BFS might need too much memory, so it might be completely impractical

We have to find out if it its possible to travel from an airport to another, it can go through other airports, and therefore it will be a very deep tree.





Note:
advantages / disadvantages of Dicts vs Lists

When the keys of the dictionary are 0, 1, ..., n, a list will be faster, since no hashing is involved. As soon as the keys are not such a sequence, a dict its the better choice.

In this case it would have been faster and more effecient to use a list.

