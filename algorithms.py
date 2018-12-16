"""
The following search algorithms are implemented to solve the social planning
search problem:
* Depth-First Search
* Breadth-First Search
* A* Search
* Greedy Search
* TBD

This module implements these algorithms as a class, as well as their
supporting data structures.
"""

import center
import heapq, random

class Algorithm:
    """
    A container for different types of search algorithms.
    """

    def __init__(self, type, cost_fn, heuristic):
        """
        Initialize the Algorithm class.
        type (string): A string denoting the type of algorithm. Either dfs,
        bfs, ucs, greedy, or astar.
        cost_fn (function): The cost function for the algorithm. For the
        social planning case, this is the sadness function.
        heuristic (function): The heuristic used for A* search.
        """
        self.type = type
        self.cost_fn = cost_fn
        self.heuristic = heuristic

    def search(self, problem):
        """
        The search algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (search object): List of viable options.

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
    # Initialize variables to store visited states, the cost, and
    # the starting state
    # visited stores the places that have already been visited
    visited = []
    # cost stores the total sadness of the current tree
    cost = 0
    # The starting state is the first of the full list of activities returned # from the Google search
    start = problem[0]

    # If it is uniform cost search, include the extra parameter for cost.
    # Push the first state to the data structure.
    if self.type == "dfs":
        dstruct = Stack()
    elif self.type == "bfs":
        dstruct = Queue()
    elif self.type == "astar":
        dstruct = PriorityQueueWithFunction(self.heuristic)
    dstruct.push((start, [], cost))

    if self.type == "ucs":
        dstruct = PriorityQueue()
        dstruct.push((start, [], cost), cost)

    # Iterate through the entire data structure.
    while not dstruct.isEmpty():
        # Deconstruct the tuple created by getSuccessors.
        # A "successor" is a member of the list of places deemed dissimilar
        # from the current node. That list is generated from the similarity
        # function applied to the current node and the full list of places
        # returned from the Google API call
        event, previous, cost = dstruct.pop()

        # Perhaps something like the below to return
        if len(previous) == 7:
            return previous, cost

        # Check if the current place has been visited before.
        if event not in visited:
            visited.append(event)
            # Add the successors of the place to the data structure.
            # for successor in problem.getSuccessors(state):
            for successor in center.similarity(event, places):
                # Let previous store all the previous places
                if ucs:
                    # The
                    dstruct.push((successor, previous + [successor], cost + sadness), cost + sadness)
                else:
                    dstruct.push(successor, previous + [successor], cost + sadness)

# The following are the classes for the data structures
class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))

def astar_heuristic(state):
    """
    Takes in a state (a triple of current place, all places before the current
    place, and the total cost associated with the current place) and applies a
    heuristic to it for A* search.
    state (triple): (current place, all places before the current
    place, the total cost associated with the current place)

    return: integer that approximates distance from the goal
    """
    # Encode the progress to the goal as the length of the list of previous states
    progress = len(state[1])
    # Goal distance is the number of places left to be added multiplied by
    # the average of the sadness value to the current point
    goal_distance = (7 - progress) * state[2] / progress
    return goal_distance
