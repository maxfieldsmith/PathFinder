import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 600
BLOCK_SIZE = 20

GRID_SIZE = (int)(WINDOW_WIDTH / 20)

GRID = [[0]*GRID_SIZE]*GRID_SIZE
WALLS = GRID

print(len(WALLS))


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    print(len(GRID))
    while True:
        drawInitalGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawInitalGrid():
    
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT - 150, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)
            #bord = pygame.Rect(x, y, blockSize, blockSize)
            if (((x / BLOCK_SIZE) + 1 < len(WALLS)) and ((y / BLOCK_SIZE) + 1 < len(WALLS))):
                if (WALLS[(int)(y / BLOCK_SIZE)][(int)(x / BLOCK_SIZE)] == 'X'):
                    #pygame.draw.rect(SCREEN, GREEN, rect)
                    pygame.draw.rect(SCREEN, RED, rect)

            

                

main()

#####################################################
#               CHOOSE ALGORITHM TYPE
#####################################################
##
## button = pygame.Rect(100, 100, 50, 50)
##
## ...
##
## if event.type == pygame.MOUSEBUTTONDOWN:
##     mouse_pos = event.pos  # gets mouse position
##
##     # checks if mouse position is over the button
##     if button.collidepoint(mouse_pos):
##         # prints current location of mouse
##         print('button was pressed at {0}'.format(mouse_pos))
##
#####################################################


#####################################################
#                   getStartState()
#####################################################
##
## Start: (0, 0)
## getSuccessors: [((0, 20), 'SOUTH', 1), ((20, 0), 'WEST', 1)]
##
## def getSuccessors(self, state):
##     """
##     Returns successor states, the actions they require, and a cost of 1.
##
##         As noted in search.py:
##             For a given state, this should return a list of triples,
##         (successor, action, stepCost), where 'successor' is a
##         successor to the current state, 'action' is the action
##         required to get there, and 'stepCost' is the incremental
##         cost of expanding to that successor
##     """
##
##     successors = []
##     for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
##         x,y = state
##         dx, dy = Actions.directionToVector(action)
##         nextx, nexty = int(x + dx), int(y + dy)
##         if not self.walls[nextx][nexty]:
##             nextState = (nextx, nexty)
##             cost = self.costFn(nextState)
##             successors.append( ( nextState, action, cost) )
##
##     # Bookkeeping for display purposes
##     self._expanded += 1 # DO NOT CHANGE
##     if state not in self._visited:
##         self._visited[state] = True
##         self._visitedlist.append(state)
##
##     return successors
##
#####################################################