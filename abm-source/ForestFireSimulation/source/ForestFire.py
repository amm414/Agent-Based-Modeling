import random

# This ABM is still a work in progress. It will be improved by the middle of September.
#
# However, I still have future plans after September to further expand this model.


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
def get_neighbor_matrix_indices(cell, max_length, neighbor_range=1):
    return [elem for sub in [[(a, b) for a in get_row_indices(cell[0], max_length, neighbor_range)] for b in
            get_row_indices(cell[1], max_length, neighbor_range)] for elem in sub]


def get_number_fires(distribution: dict):
    """
    :param distribution: the dictionary distribution for number of fires to start
    :return:
    """
    random_num = random.uniform(0, 1)
    for key in sorted(distribution.keys()):
        if random_num <= key:
            return distribution[key]
    return 0


def is_growth(number_foliage_cells, number_of_neighboring_cells, distribution):
    """
    Returns whether growth occurs in this 'dirt' cell (already confirmed to be dirt earlier).

    :param number_foliage_cells: number of neighboring cells that are foliage
    :param number_of_neighboring_cells: total number of neighboring cells
    :param distribution: the given distribution related to the percent of neighboring cells that are
            foliage cells. Dictates how likely a foliage cell will grow here.
    :return: True (growth of foliage occurs) and False (remains dirt)
    """
    foliage_ratio = number_foliage_cells / number_of_neighboring_cells
    for key in sorted(distribution.keys()):
        if foliage_ratio <= key:
            return True if random.uniform(0, 1) <= distribution[key] else False


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
                if new_type == 'Fire':
                    self.history['iterations_with_fire'].append(growth_iteration)

    def set_fire(self, growth_iterations):
        if self.agent_type == "Foliage":
            self.set_agent_type("Fire", growth_iterations)
            return self.location
        return None


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
    - Foliage Growth Rate: the likelihood a foliage will grow in a cell depending on
    how many neighboring cells with foliage there are. (defaults to an inverted parabola-esque shape).
    - Size of World: Right now it is limited to an N-by-N world. May allow the world
     to become larger
    - How Fire Spreads: how the fire spreads may become modifiable to see if the
    8 surrounding cells versus the 4 directly adjacent cells being neighbors radically
    changes results (I feel that it should).
    - Potentially add 3 type of agent: Burnt Debris. Basically after foliage burns down,
    if becomes this new agent type. This new agent-type has increased likelihood of
    spawning a new foliage in cell. Simulates that dead, organic material can become
    crucial to restarting life.


    Long-Term Goals: (May or May Not get To)
    1. Add a simple prey-predator component into model.
    2. Add a climate/weather component and its affects on the forest.
    """
    growth_iterations: int
    length: int
    fire_spread_chance: float
    fire_start_dist: dict
    foliage_growth_rate: dict
    forest: list
    is_print: bool
    history: dict or None

    def __init__(self, fire_spread, history=False, is_print=False):
        # Printing Features:
        self.is_print = is_print

        # Currently Hard-Coded Set Parameters
        self.length = 50
        self.foliage_growth_rate = {0.26: .2, 0.51: .4, 0.76: .3, 2: 0.15}
        self.fire_start_dist = {0.5: 0, 0.8: 1, 0.95: 2, 1: 3}

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
                    new_row.append(ForestCell("Foliage", (i, j)))
                else:
                    new_row.append(ForestCell("Dirt", (i, j)))
            self.forest.append(new_row)

    def simulate_iteration(self):
        if self.is_print:
            self.display_board(caption="Before Fires")

        self.simulate_fires()
        self.simulate_foliage_growth()

        if self.history is not None:
            self.track_history()
        if self.is_print:
            self.display_board(caption=f'After Growth Iteration ({self.growth_iterations}) Fires')

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
        fire_locations = []
        for i in range(get_number_fires(self.fire_start_dist)):
            x_coordinate = random.randint(0, self.length)
            y_coordinate = random.randint(0, self.length)
            self.forest[x_coordinate][y_coordinate].set_fire(self.growth_iterations)
            fire_locations.append((x_coordinate, y_coordinate))
        return fire_locations

    def burn_off_fires(self, fire_locations):
        """
        This function spreads and burns out all the existing fires.
        Keep appending the cells that have been ignited by the fire.
        When no more forest cells are alight with fire, stop the burning.

        :param fire_locations: the stack of Forest cells that are on fire.
        :return: None
        """
        while len(fire_locations) > 0:
            current_fire_cell = fire_locations.pop()
            neighbor_foliage_cells = get_neighbor_matrix_indices(current_fire_cell, self.length)
            for cell in neighbor_foliage_cells:
                if random.uniform(0, 1) <= self.fire_spread_chance:
                    self.forest[cell[0]][cell[1]].set_fire(self.growth_iterations)
                    fire_locations.append(cell)

    def simulate_fires(self):
        """
        generates the locations of fires. The number of fires started depends on the
        distribution (will become hyper-parameter).
        Goes through list adding new foliage Forest Cells that become ignited.
        The new foliage Forest Cells are added by the fire spread rate (another future hyper-param)
        :return:
        """
        fire_locations = self.start_fires()
        if len(fire_locations) > 0:
            self.burn_off_fires(fire_locations)
            if self.is_print:
                self.display_board(caption="After Fires")
        else:
            if self.is_print:
                print("\nNo Fires Started\n")

    def get_foliage_counts(self, neighbors):
        number_foliage_cells = 0
        for cell in neighbors:
            if self.forest[cell[0]][cell[1]] == "Foliage":
                number_foliage_cells += 1
        return number_foliage_cells

    def simulate_foliage_growth(self):
        """
        Simulates a singular growth iteration.
        Starts a new growth iteration and adds '1' to the counter. Only allow
        foliage growth to occur on the 'Dirt' cells. Otherwise, ignore the cell
        as there already exists foliage.

        :return: None
        """
        self.growth_iterations += 1
        for row in self.forest:
            for cell in row:
                if self.forest[cell[0]][cell[1]].agent_type == "Dirt":
                    neighbors = get_neighbor_matrix_indices(cell, self.length)
                    number_foliage_cells = self.get_foliage_counts(neighbors)
                    if is_growth(number_foliage_cells, len(neighbors), self.foliage_growth_rate):
                        self.forest[cell[0]][cell[1]].set_type("Foliage", self.growth_iterations)

    def display_board(self, caption=None):
        """
        Command-Line simplistic display of Forest.
        :return: string_board: the stringified board
        """
        string_board = ""
        for row in self.forest:
            for elem in row:
                string_board += str(elem.agent_type)[0]
            string_board += "\n"
        if caption is not None:
            print(str(caption) + "\n")
        print(string_board + "\n")
