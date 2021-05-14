import pygame
import sys
import pandas as pd
import heapq
from tkinter import *
from tkinter import ttk
import random

get_walls = random.randint(1, 5)

game_layout = pd.read_csv('src\layouts\/two.csv')

if get_walls == 1:
    game_layout = pd.read_csv('src\layouts\one.csv')

if get_walls == 3:
    game_layout = pd.read_csv('src\layouts\/three.csv')

if get_walls == 4:
    game_layout = pd.read_csv('src\layouts\/four.csv')

if get_walls == 5:
    game_layout = pd.read_csv('src\layouts\/five.csv')

WALLS = game_layout.iloc[:, :].values

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLOCK_SIZE = 20
START = (23, 26)
END = (6, 14)


options = [
    "Depth First Search",
    "Breadth First Search",
    "Dijkstras",
    "A* Search Euclidean",
    "A* Search Manhattan"
]

class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'

class Actions:
    _directions = {Directions.NORTH: (0, -1),
                   Directions.SOUTH: (0, 1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0)}

    def directionToVector(direction):
        dx, dy = Actions._directions[direction]
        return dx, dy

class Queue:
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.insert(0,item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class PriorityQueue:
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

def drawPath(path, visited, show):
    # draw nodes as they are explored if 'Show path' box was checked
    if (show):
        for node in visited:
            show = pygame.Rect(node[0] * 20, node[1] * 20, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
            pygame.draw.rect(SCREEN, WHITE, show)
            CLOCK.tick(45)
            pygame.display.update()
    # draw final path returned by the selected algorithm
    for node in path:
            show = pygame.Rect(node[0] * 20, node[1] * 20, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
            pygame.draw.rect(SCREEN, GREEN, show)
            CLOCK.tick(45)
            pygame.display.update()

def sortHelper(algorithm):
    "Helper method to use desired search algorithm"
    if (algorithm == "Depth First Search"):
        path, visited = depthFirstSearch()
        return path, visited
    
    if (algorithm == "Breadth First Search"):
        path, visited = breadthFirstSearch()
        return path, visited

    if (algorithm == "Dijkstras"):
        path, visited = aStarSearch(nullHeuristic)
        return path, visited

    if (algorithm == "A* Search Euclidean"):
        path, visited = aStarSearch(euclideanHeuristic)
        return path, visited

    if (algorithm == "A* Search Manhattan"):
        path, visited = aStarSearch()
        return path, visited

"""
This section is the pop up window at the start of the program.
Allows the user to choose which algorithm they want to see and
if they choose to see the explored nodes.
"""

sortAlgorithm = ""
def onSubmit():
    sortAlgorithm = clicked.get()
    window.quit()
    window.destroy()


def show():
    label.config( text= clicked.get() )

window = Tk()
clicked = StringVar()
clicked.set( "Depth First Search" )
label = Label(window, text='Choose Algorithm: ')
sortBox = OptionMenu( window, clicked, *options )
var = IntVar()
showVisited = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onSubmit)

showVisited.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
sortBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    drawInitalGrid()
    pygame.display.update()

    path, visited = sortHelper(clicked.get())

    drawPath(path, visited, var.get())
    
    # this loop is used to check if 'X' is closed on the window if so then quit program
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

"""
Method to draw initial grid with walls (no paths or nodes have been created/explored
"""
def drawInitalGrid():
    startx, starty = START
    endx, endy = END
    start = pygame.Rect(startx * 20, starty * 20, BLOCK_SIZE, BLOCK_SIZE)
    end = pygame.Rect(endx * 20, endy * 20, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(SCREEN, BLUE, start)
    pygame.draw.rect(SCREEN, YELLOW, end)

    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            # draw grid
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            if (((x // BLOCK_SIZE) < len(WALLS)) and ((y // BLOCK_SIZE) < len(WALLS))):
                if (WALLS[(int)(y // BLOCK_SIZE)][(int)(x // BLOCK_SIZE)] == 'X'):
                    # draw wall
                    pygame.draw.rect(SCREEN, RED, rect)

def getStartState():
    return START

def isGoalState(state):
    endx, endy = END
    statex, statey = state
    return (endx == statex and endy == statey)

def getCostOfActions(actions):
    if actions == None: return 99999
    x, y = START
    cost = 0
    for action in actions:
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = (int)(x + dx), (int)(y + dy)
        if ((WALLS[nexty][nextx] == 'X') and ((nextx > -1 and nextx < 29) and (nexty > -1 and nexty < 29))): return 99999
        cost += 1
    
    return cost


def calculateHeuristic(state, end, heuristic):
    return getCostOfActions(state[1]) + heuristic(state[0], END)    

def nullHeuristic(state, goalState):
    return 0

def euclideanHeuristic(state, goalState):
    statex, statey = state
    endx, endy = goalState
    return ( (statex - endx) ** 2 + (statey - endy) ** 2 ) ** 0.5

def manhattanHeuristic(state, goalState):
    statex, statey = state
    endx, endy = goalState
    return abs(statex - endx) + abs(statey - endy)

def costHeur(state):
    return 1

"""
Method to return the nodes that are neighbors to the current node
Along with the direction that neighbor is in and the cost it takes to 
get there.

returns a list of successors
Example: 
startState = (0, 0)
getSuccessors(startState) = [((0, 1), 'South', 1), ((1, 0), 'East', 1)]
"""
def getSuccessors(state):
    successors = []

    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        x, y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = x + dx, y + dy
        if ((not WALLS[nexty][nextx] == 'X') and ((nextx > -1 and nextx < 29) and (nexty > -1 and nexty < 29))):
            nextState = (nextx, nexty)
            cost = costHeur(nextState)
            successors.append( ( nextState, action, cost ) )

    return successors

"""
Depth First Search
    Makes use of a stack to arrange the order in which the nodes are expanded. Once a node 
    has been fully explored the next node is popped from the top of the stack (LIFO) and then that
    node is expanded.

This search is particularly bad for this problem because there are not instances in which the
node is fully explored. If the two start and end nodes are in opposite corners the function will
search every node before it finds the last (end) node.

If the layouts were a maze it would perform better.
"""
def depthFirstSearch():
    # get start node
    start_node = getStartState()

    # check if the start node is the goal node; if yes no action done
    if isGoalState(start_node):
        return []

    # create new stack for nodes
    node_stack = []

    # create list to save already visited nodes
    visited_nodes = []

    # push the start node onto the stack
    node_stack.append((start_node, [], []))

    # start loop to start DFS on given graph
    while True:
        # check if the stack is empty; if yes then return no action
        if len(node_stack) == 0:
            return []

        # store the node at the top of the stack and the path associated
        current_node, found_path, draw_path = node_stack.pop(-1)

        # store the current node in the list of visited nodes
        visited_nodes.append(current_node)

        # check if the current node is the goal node; if yes return the path
        if isGoalState(current_node):
            return draw_path, visited_nodes

        # get the children of the current node for traversal of the graph
        successor_node = getSuccessors(current_node)

        # search the children of current node
        for node in successor_node:
            # check if child node is in visited; if not then add to the top of the stack
            if node[0] not in visited_nodes:
                new_path = found_path + [node[1]]
                new_draw = draw_path + [node[0]]
                node_stack.append((node[0], new_path, new_draw))

"""
Breadth First Search
    Makes use of a queue to arrange the order in which the nodes are expanded. A node is popped
    from the start of the queue (FIFO) and checked if it is the end goal. Then its successors are
    added to the end of the queue.

This search performs okay but if the graph was bigger this would be very ineffient since it sweeps
layer by layer to check if current node is end node.
"""
def breadthFirstSearch():
    # get the start node state
    start_node = getStartState()

    # check if the start node state is the goal node state
    # if yes return no action
    if isGoalState(start_node):
        return []

    # create a queue data structure to use for traversal
    node_queue = Queue()

    # create set to store visited nodes
    visited_nodes = []

    # push the start node onto the queue
    node_queue.push((start_node, [], []))

    # start loop to determine BFS of graph
    while True:
        # check if the queue is empty; if yes return no action
        if node_queue.isEmpty():
            return []

        # get the node at the front of the queue and the path associated with it
        current_node, found_path, draw_path = node_queue.pop()

        # store the current node in the list of visited nodes
        visited_nodes.append(current_node)

        # check if the current node is a goal node; if yes then return the path
        if isGoalState(current_node):
            return draw_path, visited_nodes

        # get the children of the current node to traverse further into the tree
        successor_node = getSuccessors(current_node)

        # search the child nodes
        for node in successor_node:
            # check if child is not in visited or frontier
            if node[0] not in visited_nodes and node[0] not in (frontier[0] for frontier in node_queue.list):                                      
                new_path = found_path + [node[1]]
                new_draw = draw_path + [node[0]]
                node_queue.push((node[0], new_path, new_draw))
        
"""
Great explaination of heuristics from:
https://softwareengineering.stackexchange.com/questions/127027/finding-an-a-heuristic-for-a-directed-graph

A* Search
    Makes use of a priority queue to arrange the order in which the nodes are expanded. The node with the
    lowest cost is placed at the front of the queue and explored first. Costs are determined with different
    heuristic models. The models I chose to use for this problem are:
        Euclidean: measures the distance between two points in a straight line
        Manhattan: measures the distance between two points by the sum of the absolute differences of their
                   cartesian coordinates
    These models will always return a value that is close to the actual cost. If we had the actual cost
    to get to the goal state then the algorithm will always follow the shortest path and never expand. While
    this would be nice it is near impossible to get in real world scenario.

    If the heuristics are greater than the actual cost then it is not guaranteed the algorithm will return
    the shortest path

Dijkstras Algorithm
    It is A* algorithm except the heuristic is zero for every node. Always returns the shortest path


"""
def aStarSearch(heuristic=manhattanHeuristic):
    # get the start node
    start_node = getStartState()

    # check if the start node is the end node
    if isGoalState(start_node):
        return []

    # create a priority queue to store nodes that have been visited but not explored
    open_priority_queue = PriorityQueue()

    # create a list to store nodes that have been visited and expanded
    closed_list = []

    # push the start node in the queue and the cost of the node
    open_priority_queue.push((start_node, [], []), calculateHeuristic((start_node, [], []), END, heuristic))

    while True:
        # if the queue is empty then the goal node was never found return empty path
        if open_priority_queue.isEmpty():
            return []

        # pop the node to be explored from the front of the queue
        current_node, current_path, draw_path = open_priority_queue.pop()

        # check if current node is the end if it is return the path and the visited nodes to be drawn
        if isGoalState(current_node):
            return draw_path, closed_list

        # add the current node to the closed list (visited and explored)
        closed_list.append(current_node)

        # node update the successors of the current node
        for children in getSuccessors(current_node):
            if children[0] not in closed_list:
                # if the successor hasnt been visited yet then store it in the open priority queue
                if (children[0] not in (frontier[2][0] for frontier in open_priority_queue.heap)):
                    new_path = current_path + [children[1]]
                    new_draw = draw_path + [children[0]]
                    new_cost = calculateHeuristic((children[0], new_path, new_draw), END , heuristic)
                    open_priority_queue.push((children[0], new_path, new_draw), new_cost)
                # if the successor has been visited update the cost it takes to get there
                else:
                    for frontier in open_priority_queue.heap:
                        # find the old cost of the node in the open priority queue
                        if frontier[2][0] == children[0]:
                            old_cost = getCostOfActions(frontier[2][1])

                    new_path = current_path + [children[1]]
                    new_draw = draw_path + [children[0]]
                    new_cost = calculateHeuristic((children[0], new_path, new_draw), END, heuristic)
                    # if the old cost is more than the new cost update the cost so it is cheaper to get there
                    if old_cost > new_cost:
                        open_priority_queue.update((children[0], new_path, new_draw), new_cost)

main()