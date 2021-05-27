import pygame
import time
from grid import OccupancyGridMap
from typing import List

# Define some colors
BLACK = (0, 0, 0)  # BLACK
UNOCCUPIED = (255, 255, 255)  # WHITE
GOAL = (0, 255, 0)  # GREEN
START = (255, 0, 0)  # RED
GRAY1 = (145, 145, 102)  # GRAY1
OBSTACLE = (77, 77, 51)  # GRAY2
LOCAL_GRID = (0, 0, 80)  # BLUE

colors = {
    0: UNOCCUPIED,
    1: GOAL,
    255: OBSTACLE
}


class Animation:
    def __init__(self,
                 title="D* Lite Path Planning",
                 width=10,
                 height=10,
                 margin=0,
                 x_dim=100,
                 y_dim=50,
                 starts=(0, 0),
                 goals=(50, 50),
                 grid=None,
                 colors=None,
                 viewing_range=3):

        self.width = width
        self.height = height
        self.margin = margin
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.starts = starts
        self.currents = starts
        self.observation = {"pos": None, "type": None}
        self.goals = goals
        self.cells = grid
        self.colors = colors
        self.viewing_range = viewing_range

        pygame.init()

        # Set the 'width' and 'height' of the screen
        window_size = [(width + margin) * y_dim + margin,
                       (height + margin) * x_dim + margin]

        self.screen = pygame.display.set_mode(window_size)

        # create occupancy grid map
        """
        set initial values for the map occupancy grid
        |----------> y, column
        |           (x=0,y=2)
        |
        V (x=2, y=0)
        x, row
        """
        self.world = OccupancyGridMap(x_dim=x_dim,
                                      y_dim=y_dim,
                                      exploration_setting='8N')

        # Set title of screen
        pygame.display.set_caption(title)

        # set font
        pygame.font.SysFont('Comic Sans MS', 36)

        for r, l in enumerate(self.cells):
            for c, is_obstacle in enumerate(l):
                if is_obstacle:
                    # turn pos into cell
                    grid_cell = (r, c)

                    # set the location in the grid map
                    self.world.set_obstacle(grid_cell)

        # Loop until the user clicks the close button
        self.done = False

        # used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

    def get_positions(self):
        return self.currents

    def set_positions(self, poses: [(int, int)]):
        self.currents = poses

    def get_goals(self):
        return self.goals

    def set_goals(self, goals: (int, int)):
        self.goals = goals

    def set_starts(self, starts: (int, int)):
        self.starts = starts

    def display_obs(self, observations=None):
        if observations is not None:
            for o in observations:
                pygame.draw.rect(self.screen, GRAY1, [(self.margin + self.width) * o[1] + self.margin,
                                                      (self.margin + self.height) * o[0] + self.margin,
                                                      self.width,
                                                      self.height])

    def run_game(self, paths=None):
        if paths is None:
            paths = [[]]

        paths = paths[:10]
        # set the screen background
        self.screen.fill(BLACK)

        # draw the grid
        for row in range(self.x_dim):
            for column in range(self.y_dim):
                # color the cells
                pygame.draw.rect(self.screen, colors[self.world.occupancy_grid_map[row][column]],
                                 [(self.margin + self.width) * column + self.margin,
                                  (self.margin + self.height) * row + self.margin,
                                  self.width,
                                  self.height])

        for color, goal in zip(self.colors, self.goals):
            # fill in the goal cell with green
            pygame.draw.rect(self.screen, color, [(self.margin + self.width) * goal[1] + self.margin,
                                                  (self.margin + self.height) * goal[0] + self.margin,
                                                  self.width,
                                                  self.height])
            center = [round(goal[1] * (self.width + self.margin) + self.width / 2) + self.margin,
                      round(goal[0] * (self.height + self.margin) + self.height / 2) + self.margin]
            pygame.draw.circle(self.screen, UNOCCUPIED, center, round(self.width / 2) - 2)

        robot_centers = []
        for agent, current in enumerate(self.currents):
            # draw a moving robot, based on current coordinates
            robot_centers.append([round(current[1] * (self.width + self.margin) + self.width / 2) + self.margin,
                                  round(current[0] * (self.height + self.margin) + self.height / 2) + self.margin])

        for color, robot_center in zip(self.colors, robot_centers):
            # draw robot position as red circle
            pygame.draw.circle(self.screen, color, robot_center, round(self.width / 2) - 2)

        pygame.display.flip()

        curr_time = 0
        while self.currents != self.goals:
            pygame.time.wait(1000)
            self.clear_positions(self.currents)
            new_poses = []
            for path, curr in zip(paths, self.currents):
                if path[0][2] == curr_time:
                    new_poses.append((path[0][0], path[0][1]))
                else:
                    new_poses.append(curr)
            paths = list(map(lambda p: p if len(p) == 1 else p[1:], paths))
            print(new_poses)
            self.set_positions(new_poses)
            self.draw_positions(new_poses)
            pygame.display.flip()
            curr_time += 1
        # set game tick
        self.clock.tick(20)

        # go ahead and update screen with that we've drawn
        pygame.display.flip()

    # be 'idle' friendly. If you forget this, the program will hang on exit
    pygame.quit()

    def clear_positions(self, currents):
        robot_centers = []
        for agent, current in enumerate(currents):
            robot_centers.append([round(current[1] * (self.width + self.margin) + self.width / 2) + self.margin,
                                  round(current[0] * (self.height + self.margin) + self.height / 2) + self.margin])

        for color, robot_center in zip(self.colors, robot_centers):
            # draw robot position as red circle
            pygame.draw.circle(self.screen, UNOCCUPIED, robot_center, round(self.width / 2) - 2)

    def draw_positions(self, currents):
        robot_centers = []
        for agent, current in enumerate(currents):
            robot_centers.append([round(current[1] * (self.width + self.margin) + self.width / 2) + self.margin,
                                  round(current[0] * (self.height + self.margin) + self.height / 2) + self.margin])

        for color, robot_center in zip(self.colors, robot_centers):
            # draw robot position as red circle
            pygame.draw.circle(self.screen, color, robot_center, round(self.width / 2) - 2)
