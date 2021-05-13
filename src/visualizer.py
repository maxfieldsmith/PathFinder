import pygame
import sys
import pandas as pd
import heapq
from tkinter import *
from tkinter import ttk
import random

get_walls = random.randint(1, 4)

game_layout = pd.read_csv('src\layouts\/two.csv')

if get_walls == 1:
    game_layout = pd.read_csv('src\layouts\one.csv')

if get_walls == 3:
    game_layout = pd.read_csv('src\layouts\/three.csv')

if get_walls == 4:
    game_layout = pd.read_csv('src\layouts\/four.csv')

WALLS = game_layout.iloc[:, :].values

sortAlgorithm = ""


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
END = (6, 16)

GRID_SIZE = (int)(WINDOW_WIDTH / 20)

# GRID is to easily paint display
# WALLS keeps track of where walls are
GRID = [[0]*GRID_SIZE]*GRID_SIZE

options = [
    "Depth First Search",
    "Breadth First Search",
    "Dijkstras",
    "A* Search"
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

def drawPath(path, visited, show):
    if (show):
        for node in visited:
            show = pygame.Rect(node[0] * 20, node[1] * 20, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
            pygame.draw.rect(SCREEN, WHITE, show)
            CLOCK.tick(45)
            pygame.display.update()
    
    for node in path:
            show = pygame.Rect(node[0] * 20, node[1] * 20, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
            pygame.draw.rect(SCREEN, GREEN, show)
            CLOCK.tick(45)
            pygame.display.update()

def sortHelper(algorithm):
    if (algorithm == "Depth First Search"):
        path, visited = depthFirstSearch()
        return path, visited
    
    if (algorithm == "Breadth First Search"):
        path, visited = breadthFirstSearch()
        return path, visited

    if (algorithm == "Dijkstras"):
        path, visited = aStarSearch(nullHeuristic)
        return path, visited

    if (algorithm == "A* Search"):
        path, visited = aStarSearch(euclideanHeuristic)
        return path, visited




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
    
    print(var.get())

    path, visited = sortHelper(clicked.get())

    drawPath(path, visited, var.get())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


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
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            if (((x / BLOCK_SIZE) + 1 < len(WALLS)) and ((y / BLOCK_SIZE) + 1 < len(WALLS))):
                if (WALLS[(int)(y / BLOCK_SIZE)][(int)(x / BLOCK_SIZE)] == 'X'):
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

def getSuccessors(state):
    successors = []

    for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        x, y = state
        dx, dy = Actions.directionToVector(action)
        nextx, nexty = x + dx, y + dy
        if ((not WALLS[nexty][nextx] == 'X') and ((nextx > -1 and nextx < 29) and (nexty > -1 and nexty < 29))):
            if (nextx == 29): print ("whta")
            nextState = (nextx, nexty)
            cost = costHeur(nextState)
            successors.append( ( nextState, action, cost ) )

    return successors


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

def aStarSearch(heuristic=manhattanHeuristic):
    start_node = getStartState()

    if isGoalState(start_node):
        return []

    open_priority_queue = PriorityQueue()

    closed_list = []

    open_priority_queue.push((start_node, [], []), calculateHeuristic((start_node, [], []), END, heuristic))


    while True:
        if open_priority_queue.isEmpty():
            return []

        current_node, current_path, draw_path = open_priority_queue.pop()

        if isGoalState(current_node):
            return draw_path, closed_list

        closed_list.append(current_node)

        for children in getSuccessors(current_node):
            if children[0] not in closed_list:
                if (children[0] not in (frontier[2][0] for frontier in open_priority_queue.heap)):
                    new_path = current_path + [children[1]]
                    new_draw = draw_path + [children[0]]
                    new_cost = calculateHeuristic((children[0], new_path, new_draw), END , heuristic)
                    open_priority_queue.push((children[0], new_path, new_draw), new_cost)
                else:
                    for frontier in open_priority_queue.heap:
                        if frontier[2][0] == children[0]:
                            old_cost = getCostOfActions(frontier[2][1])

                    new_path = current_path + [children[1]]
                    new_draw = draw_path + [children[0]]
                    new_cost = calculateHeuristic((children[0], new_path, new_draw), END, heuristic)

                    if old_cost > new_cost:
                        open_priority_queue.update((children[0], new_path, new_draw), new_cost)

main()