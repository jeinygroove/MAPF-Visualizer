import utils
import random
from gui import Animation

OBSTACLE = 255
UNOCCUPIED = 0

if __name__ == '__main__':

    """
    set initial values for the map occupancy grid
    |----------> y, column
    |           (x=0,y=2)
    |
    V (x=2, y=0)
    x, row
    """
    x_dim = 100
    y_dim = 80
    view_range = 5
    grid = utils.ReadMapFromMovingAIFile('maze-32-32-2.map')
    paths = utils.ReadAgentsPathsFromFile('lol.txt')

    number_of_colors = len(paths)
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

    starts = list(map(lambda path: path[0], paths))
    goals = list(map(lambda path: path[-1], paths))

    gui = Animation(title="D* Lite Path Planning",
                    width=20,
                    height=20,
                    margin=0,
                    x_dim=x_dim,
                    y_dim=y_dim,
                    starts=starts,
                    goals=goals,
                    grid=grid.cells,
                    colors=colors,
                    viewing_range=view_range)

    gui.run_game(paths=paths)
