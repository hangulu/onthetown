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

class Algorithm:
    """
    A container for different types of search algorithms.
    """

    def __init__(self, type, cost_fn, heuristic):
        self.type = type
        self.cost_fn = cost_fn
        self.heuristic = heuristic

    def search(self, problem):
    # Initialize variables to store visited states, the cost, and the starting state
    visited = []
    cost = 0
    start = problem.getStartState() # change this

    # If it is uniform cost search, include the extra parameter for cost. Push the first state to the data structure.
    if self.type == "dfs":
        dstruct = Stack()
    elif self.type == "bfs":
        dstruct = Queue()
    elif self.type == "astar":
        dstruct = PriorityQueueWithFunction(heuristic) # include heuristic
    dstruct.push((start, [], cost))

    if self.type == "ucs":
        dstruct = PriorityQueue()
        dstruct.push((start, [], cost), cost)

    # Iterate through the entire data structure.
    while not dstruct.isEmpty():
        # Deconstruct the tuple created by getSuccessors.
        # We have to redo this, based on how we consider successors
        state, direction, cost = dstruct.pop()
        # Check if the goal state is the current state.
        # Check if we have the desired number of states
        if problem.isGoalState(state):
            return direction
        # Perhaps something like the below
        if len(problem) == 7:
            return problem
        # Check if the current state has been visited before.
        if state not in visited:
            visited.append(state)
            # Add the successors of the state to the data structure.
            for successor in problem.getSuccessors(state):
                # Need to work on succession. Will come after more algorithms talk
                # Let direction store all the directions to the state.
                if ucs:
                    dstruct.push((successor[0], direction + [successor[1]], cost + successor[2]), cost + successor[2])
                else:
                    dstruct.push((successor[0], direction + [successor[1]], cost + successor[2]))

    # The behavior below has been abstracted above, using the "type" attribute of the Algorithm class
    # def dfs(problem):
    #     """
    #     Search the deepest nodes in the search tree first.
    #     """
    #     # Run the search with a stack.
    #     return search(problem, util.Stack())
    #
    # def bfs(problem):
    #     """
    #     Search the shallowest nodes in the search tree first.
    #     """
    #     # Run the search with a queue.
    #     return search(problem, util.Queue())
    #
    # def ucs(problem):
    #     """
    #     Search the node of least total cost first.
    #     """
    #     # Run the search with a priority queue.
    #     return search(problem, util.PriorityQueue(), ucs=True)
    #
    # def nullHeuristic(state, problem=None):
    #     """
    #     A heuristic function estimates the cost from the current state to the nearest goal in the provided SearchProblem. This heuristic is trivial.
    #     """
    #     return 0
    #
    # def aStarSearch(problem, heuristic=nullHeuristic):
    #     """
    #     Search the node that has the lowest combined cost and heuristic first.
    #     """
    #     # Create the heuristic function, then run using the genericSearch
    #     def composite(currentState):
    #         return heuristic(currentState[0], problem) + currentState[2]
    #     return search(problem, util.PriorityQueueWithFunction(composite))

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
