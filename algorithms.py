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

import center as c
import copy
import heapq, random

class Algorithm:
    """
    A container for different types of search algorithms.
    """

    def __init__(self):
        """
        Initialize the Algorithm class.
        """
            pass

    def search(self, party):
        """
        The search algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

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
        filtered_list = party.filteredPlaces
        start = filtered_list[0]

        # If it is uniform cost search, include the extra parameter for cost.
        # Push the first state to the data structure.
        if self.type != "ucs":
            if self.type == "dfs":
                dstruct = Stack()
            elif self.type == "bfs":
                dstruct = Queue()
            elif self.type == "astar":
                dstruct = PriorityQueueWithFunction(self.heuristic)
            dstruct.push((start, [], cost))
        else:
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
                # print self.type, cost
                return previous, cost

            # Check if the current place has been visited before.
            if event not in visited:
                visited.append(event)
                # Add the successors of the place to the data structure.
                # for successor in problem.getSuccessors(state):
                for successor in c.similarity(event, filtered_list):
                    sadness = successor["sadness"]
                    succ_cost = sum(sadness) + max(sadness)
                    # Let previous store all the previous places
                    if self.type == "ucs":
                        dstruct.push((successor, previous + [successor], cost + succ_cost), cost + succ_cost)
                    else:
                        dstruct.push((successor, previous + [successor], cost + succ_cost))

    def dfsSearch(self, party):
        """
        The DFS algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
        # Initialize variables to store visited states, the cost, and
        # the starting state
        # visited stores the places that have already been visited
        visited = []
        # cost stores the total sadness of the current tree
        cost = 0
        # The starting state is the first of the full list of activities
        # returned from the Google search
        filteredList = party.filteredPlaces
        path = []

        # Initialize the data structure for the frontier, a stack, and push
        # the first node to it
        stack = Stack()
        stack.push((path, filteredList, cost))

        # Iterate through the entire data structure
        while not stack.isEmpty():
            # Deconstruct the tuple created by the successor function
            # A "successor" is a member of the list of places deemed dissimilar
            # from the current node. That list is generated from the similarity
            # function applied to the current node and the full list of places
            # returned from the Google API call
            path, remaining, cost = stack.pop()

            # The goal test
            if len(path) == 7:
                return path, cost

            if len(path) != 0:
                # Get the last event in the path and check if it was visited
                event = path[-1]
                if event not in visited:
                    visited.append(event)
                    # Find the successors of the current node
                    nextList = c.similarity(event, remaining)
                    # Iterate through the successors and add them to the
                    # frontier
                    for successor in nextList:
                        # Extract the sadness
                        sadness = successor["sadness"]
                        # Find the cost and push the new state to the frontier
                        nextCost = sum(sadness) + max(sadness)
                        stack.push((path + [successor], nextList, cost + nextCost))
            else:
                # For the initial empty path
                for successor in filteredList:
                    sadness = successor["sadness"]
                    nextCost = sum(sadness) + max(sadness)
                    newList = copy.deepcopy(filteredList)
                    newList.remove(successor)
                    stack.push((path + [successor], filteredList, cost + nextCost))

    def bfsSearch(self, party):
        """
        The BFS algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
        # Initialize variables to store visited states, the cost, and
        # the starting state
        # visited stores the places that have already been visited
        visited = []
        # cost stores the total sadness of the current tree
        cost = 0
        # The starting state is the first of the full list of activities
        # returned from the Google search
        filteredList = party.filteredPlaces
        path = []

        # Initialize the data structure for the frontier, a queue, and push
        # the first node to it
        queue = Queue()
        queue.push((path, filteredList, cost))

        # Iterate through the entire data structure
        while not queue.isEmpty():
            # Deconstruct the tuple created by the successor function
            # A "successor" is a member of the list of places deemed dissimilar
            # from the current node. That list is generated from the similarity
            # function applied to the current node and the full list of places
            # returned from the Google API call
            path, remaining, cost = queue.pop()

            # The goal test
            if len(path) == 7:
                return path, cost

            if len(path) != 0:
                # Get the last event in the path and check if it was visited
                event = path[-1]
                # Find the successors of the current node
                nextList = c.similarity(event, remaining)
                # Iterate through the successors and add them to the
                # frontier
                for successor in nextList:
                    # Extract the sadness
                    sadness = successor["sadness"]
                    # Find the cost and push the new state to the frontier
                    nextCost = sum(sadness) + max(sadness)
                    queue.push((path + [successor], nextList, cost + nextCost))

            else:
                # For the initial empty path
                for successor in filteredList:
                    sadness = successor["sadness"]
                    nextCost = sum(sadness) + max(sadness)
                    newList = copy.deepcopy(filteredList)
                    newList.remove(successor)
                    queue.push((path + [successor], newList, cost + nextCost))

    def greedySearch(self, party):
        """
        The Greedy Search algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
        # Initialize variables to store the visited states,
        # the cost and the starting state
        # cost stores the total sadness of the current tree
        visited = []
        cost = 0
        # The starting state is the first of the full list of activities
        # returned from the Google search
        filteredList = party.filteredPlaces
        path = []

        # Initialize the data structure for the frontier, a priority queue,
        # and push the first node to it
        prioQ = PriorityQueue()
        prioQ.push((path, filteredList, cost), 0)

        # Iterate through the entire data structure
        while not prioQ.isEmpty():
            # Deconstruct the tuple created by the successor function
            # A "successor" is a member of the list of places deemed dissimilar
            # from the current node. That list is generated from the similarity
            # function applied to the current node and the full list of places
            # returned from the Google API call
            path, remaining, cost = prioQ.pop()

            # The goal test
            if len(path) == 7:
                return path, cost

            if len(path) != 0:
                # Get the last event in the path and check if it was visited
                event = path[-1]
                if path not in visited:
                    visited.append(path)
                    # Find the successors of the current node
                    newList = c.similarity(event, remaining)
                    for successor in newList:
                        # Check if the successor is in the current path
                        if successor not in path:
                            # Extract the sadness
                            sadness = successor["sadness"]
                            # Find the cost and push the new state to the frontier
                            nextCost = sum(sadness) + max(sadness)
                            prioQ.push((path + [successor], newList, cost + nextCost), heuristic((path + [successor], newList, cost + nextCost)))
            else:
                # For the initial empty path
                for successor in filteredList:
                    sadness = successor["sadness"]
                    nextCost = sum(sadness) + max(sadness)
                    newList = copy.deepcopy(filteredList)
                    newList.remove(successor)
                    prioQ.push((path + [successor], filteredList, cost + nextCost), heuristic((path + [successor], newList, cost + nextCost)))

    def astarSearch(self, party):
        """
        The A* Search algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
        # Initialize variables to store the visited states,
        # the cost, and the starting state
        visited = []
        cost = 0
        filteredList = party.filteredPlaces
        path = []

        # Initialize the data structure for the frontier, a priority queue
        # with a function, and push the first node to it
        prioQ = PriorityQueueWithFunction(astarFunction)
        prioQ.push((path, filteredList, cost))

        # Iterate through the entire data structure
        while not prioQ.isEmpty():
            # Deconstruct the tuple created by the successor function
            # A "successor" is a member of the list of places deemed dissimilar
            # from the current node. That list is generated from the similarity
            # function applied to the current node and the full list of places
            # returned from the Google API call
            path, remaining, cost = prioQ.pop()

            # The goal test
            if len(path) == 7:
                return path, cost

            if len(path) != 0:
                # Get the last event in the path and check if it was visited
                event = path[-1]
                if path not in visited:
                    visited.append(path)
                    # Find the successors of the current node
                    nextList = c.similarity(event, remaining)
                    # Iterate through the successors and add them to the
                    # frontier
                    for successor in nextList:
                        # Extract the sadness
                        sadness = successor["sadness"]
                        # Find the cost and push the new state to the frontier
                        nextCost = sum(sadness) + max(sadness)
                        prioQ.push((path + [successor], nextList, cost + nextCost))
            else:
                # For the initial empty path
                for successor in filteredList:
                    sadness = successor["sadness"]
                    nextCost = sum(sadness) + max(sadness)
                    newList = copy.deepcopy(filteredList)
                    newList.remove(successor)
                    prioQ.push((path + [successor], filteredList, cost + nextCost))

    def ucsSearch(self, party):
        """
        The UCS algorithm. Takes in a search problem and returns a
        solution. In the social plannnig case, the search problem is the
        list of viable options for an activity, and the object returned is
        a list of the "best" 7.
        problem (Party object): An object containing information about a
        potential meetup

        return: Tuple of a list of the best 7 options for an activity and
        the total sadness associated with that list
        """
        # Initialize variables to store the visited path,
        # the cost, and the starting state
        visited = []
        cost = 0
        filteredList = party.filteredPlaces
        path = []

        # Initialize the data structure for the frontier, a priority queue
        # with a function, and push the first node to it
        prioQ = PriorityQueue()
        prioQ.push((path, filteredList, cost), cost)

        # Iterate through the entire data structure
        while not prioQ.isEmpty():
            # Deconstruct the tuple created by the successor function
            # A "successor" is a member of the list of places deemed dissimilar
            # from the current node. That list is generated from the similarity
            # function applied to the current node and the full list of places
            # returned from the Google API call
            path, remaining, cost = prioQ.pop()

            # The goal test
            if len(path) == 7:
                return path, cost

            if len(path) != 0:
                # Get the last event in the path and check if it was visited
                event = path[-1]
                if path not in visited:
                    visited.append(path)
                    # Find the successors of the current node
                    nextList = c.similarity(event, remaining)
                    # Iterate through the successors and add them to the
                    # frontier
                    for successor in nextList:
                        # Extract the sadness
                        sadness = successor["sadness"]
                        # Find the cost and push the new state to the frontier
                        nextCost = sum(sadness) + max(sadness)
                        prioQ.push((path + [successor], nextList, cost + nextCost), cost + nextCost)
            else:
                # For the initial empty path
                for successor in filteredList:
                    sadness = successor["sadness"]
                    nextCost = sum(sadness) + max(sadness)
                    newList = copy.deepcopy(filteredList)
                    newList.remove(successor)
                    prioQ.push((path + [successor], newList, cost + nextCost), cost + nextCost)

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
    Implement a priority queue with the same push/pop signature of the
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

def astarFunction(state):
    """
    Determine the queuing order for the A* function.
    state (list): Information for a given state.

    return: The heuristic applied to the state added to the cost.
    """
    return state[2] + heuristic(state)

def heuristic(state):
    """
    Take in a state (a triple of current place, all places before the current
    place, and the total cost associated with the current place) and apply a
    heuristic to it for A* search.
    state (triple): (current place, all places before the current
    place, the total cost associated with the current place)

    return: integer that approximates distance from the goal
    """
    # Encode the progress to the goal as the length of the list of previous states
    progress = len(state[0])
    # Goal distance is the number of places left to be added multiplied by
    # the average of the sadness value to the current point
    if progress != 0:
        goal_distance = (7 - progress) * state[2] / (progress)
    else:
        goal_distance = 7
    return goal_distance
