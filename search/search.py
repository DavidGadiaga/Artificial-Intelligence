# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


# da commentare 

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    from util import Stack

    fringe = Stack()
    # Initialize the fringe with the start state
    fringe.push(problem.getStartState())
    # Keep track of visited states
    visited = []
    # Current path of actions
    path = []
    # Stack to store the total path
    total_path = Stack()
    # Get the initial state from the fringe
    currentstate = fringe.pop()
    # Mark the current state as visited
    while not problem.isGoalState(currentstate):
        if currentstate not in visited:
            visited.append(currentstate)
            successors = problem.getSuccessors(currentstate)
            for child, action, cost in successors:
                # Add child to the fringe
                fringe.push(child)
                # Extend the current path with the new action
                newPath = path + [action]  
                # Store the total path
                total_path.push(newPath)
        # Move to the next state in the fringe
        currentstate = fringe.pop()
         # Update the current path
        path = total_path.pop()
    return path      

    "util.raiseNotDefined()"

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    from util import Queue

    fringe = Queue()  # Initialize a queue for BFS
    fringe.push(problem.getStartState())  # Enqueue the start state
    visited = []  # List to keep track of visited states
    path = []  # List to store the current path of actions
    total_path = Queue()  # Queue to store the total path
    currentstate = fringe.pop()  # Dequeue the initial state from the fringe

    while not problem.isGoalState(currentstate):
        if currentstate not in visited:
            visited.append(currentstate)  # Mark the current state as visited
            successors = problem.getSuccessors(currentstate)

            for child, action, cost in successors:
                fringe.push(child)  # Enqueue the child state
                newPath = path + [action]  # Extend the current path with the new action
                total_path.push(newPath)  # Enqueue the updated path

        currentstate = fringe.pop()  # Dequeue the next state from the fringe
        path = total_path.pop()  # Dequeue the corresponding path

    return path  # Return the solution path 

    "util.raiseNotDefined()"

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    fringe = PriorityQueue()  # Initialize a priority queue for UCS
    fringe.push((problem.getStartState(), [], 0), 0)  # Enqueue the start state with an initial cost of 0
    visited = set()  # Set to keep track of visited states

    while not fringe.isEmpty():
        current_state, actions, total_cost = fringe.pop()

        if current_state in visited:
            continue  # Skip this iteration if the state has already been visited

        visited.add(current_state)  # Mark the current state as visited

        if problem.isGoalState(current_state):
            return actions  # Return the solution path if the goal is reached

        successors = problem.getSuccessors(current_state)

        for successor, action, step_cost in successors:
            new_actions = actions + [action]
            new_total_cost = total_cost + step_cost
            fringe.push((successor, new_actions, new_total_cost), new_total_cost)
            # Enqueue the successor with the updated path and total cost

    return None  # Return None if no solution is found



    "util.raiseNotDefined()"

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    from util import PriorityQueue
    from util import Counter

    fringe = PriorityQueue()  # Initialize a priority queue for A* search
    counts = Counter()  # Counter to keep track of total costs
    current = (problem.getStartState(), [])  # Initialize with start state and an empty path
    counts[str(current[0])] += heuristic(current[0], problem)  # Add heuristic cost to initial state
    fringe.push(current, counts[str(current[0])])  # Enqueue the start state with its total cost
    visited = []  # List to keep track of visited states

    while not fringe.isEmpty():
        node, path = fringe.pop()

        if problem.isGoalState(node):
            return path  # Return the solution path if the goal is reached

        if not node in visited:
            visited.append(node)  # Mark the current state as visited

            for child, move, cost in problem.getSuccessors(node):
                newpath = path + [move]
                counts[str(child)] = problem.getCostOfActions(newpath)
                counts[str(child)] += heuristic(child, problem)
                fringe.push((child, newpath), counts[str(child)])
                # Enqueue the successor with the updated path and total cost

"util.raiseNotDefined()"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch