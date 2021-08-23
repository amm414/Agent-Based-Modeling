import random


"""
This Agent-Based Model (ABM) focuses on the basic Forest Fire (FF) model.

The model will simulate a forest in a discrete space via a basic x,y coordinate
system. Each cell will hold the value of:
    1. 'Dirt': Dirt is where trees can grow
    2. 'Foliage': Foliage represents the greenery of the Forest
    3. 'Fire': Fire is what we are simulating in relation to forest size.
    4. 'Burnt': Temporary description after foliage is burned down from a fire.
These Forest Cells will be the agents of this ABM for FF model. 

The goal of the model is to simulate a forest fire and how it is impacted by a few 
variables like the likelihood the fire will spread, the probability distribution of 
how many fires can start in each iteration, the growth distribution of new 
foliage, size of forest, and potentially others. These variables will ultimately be 
modifiable from the object instantiation. Users can modify the object and model parameters
and thus I call them **hyper-parameters**.

Current Hyper-Parameters Supported:
- Fire Spread Chance: the percent likelihood that the fire can spread to the
    neighboring cell. 100% is guaranteed to spread; 0% will never spread. May allow for 
    more complex fire spread distributions to take other factors into account (like 
    how long the fire has been raging)
- Length of Forest: the forest is a square (may allow for rectangles eventually). The 
    Forest will be created a an N-by-N discrete Grid using x,y coordinate system to 
    easily identify agent locations.
- Foliage Growth Rate: the growth rate is a distribution given in dictionary format that 
    depends on the number of foliage cells are in the neighboring cells (as a percent). 
    The goal is to allow for foliage to grow if foliage is nearby, however, if there is 
    a lot of nearby foliage, then the growth of new foliage may stagnate.
- Fire Start Distribution: The distribution of number of fires that start per iteration. The 
    distribution is a dictionary, as well. The goal is to allow for the user to alter how 
    common fires are. Important to note: the fire CAN start, but, if the fire starts on a 
    Forest Cell that is NOT foliage, there will be no fire.  


Future Parameters to Support:
- Different methods for how foliage grows. Possibly make each foliage agent have a 
    cycle for reproduction of once every x iterations and must have a neighboring 
    cell that is empty.
- Implement special foliage growth distribution for burnt cells. This would allow the 
    burnt organic material to allow for a quick rebound. This would model how periodic 
    fires help to improve the fertility of soil.

Potential Additions to the Model:
- Potentially will implement a weather/climate component to the model as well. I have 
    few details as this is at least 4+ months away (I first want to implement other models).

My Goals with the Model:

1. Add a GUI component to my website:
    I hope to integrate this program into my website and use basic JavaScript to consume the 
    simulation data generated based on inputs from the frontend.
2. Add GUI to My GitHub Repo:
    I hope to incorporate a PyGame-based GUI implementation that users can clone and easily use.
    I will use this PyGame and add other models that users can choose from within that frontend
    application.
3. I am interested in tracking the data to analyze:
    I am going to create a 'history' component to the ABMs to allow for data analyses to 
    identify patterns (emergent patterns in ABM is a primary goal to capture). I hope to analyze the 
    various impacts that altering the hyper-parameters have on the resulting model. These findings
    will be uploaded to my website as my academic-styled blog posts.
"""


# calculate the indices for a row
def get_row_indices(center: int, length: int, neighbor_range: int):
    """
    I do not recommend using, unless you know what to do...
    This function takes the center location x and generates the
    list of numbers that are within the neighbor_range with the
    limitation of the length (cannot extend past the length or
    go below 0). Examples:
    1. center: 1, length: 2, neighbor_range: 1 results in a
    list of [0, 1, 2]
    2. center: 1, length: 1, neighbor_range: 1 results in a
    list of [0, 1]
    3. center: 1, length: 4, neighbor_range: 2 results in a
    list of [0, 1, 2, 3]

    :param center: int; the center location to get the neighbor_range above and below
    :param length: int; the maximum value allowed (the minimum value allowed is 0)
    :param neighbor_range: int; The maximum number above and below the center value to
        return in resulting list
    :return: list; numbers in range of x-neighbor_range: x+neighbor_range, with limitations
        of length being the max allowed number in range and 0 being the minimum.
    """
    return [x for x in range(max(0, center-neighbor_range), min(length, center+1+neighbor_range))]


# calculate the matrix of indices for neighbors
def get_neighbor_matrix_indices(cell, max_length, neighbor_range=1):
    """
    Get the matrix of neighboring cells surrounding the cell given as the parameter. The goal is to
    return the 2D list of x,y locations representing all the neighbors within the given
    neighbor range.

    :param cell: tuple; (x,y) coordinate tuple of cell location to find neighbors for.
    :param max_length: int; the maximum range allowed for location coordinate values
        (0 is minimum, max_length is the maximum allowed)
    :param neighbor_range:
    :return: 2D List; returns list of x,y pairs representing the coordinates of neighbors of given cell
    """
    return [elem for sub in [[(a, b) for a in get_row_indices(cell[0], max_length, neighbor_range)] for b in
            get_row_indices(cell[1], max_length, neighbor_range)] for elem in sub]


def get_number_fires(distribution: dict):
    """
    Use the distribution to randomly get how many fires to start in the Forest.

    :param distribution: dict; the distribution of number of fires to start each iteration.
    :return: int; the number of fires to start from the distribution
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
    - history: tracks how the Forest Cell changes over time. Only really useful to
        do data analysis on after the fact.
    """
    agent_type: str
    location: tuple
    history: dict or None

    def __init__(self, agent_type, location, history=False):
        self.history = None
        self.agent_type = agent_type
        self.location = location
        if history:
            self.init_history()

    def init_history(self):
        """
        Simply inits the history of the cell. Should only be called on Forest Cell creation

        :return: None
        """
        self.history = {
            "Metadata": {"Number of Fires": 0, "Number of Times Foliage": 0, "Number of Times Dirt": 0},
            "States": []
        }
        self.update_history(0)

    def update_history(self, growth_iteration):
        """
        Updates the history whenever certain functions are called. Currently, it is when the
        set_agent_type is updated to a different value.

        :param growth_iteration: int; what is the current growth iteration number (represents Time in model).
        :return: None
        """
        new_entry = {
            "New Agent Type": self.agent_type,
            "Current Growth Iteration": growth_iteration,
        }
        self.history["States"].append(new_entry)
        if self.agent_type == "Fire":
            self.history["Metadata"]["Number of Fires"] += 1
        elif self.agent_type == "Foliage":
            self.history["Metadata"]["Number of Times Foliage"] += 1
        elif self.agent_type == "Dirt":
            self.history["Metadata"]["Number of Times Dirt"] += 1

    def set_agent_type(self, new_type, growth_iteration):
        """
        Sets the Forest Agent to the specified agent_type. Should add some error checking.

        :param new_type: str; the name of the new agent to set the Cell to.
        :param growth_iteration: int; the number of growth iterations that have occurred.
        :return: None
        """
        if not new_type == self.agent_type:
            self.agent_type = new_type
            if self.history is not None:
                self.history['agent_type_changes'].append((growth_iteration, self.agent_type))
                if new_type == 'Fire':
                    self.history['iterations_with_fire'].append(growth_iteration)

    def set_fire(self, growth_iterations):
        """
        Sets the Forest Cell agent_type to 'Fire' if the Forest Cell agent_type is 'Foliage' else nothing happens.
        :param growth_iterations: int; the number of growth iterations that have occurred.
        :return: Bool; True -> Forest Cell on Fire; False -> Forest Cell NOT on Fire
        """
        if self.agent_type == "Foliage":
            self.set_agent_type("Fire", growth_iterations)
            return True
        return False

    def set_to_burnt_down(self, growth_iterations):
        """
        Sets the Forest Cell agent_type to 'Burnt' if the Forest Cell agent_type is 'Fire' else nothing happens.
        :param growth_iterations: int; the number of growth iterations that have occurred.
        :return: Bool; True -> Forest Cell Burnt Down; False -> Forest Cell NOT Burnt Down
        """
        if self.agent_type == 'Fire':
            self.set_agent_type("Burnt", growth_iterations)
            return True
        return False

    def set_to_dirt(self, growth_iterations):
        """
        Sets the Forest Cell agent_type to Dirt if the Forest Cell agent_type is 'Burnt' else nothing happens.
        :param growth_iterations: int; the number of growth iterations that have occurred.
        :return: Bool; True -> Forest Cell set to Dirt; False -> Forest Cell NOT set to Dirt
        """
        if self.agent_type == "Burnt":
            self.set_agent_type("Dirt", growth_iterations)
            return True
        return False

    def set_to_foliage(self, growth_iterations):
        """
        Sets the Forest Cell agent_type to Foliage if the Forest Cell agent_type is 'Dirt' or 'Burnt' else nothing
        happens.
        :param growth_iterations: int; the number of growth iterations that have occurred.
        :return: Bool; True -> Forest Cell set to Dirt; False -> Forest Cell NOT set to Dirt
        """
        if self.agent_type == "Burnt" or self.agent_type == "Dirt":
            self.set_agent_type("Foliage", growth_iterations)
            return True
        return False


class ForestFireSim:
    """
    The Class that performs the simulation by collecting and organizing a discrete space (x,y coordinate plane) of
    ForestCells from above. This class allows the user to run iterations as long as possible. However, this class
    does capture data within the 'history' variable. That variable can become large. Additionally, for very
    long simulations, I recommend not collecting data within the individual agents.

    The class attributes are:
    1. growth_iterations: int; tracks how many growth iterations (turns of foliage spawning) have occurred.
    2. length: int; range between 10 and 100. The length of the Forest's discrete space (it is a square).
    3. fire_spread_chance: float; range between 0 and 1 (exclusive). The probability that the fire will spread to a
        neighboring ForestCell.
    4. foliage_growth_rate: dict; dictionary used for spawning new foliage based on percent of neighboring Forest Cells
        being Foliage. This variable represents the likelihood a Forest Cell with Dirt will spawn Foliage depending
        on the percent of neighboring Foliage Forest Cells there are. The key is the percent of neighbors with
        foliage and the value is the probability of foliage spawning.
    5. fire_start_dist: dict; represents the CDF for generating the number of fires to start each iteration of the
        program. The key represents the CDF and the value is the number of fires to start.
    6. forest: 2D List of ForestCell; the current Forest state.
    7. is_print: bool; True -> print to the CMD Line periodically throughout program; False -> No CMD Line printing
    8. history: dict; the JSON representation of data collected throughout the current run. This will track a few
        Metadata components like number of fires started, and the hyper-parameters that were set at initialization.
    9. agent_history: bool; whether to track the history of individual agents. Good for data collection for
        data analysis. However, this does add more time and memory requirements.


    Hyper-Parameters:

    The variables that are modifiable from the initialization of the ABM simulation. These variables will effect the
    results in different ways.
    - length
    - fire_spread_chance
    - foliage_growth_rate
    - fire_start_dist
    """
    growth_iterations: int
    length: int
    fire_spread_chance: float
    foliage_growth_rate: dict
    fire_start_dist: dict
    forest: list
    is_print: bool
    history: dict
    agent_history: bool

    def __init__(self, length=20, fire_spread_chance=0.50, foliage_growth_rate=None, fire_start_dist=None,
                 agent_history=False, is_print=False):
        """

        :param length: int; Hyper-Parameter; the length of the discrete space for the Forest.
        :param fire_spread_chance: float; Hyper-Parameter; the percent that fire will spread to neighboring
            'Foliage' Forest Cell
        :param foliage_growth_rate: dict; Hyper-Parameter; determines the likelihood that the Forest Cell with
            'Dirt' will spawn 'Foliage' depending on the percent of neighboring 'Foliage' Forest Cells.
        :param fire_start_dist: dict; Hyper-Parameter; determines the CDF for how many fires are started each
            iteration.
        :param agent_history: bool; whether to store the individual Forest Cell agent's data overtime.
        :param is_print: bool; whether to print results as we go to the CMD Line.
        """
        ################################################################
        # Instantiate the Hyper-Parameters
        # get Forest Length
        if 10 > int(length):
            raise ValueError("The Forest length must an integer and be greater than 10.")
        self.length = length
        # get fire_spread rate
        if not (0 < float(fire_spread_chance) < 1):
            raise ValueError("The fire_spread must be a probability. "
                             "Therefore must be between 1 and 0, but not 0 nor 1")
        self.fire_spread_chance = fire_spread_chance
        # get the foliage_growth_Rate
        if foliage_growth_rate is None:
            self.foliage_growth_rate = {0.01: 0.03, 0.26: .15, 0.51: .2, 0.76: .15, 1: 0.1}
        else:
            self.foliage_growth_rate = foliage_growth_rate
        # get the fire_start_distribution for # of fires started each iteration
        if fire_start_dist is None:
            self.fire_start_dist = {0.65: 0, 0.85: 1, 0.97: 2, 1: 3}
        else:
            self.fire_start_dist = fire_start_dist

        # End of the Hyper-Parameters
        ################################################################
        self.growth_iterations = 0
        self.is_print = bool(is_print)
        self.agent_history = False
        if bool(agent_history):
            self.agent_history = True

        # Create the Forest
        self.forest = []
        self.create_forest()
        self.init_history()
        self.track_history()
        if self.is_print:
            self.display_board(caption="The __init__ Function Forest Created...")

    def create_forest(self):
        """
        Generates the forest. Using a random number to have ~40% foliage and ~60% dirt.
        :return: None
        """
        for i in range(self.length):
            new_row = []
            for j in range(self.length):
                if random.randint(0, 100) > 40:
                    new_row.append(ForestCell("Foliage", (i, j), self.agent_history))
                else:
                    new_row.append(ForestCell("Dirt", (i, j), self.agent_history))
            self.forest.append(new_row)

    def init_history(self):
        """
        Inits the 'history' variable. This will track the state of the Forest over iterations and fires.
        :return: None
        """
        self.history = {
            "Metadata": {'Number of Fires': 0,
                         "Hyper-Parameters": {
                             "Forest Length": self.length,
                             "agent_history": self.agent_history,
                             "foliage_growth_rate": self.foliage_growth_rate,
                             "fire_start_dist": self.fire_start_dist,
                             "fire_spread_chance": self.fire_spread_chance,
                         }},
            "Forest": []
        }

    def track_history(self, fire_iteration=None):
        """
        Updates and tracks the current state of the Forest which will be lost after the next iteration.
        :param fire_iteration: int or None; if integer -> there is a fire that has been occurring for this number of
            fire iterations; else growth iteration and new foliage spawning
        :return: None
        """
        if fire_iteration is None:
            new_entry = {"Growth Iteration": self.growth_iterations}
        else:
            new_entry = {"Fire Spread Iteration": int(fire_iteration)}
            if fire_iteration == 0:
                self.history['Metadata']['Number of Fires'] += 1
        new_entry['Forest State'] = self.str_list_repr_forest()
        self.history["Forest"].append(new_entry)

    def simulate_iteration(self):
        """
        This simulates 1 iteration. An iteration is basically a unit of time. In this time, fires
        will start and burn off some of the forest (if there are any). Then, the forest will spawn new
        foliage as a growth_iteration. Finally, updates the history. May print at the end if param is set.
        :return: None
        """
        self.simulate_fires()
        self.simulate_foliage_growth()
        self.track_history()
        if self.is_print:
            self.display_board(caption=f'After Growth Iteration Number: {self.growth_iterations}')
            print("\n" + "*" * int(self.length + self.length/2) + "\n")

    def start_fires(self):
        """
        Generate the locations of the initial fires based on the number that is randomly generated through the
        fire_start_dist variable. If there are fires, return list of (x,y) coordinate tuple pairs representing the
        location within the forest the fire is located.
        :return: list; list of tuples, where the tuples are x, y pairings for the locations of fires.
        """
        fire_locations = []
        for i in range(get_number_fires(self.fire_start_dist)):
            x_coordinate = random.randint(0, self.length-1)
            y_coordinate = random.randint(0, self.length-1)
            if self.forest[x_coordinate][y_coordinate].set_fire(self.growth_iterations):
                fire_locations.append((x_coordinate, y_coordinate))
        return fire_locations

    def burn_off_fires(self, current_fire_locations, fire_counter=1):
        """
        Recursive Function. Will return to the simulate_fires() after no more fires to spread. The function
        takes the locations of fires and keeps spreading the fires until there are no more. Each function call
        represents 1 fire iteration. The goal is to allow the frontend to showcase the spread of the
        fire throughout the forest.
        :param current_fire_locations: list; list of (x,y) coordinate tuple pairs where there is fire.
        :param fire_counter: int; tracks the number of fire iterations computed.
        :return: None
        """
        new_fire_locations = []
        for fire_cell_location in current_fire_locations:
            neighbor_foliage_cells = get_neighbor_matrix_indices(fire_cell_location, self.length)
            for cell in neighbor_foliage_cells:
                if random.uniform(0, 1) <= self.fire_spread_chance:
                    if self.forest[cell[0]][cell[1]].set_fire(self.growth_iterations):
                        new_fire_locations.append(cell)
            # Now set this Fire Cell to dirt
            self.forest[fire_cell_location[0]][fire_cell_location[1]].set_to_burnt_down(self.growth_iterations)
        self.track_history(fire_iteration=fire_counter)
        if self.is_print:
            self.display_board(caption=f'Fire Iteration #{fire_counter}')
        if len(new_fire_locations) > 0:
            self.burn_off_fires(new_fire_locations, fire_counter=fire_counter+1)

    def burnt_to_dirt(self):
        """
        Iterates over the Forest and sets 'Burnt' Forest Cells to 'Dirt' Forest Cells.
        :return: None
        """
        for row in self.forest:
            for cell in row:
                cell.set_to_dirt(self.growth_iterations)

    def simulate_fires(self):
        """
        Simulates the fire of the model. This will get the number of fires to start. Then, will iteratively
        burn, spread, and extend the fire across the Forest. If printing is on, then there will be prints throughout
        the iterative fire spreading process.
        :return: None
        """
        fire_locations = self.start_fires()
        if len(fire_locations) > 0:
            self.track_history(fire_iteration=0)
            if self.is_print:
                self.display_board(caption=f'Fire Iteration #0')
            self.burn_off_fires(fire_locations, fire_counter=1)
            if self.is_print:
                self.display_board(caption="After Fires")
            self.burnt_to_dirt()
        else:
            if self.is_print:
                print("\nNo Fires Started\n")
        self.burnt_to_dirt()

    def get_foliage_counts(self, neighbors):
        """
        Counts the number of neighboring cells that have Foliage.
        :param neighbors: list; list of tuples (x, y coordinate pairs) of the neighboring cells' locations.
        :return: Int; number of neighboring cells that have Foliage.
        """
        number_foliage_cells = 0
        for cell in neighbors:
            if self.forest[cell[0]][cell[1]].agent_type == "Foliage":
                number_foliage_cells += 1
        return number_foliage_cells

    def simulate_foliage_growth(self):
        """
        Simulates the growth of new Foliage depending on the percent of neighboring cells that are 'Foliage'
        Forest Cells. Will only affect 'Dirt' and 'Burnt' Forest Cells (not yet implemented for 'Burnt' cells as
        they should be converted to Dirt already). 'Foliage' Forest Cells are unaffected.
        :return: None
        """
        self.growth_iterations += 1
        for row in self.forest:
            for cell in row:
                if cell.agent_type == "Dirt" or cell.agent_type == 'Burnt':
                    neighbors = get_neighbor_matrix_indices(cell.location, self.length)
                    number_foliage_cells = self.get_foliage_counts(neighbors)
                    if is_growth(number_foliage_cells, len(neighbors), self.foliage_growth_rate):
                        cell.set_to_foliage(self.growth_iterations)

    def display_board(self, caption=None):
        """
        Command-Line simplistic display of Forest.
        :return: string_board: the stringified board
        """
        string_board = ""
        for row in self.forest:
            for elem in row:
                if elem.agent_type == 'Foliage':
                    string_board += "T"
                elif elem.agent_type == "Fire":
                    string_board += "F"
                elif elem.agent_type == "Dirt":
                    string_board += "."
                elif elem.agent_type == "Burnt":
                    string_board += "B"
            string_board += "\n"
        if caption is not None:
            print(str(caption) + "\n")
        print(string_board + "\n")
        return string_board

    def str_list_repr_forest(self):
        """
        This is use to store the history of the Forest.
        This will be used to analyze and for frontend consumption.
        :return: list; char_forest ... 2D List containing the strings that are allowed
            ('Foliage', 'Fire', 'Dirt', 'Burnt')
        """
        char_forest = []
        for row in self.forest:
            new_row = []
            for elem in row:
                new_row.append(elem.agent_type)
            char_forest.append(new_row)
        return char_forest
