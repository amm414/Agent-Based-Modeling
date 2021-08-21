import random


FOREST_AGENT_TYPES = ['dirt', 'tree', 'fire', 'burnt']
INITIAL_FOREST_AGENT_TYPES = ['dirt', 'tree']


def get_number_fires(distribution: dict):
    """
    :param distribution:
    :return:
    """
    number_fires = 0
    random_num = random.uniform(0, 1)
    for key in sorted(distribution.keys()):
        if random_num <= key:
            return distribution[key]
    return 0


class ForestCell:
    """
    The Class representing the individual cell of a forest in a discrete space.
    The cell will contain the following attributes:
    - agent_type: represents what the forest cell is
    - location: an (x, y) tuple that represents the
        coordinates of the forest cell (does not move)

    Will add to
    - history: will eventually track the past values of the cell
    """
    agent_type: str
    location: tuple
    # history: ??? (probably create additional object)
    history: dict or None

    def __init__(self, agent_type, location, history=False):
        self.agent_type = agent_type
        self.location = location
        self.history = None
        if history:
            self.history = {"location": self.location,
                            'agent_type_changes': [(0, self.agent_type)],
                            "iterations_with_fire": []}

    def set_agent_type(self, new_type, growth_iteration):
        if not new_type == self.agent_type:
            self.agent_type = new_type
            if self.history is not None:
                self.history['agent_type_changes'].append((growth_iteration, self.agent_type))
                if new_type == 'fire':
                    self.history['iterations_with_fire'].append(growth_iteration)

    def set_fire(self, growth_iterations):
        if self.agent_type == "tree":
            self.set_agent_type("fire", growth_iterations)
            return self.location
        return None



# This implementation is going to change over the next 2-4 weeks


class ForestFireSim:
    """
    The main object that creates the world and instantiates the individual agents.

    The __init__() will have hyper-parameters to affect the resulting simulated
    world. These hyper-parameters are what I will ultimately analyze later after
    adding the ability to collect data from it.

    There are 2 parameters to affect the output of model:
    1. print: will print to cmdline the forest (not very easy to tell what is happening)
    2. history: will dictate whether we wish to capture data. Right now, this is not
    a very useful parameter, but the program will eventually be able to track many
    different states, values, statistics of the simulation.

    Current Hyper-Parameters Supported:
    - Fire Spread Chance: the percent likelihood that the fire can spread to the
    neighboring cell. 1000% is guaranteed to spread; 0% will never spread.

    Future Hyper-Parameters to Support:
    - Fire Start (or Lightning Strike) Distribution: The distribution to see how many
    forest fires can start in a given growth iteration.
    - Tree Growth Rate: the likelihood a tree/foliage will grow in a cell depending on
    how many neighboring trees there are. (defaults to an inverted parabola-esque shape).
    - Size of World: Right now it is limited to an N-by-N world. May allow the world
     to become larger
    - How Fire Spreads: how the fire spreads may become modifiable to see if the
    8 surrounding cells versus the 4 directly adjacent cells being neighbors radically
    changes results (I feel that it should).
    - Potentially add 3 type of agent: Burnt Debris. Basically after foliage burns down,
    if becomes this new agent type. This new agent-type has increased likelihood of
    spawning a new tree/foliage in cell. Simulates that dead, organic material can become
    crucial to restarting life.


    Long-Term Goals: (May or May Not get To)
    1. Add a simple prey-predator component into model.
    2. Add a climate/weather component and its affects on the forest.
    """
    length: int
    max_growth_iterations: int
    fire_spread_chance: float
    fire_start_dist: dict
    tree_growth_rate: dict
    forest: list
    print: bool
    history: dict or None

    def init(self, fire_spread, history=False, print=False):
        # Printing Features:
        self.print = print

        # Currently Hard-Coded Set Parameters
        self.length = 50
        self.tree_growth_rate = {0.26: .2, 0.51: .4, 0.76: .3, 2: 0.15}
        self.fire_start_dist = {0.4: 0, 0.7: 1, 0.95: 2, 1: 3}

        # Controllable Hyper-Parameters
        self.fire_spread_chance = fire_spread

        # The history variable; probably need to create separate class for this eventually
        self.history = None
        self.growth_iterations = 0
        if history:
            self.history = {'Forest Cell States': [],
                            'Statistics by Growth Iteration': []}
            self.track_history()


        # Create the Forest
        self.forest = []
        self.create_forest()

    def create_forest(self):
        for i in range(self.length):
            new_row = []
            for j in range(self.length):
                if random.randint(0, 100) > 40:
                    new_row.append(ForestCell("tree", (i, j)))
                else:
                    new_row.append(ForestCell("dirt", (i, j)))
            self.forest.append(new_row)

    def simulate_growth_iteration(self):
        self.growth_iterations += 1
        self.start_fires()
        self.simulate_fires()
        self.simulate_foliage_growth()
        if self.history is not None:
            self.track_history()

    def track_history(self):
        """
        Track the changes to the Forest World
        This will be expanded between August 2021 and September 2021.
        :return:
        """
        raise NotImplementedError

    def start_fires(self):
        """
        Affects the Forest Cell States.
        Selects random locations in Forest to begin fires.
        Randomly selects number of fires from fire_start_dist (dictionary of distributions for number of fires).
        Sets the cell to a fire agent-type
        :return:
        """
        number_of_fires = get_number_fires(self.fire_start_dist)
        for i in range(number_of_fires):
            x_coordinate = random.randint(0, self.length)
            y_coordinate = random.randint(0, self.length)
            self.forest[x_coordinate][y_coordinate].set_fire(self.growth_iterations)








class ForestFireSimulationSimple:


    def __init__(self, length=10, max_growth_iter=100, initial_forest_rate=0.4, fire_spread=0.5,
                 tree_growth_rate=None, debug=False):
        """
        Inits the forest fire simulation class with initial values that will generate the
        world and current state of 'trees' vs 'soil.'

        :param length: the length of the discrete world (it is a 2-d square)
        :param max_growth_iter: How many iterations should be simulated (default to 100, max is 10_000)
        :param initial_forest_rate: the likelihood of initial world cell has 'tree' in it. Otherwise 'soil'
        :param fire_spread: the percent chance the fire spreads to the neighboring cells
        :param tree_growth_rate: the list of percents that relate to the likelihood new tree grows based
            on number of neighboring cells have a 'tree' in it.
        :param debug: whether we should print results to screen every turn and fire spread
        """
        self.length = min(length, 1_000)
        self.max_growth_iter = min(max_growth_iter, 10_000)
        self.fire_spread = fire_spread if 0 < fire_spread <= 1 else 0.5

        self.tree_growth_rate = tree_growth_rate or [0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0, 0]
        self.world = []
        self.create_world(initial_forest_rate)
        self.number_of_growth_iterations = 0
        self.debug = debug

    def create_world(self, initial_forest_rate):
        # called by the initiation of the class. Creates the forest as 2D list (values either 'tree' or 'soil')
        # create the world based on the initial_forest_rate specified by init function
        for i in range(self.length):
            new_row = []
            for j in range(self.length):
                if random.uniform(0, 1) < initial_forest_rate:
                    new_row.append('tree')
                else:
                    new_row.append('soil')
            self.world.append(new_row)

    def run_simulation(self):
        # keep simulating iterations until the specified max number of iterations is hit.
        if self.debug:
            self.display_forest()
        while self.number_of_growth_iterations < self.max_growth_iter:
            self.simulate_turn()

    def simulate_turn(self):
        # Grow the trees based on neighboring tree counts.
        # Then, have lightning strike and simulate the fire (if no tree struck, then no fire).
        self.number_of_growth_iterations += 1
        self.growth_iteration()
        if self.debug:
            self.display_forest()
        x, y = self.lightning_strike()
        self.simulate_fire(x, y)
        if self.debug:
            self.display_forest()

    # Start a fire on the square (must be a 'tree' cell)
    def lightning_strike(self):
        # generate a random x,y pair representing the coordinates of a lightning strike.
        # if that cell is a tree, the lightning starts a fire (return '(x,y)' tuple)
        # else return tuple of Nones representing No fire started
        x, y = random.randint(0, self.length-1), random.randint(0, self.length-1)
        if self.world[x][y] == 'tree':
            return x, y
        return None, None

    # keep iterating over the world until no fire exists
    # there will be a stack of fire_cells that track the cells that have fire and may spread
    def simulate_fire(self, x, y):
        # This simulates the fire until no fire remains. Fire can spread to the 8 neighboring cells.
        # The fire_cells is a stack that pops() a cell of fire and sees if neighboring cells have the
        # fire spread to it, and appends/push() those cells that the fire spreads to.
        # The fire is finished if fire_cells is empty.
        if x is None:
            return 0  # there was no fire started
        fire_cells, fire_iterations = [(x, y)], 0
        while not len(fire_cells) == 0:
            current_fire_cell = fire_cells.pop()
            fire_iterations += 1
            neighbors = get_neighbor_matrix_indices(current_fire_cell, self.length, self.length, neighbor_range=1)
            for neighbor in neighbors:
                if self.world[int(neighbor[0])][int(neighbor[1])] == 'tree' and check_fire_spread(self.fire_spread):
                    self.world[int(neighbor[0])][int(neighbor[1])] = 'fire'
                    fire_cells.append(neighbor)
            self.world[current_fire_cell[0]][current_fire_cell[1]] = 'soil'
            if self.debug:
                self.display_forest()
        return fire_iterations

    def growth_iteration(self):
        for i in range(self.length):
            for j in range(self.length):
                if self.world[i][j] == 'soil':
                    neighbor_counts = self.get_counts(i, j)
                    self.world[i][j] = self.update_soil_cell(neighbor_counts)

    def get_counts(self, i, j):
        neighbor_counts = {'soil': -1, 'tree': 0}
        for x in get_row_indices(i, self.length, 1):
            for y in get_row_indices(j, self.length, 1):
                if self.world[x][y] == 'tree':
                    neighbor_counts['tree'] += 1
                elif self.world[x][y] == 'soil':
                    neighbor_counts['soil'] += 1
        return neighbor_counts

    def update_soil_cell(self, neighbor_counts):
        if random.uniform(0, 1) < self.tree_growth_rate[neighbor_counts['tree']]:
            return 'tree'
        return 'soil'

    def display_forest(self):
        string_to_print = ''
        for row in self.world:
            for elem in row:
                if elem == 'tree':
                    string_to_print += 'T'
                elif elem == 'fire':
                    string_to_print += 'F'
                elif elem == 'soil':
                    string_to_print += ' '
            string_to_print += "\n"
        print("Current Growth Iteration: " + str(self.number_of_growth_iterations) + "\n\n" +
              string_to_print + "\n\n\n")




"""
These functions relate to finding the indices of the 'neighbors' to a given location within the 
grid world. It creates a square with cell as the center (in the form of a tuple '(x,y)'). The size 
of the square is set on the initial call to get_neighbor_matrix_indices. There needs to be an 
extra '+1' on the upper range as range() is exclusive on upper bound, not inclusive. 
"""


# calculate the indices for a row
def get_row_indices(center, length, neighbor_range):
    return [x for x in range(max(0, center-neighbor_range), min(length, center+1+neighbor_range))]


# calculate the matrix of indices for neighbors
def get_neighbor_matrix_indices(cell, max_x, max_y, neighbor_range=1):
    return [elem for sub in [[(a, b) for a in get_row_indices(cell[0], max_x, neighbor_range)] for b in
            get_row_indices(cell[1], max_y, neighbor_range)] for elem in sub]


def check_fire_spread(fire_spread_percent):
    return random.uniform(0, 1) < fire_spread_percent





