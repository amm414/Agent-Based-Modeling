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
def get_neighbor_matrix_indices(cell: tuple, max_length: int, neighbor_range=1):
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


class ForestCellHistory:
    """
    The Class object collecting the history and data of the individual ForestCell
    agents if the user requests. Useful for data analysis, not much else.
    Following the composition-based development.
    """
    keep_history: bool
    metadata: dict
    agent_states: list

    def __init__(self, location: tuple, initial_agent_type: str, agent_history=False):
        """
        The initialization of Agent's history. This object will be 'None' if no history is
        being tracked at an individual agent level.
        :param location: tuple; the x, y coordinate pair tuple indicating agent location
        :param initial_agent_type: str; the initial agent type
        :param agent_history: bool, if set to False: no history will be tracked.
        """
        self.keep_history = False
        if agent_history:
            self.keep_history = True
            self.metadata = {'location': tuple(location), 'number_of_fires': 0,
                             'iterations_of_foliage': 0, 'iterations_of_dirt': 0
                             }
            self.agent_states = []
            self.update_state_change(initial_agent_type, 'growth', 0)

    def update_state_change(self, new_agent_type: str, iteration_type: str, iteration_number: int):
        """
        Updates the new, altered agent-state into the history.
        :param new_agent_type: str; the new agent type for the ForestCell agent.
        :param iteration_type: str; the type of iteration ('fire' or 'growth').
        :param iteration_number: int; the number of iterations that have occurred.
        :return: None
        """
        if self.keep_history:
            new_entry = {'agent_type': new_agent_type,
                         'iteration_type': str(iteration_type),
                         'iteration_number': int(iteration_number)}
            # update metadata
            if len(self.agent_states) > 0:
                if self.agent_states[-1]['agent_type'] == 'Foliage':
                    self.metadata['iterations_of_foliage'] += (iteration_number -
                                                               self.agent_states[-1]['iteration_number'])
                elif self.agent_states[-1]['agent_type'] == 'Dirt':
                    self.metadata['iterations_of_dirt'] += (iteration_number -
                                                            self.agent_states[-1]['iteration_number'])
            if new_agent_type == 'Fire':
                self.metadata['number_of_fires'] += 1
            self.agent_states.append(new_entry)

    def get_dict_history(self):
        """
        Takes the metadata and agent_states and combines them into a singular
        variable to return. It returns a dictionary (in the style of a JSON
        response object). Used to analyze after simulations are run.
        :return:
        """
        dict_history = {
            'metadata': self.metadata,
            'agent_states': self.agent_states
        }
        return dict_history


class ForestHistory:
    """
    The Class object that stores the data generated by the ForestFireSim.
    This follows the composition-based development of creating components to
    combine in a final object rather than rely on inheritance. Better for
    ABM as the instances of the ABM agents and models will have different parameters.
    """
    metadata: dict
    forest_states: list
    number_of_fire_iterations: list
    number_burnt_cells: list
    number_foliage_cells: list

    def __init__(self, length: int, agent_history: bool, foliage_growth_rate: float, fire_start_dist: dict,
                 fire_spread_chance: float):
        """
        Takes the parameters for the ForestFireSim and saves as 'metadata' within the history and collection
        of data gathered from simulation of ABM. Other metadata to track is the number of growth_iterations
        and number_of_fires that have occurred.
        :param length: int; length of Forest grid
        :param agent_history: bool; whether to track individual agent history.
        :param foliage_growth_rate: dict; the probability of foliage spawning depending on neighboring
            ForestCells having foliage themselves.
        :param fire_start_dist: dict; CDF that dictates the number of fires that are created per growth iteration.
        :param fire_spread_chance: float; the probability that fire spreads to the neighboring ForestCell.
        """
        self.metadata = {'number_of_fires': 0, 'number_of_growth_iterations': 0,
                         "hyper-parameters": {
                             "length": length,
                             "agent_history": agent_history,
                             "foliage_growth_rate": foliage_growth_rate,
                             "fire_start_dist": fire_start_dist,
                             "fire_spread_chance": fire_spread_chance,
                         },
                         "key": {
                             "Foliage": "T",
                             "Fire": "F",
                             "Burnt": "B",
                             "Dirt": "D",
                         }}
        self.forest_states = []
        self.number_burnt_cells = []
        self.number_of_fire_iterations = []
        self.number_foliage_cells = []

    def update_history(self, iter_type: str, iter_num: int, forest_representation: list):
        """
        Updates the history and data collection
        :param iter_type:
        :param iter_num:
        :param forest_representation:
        :return:
        """
        if iter_type.lower() == 'fire' and iter_num == 0:
            self.metadata['number_of_fires'] += 1
        elif iter_type.lower() == 'growth':
            # check if fire statistics update needed first
            if len(self.forest_states) > 0 and self.forest_states[-1]['iteration_type'].lower() == 'fire':
                self.update_new_fire_statistic()
            self.metadata['number_of_growth_iterations'] = iter_num
        new_entry = {
            "iteration_type": str(iter_type),
            "iteration_number": str(iter_num),
            "state": forest_representation
        }
        self.forest_states.append(new_entry)
        if iter_type.lower() == 'growth':
            # after saving the Forest World to history, use it to update the growth statistics
            self.update_growth_statistics()

    def count_elem(self, elem: str):
        """
        Counts the number of occurrences of the given elem (key of agent_type)
        :param elem: str; the key of the agent type.
        :return: number of times that agent type occurred
        """
        return [x for row in self.forest_states[-1]['state'] for x in row].count(elem)

    def update_new_fire_statistic(self):
        """
        Updates the statistics being gathered throughout the simulation. Uses the last forest_state saved.
        Saves statistics on number of cells caught fire (now they are 'burnt') and number of fire
        iterations it took to spread + end the fire.

        This may be expanded over time.
        :return: None
        """
        self.number_of_fire_iterations.append(self.forest_states[-1]['iteration_number'])
        self.number_burnt_cells.append(self.count_elem('B'))

    def update_growth_statistics(self):
        """
        Updates the statistics being gathered throughout the simulation. Uses the last forest_state saved.
        Saves statistics on number of foliage cells there are.

        This may be expanded over time.
        :return: None
        """
        self.number_foliage_cells.append(self.count_elem('T'))

    def get_dict_forest_history(self):
        """
        Return the metadata and forest states as a JSON-esque response object (Python dictionary).
        :return: dict; the dictionary of metadata and all forest states for the model.
        """
        history = {
            'metadata': self.metadata,
            'number_of_foliage_cells': self.number_foliage_cells,
            'number_of_fire_iterations': self.number_of_fire_iterations,
            'number_burnt_cells': self.number_burnt_cells,
            'forest': self.forest_states
        }
        return history


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
    history: ForestCellHistory

    def __init__(self, agent_type: str, location: tuple, history=False):
        self.agent_type = agent_type
        self.location = location
        self.history = ForestCellHistory(self.location, self.agent_type, agent_history=history)

    def set_agent_type(self, new_type: str, type_iteration: str, num_iterations: int):
        """
        Sets the Forest Agent to the specified agent_type. Should add some error checking.
        :param new_type: str; the new agent type the ForestCell becomes
        :param type_iteration: str; the type of iteration (either 'Fire' or 'Growth')
        :param num_iterations: int; the number of the iterations.
        :return: None
        """
        if not new_type == self.agent_type:
            self.agent_type = new_type
            self.history.update_state_change(new_type, str(type_iteration), int(num_iterations))

    def set_fire(self, num_iter: int):
        """
        Sets the Forest Cell agent_type to 'Fire' if the Forest Cell agent_type is 'Foliage' else nothing happens.
        :param num_iter: int; the number of iterations that have occurred.
        :return: Bool; True -> Forest Cell on Fire; False -> Forest Cell NOT on Fire
        """
        if self.agent_type == "Foliage":
            self.set_agent_type("Fire", 'fire', num_iter)
            return True
        return False

    def set_to_burnt_down(self, num_iter: int):
        """
        Sets the Forest Cell agent_type to 'Burnt' if the Forest Cell agent_type is 'Fire' else nothing happens.
        :param num_iter: int; the number of iterations that have occurred.
        :return: Bool; True -> Forest Cell Burnt Down; False -> Forest Cell NOT Burnt Down
        """
        if self.agent_type == 'Fire':
            self.set_agent_type("Burnt", 'fire',  num_iter)
            return True
        return False

    def set_to_dirt(self, num_iter: int):
        """
        Sets the Forest Cell agent_type to Dirt if the Forest Cell agent_type is 'Burnt' else nothing happens.
        :param num_iter: int; the number of iterations that have occurred.
        :return: Bool; True -> Forest Cell set to Dirt; False -> Forest Cell NOT set to Dirt
        """
        if self.agent_type == "Burnt":
            self.set_agent_type("Dirt", 'growth', num_iter)
            return True
        return False

    def set_to_foliage(self, num_iter: int):
        """
        Sets the Forest Cell agent_type to Foliage if the Forest Cell agent_type is 'Dirt' or 'Burnt' else nothing
        happens.
        :param num_iter: int; the number of iterations that have occurred.
        :return: Bool; True -> Forest Cell set to Dirt; False -> Forest Cell NOT set to Dirt
        """
        if self.agent_type == "Burnt" or self.agent_type == "Dirt":
            self.set_agent_type("Foliage", 'growth', num_iter)
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
    foliage_growth_rate: float
    fire_start_dist: dict
    forest: list
    is_print: bool
    history: ForestHistory
    agent_history: bool

    def __init__(self, length=20, fire_spread_chance=0.50, foliage_growth_rate=0.05, fire_start_dist=None,
                 agent_history=False, is_print=False):
        """
        :param length: int; Hyper-Parameter; the length of the discrete space for the Forest.
        :param fire_spread_chance: float; Hyper-Parameter; the percent that fire will spread to neighboring
            'Foliage' Forest Cell
        :param foliage_growth_rate: float; Hyper-Parameter; determines the likelihood that the Forest Cell with
            'Dirt' will spawn 'Foliage'.
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
        if not (0 < float(fire_spread_chance) <= 1):
            raise ValueError("The fire_spread must be a probability. "
                             "Therefore must be between 1 and 0, but not 0 nor 1")
        self.fire_spread_chance = fire_spread_chance
        # get the foliage_growth_Rate
        if 0.01 < float(foliage_growth_rate) < 0.21:
            self.foliage_growth_rate = float(foliage_growth_rate)
        else:
            self.foliage_growth_rate = 0.05  # Default value
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
        self.history = ForestHistory(self.length, self.agent_history, self.foliage_growth_rate,
                                     self.fire_start_dist, self.fire_spread_chance)
        self.history.update_history('growth', 0, self.str_list_repr_forest())
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

    def simulate_for_n_iterations(self, n: int):
        """
        Simulates the forest for n GROWTH iterations.
        :param n: int; represents the number of GROWTH iterations to simulate
        :return: None
        """
        for i in range(int(n)):
            self.simulate_iteration()

    def simulate_iteration(self):
        """
        This simulates 1 iteration. An iteration is basically a unit of time. In this time, fires
        will start and burn off some of the forest (if there are any). Then, the forest will spawn new
        foliage as a growth_iteration. Finally, updates the history. May print at the end if param is set.
        :return: None
        """
        self.simulate_fires()
        self.simulate_foliage_growth()
        self.history.update_history('growth', self.growth_iterations, self.str_list_repr_forest())
        self.burnt_to_dirt()
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
            if self.forest[x_coordinate][y_coordinate].set_fire(0):
                fire_locations.append((x_coordinate, y_coordinate))
        return fire_locations

    def burn_off_fires(self, current_fire_locations: list, fire_counter=1):
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
                    if self.forest[cell[0]][cell[1]].set_fire(fire_counter):
                        new_fire_locations.append(cell)
            # Now set this Fire Cell to dirt
            self.forest[fire_cell_location[0]][fire_cell_location[1]].set_to_burnt_down(fire_counter)
        self.history.update_history('fire', fire_counter, self.str_list_repr_forest())
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
            self.history.update_history('fire', 0, self.str_list_repr_forest())
            if self.is_print:
                self.display_board(caption=f'Fire Iteration #0')
            self.burn_off_fires(fire_locations, fire_counter=1)
            if self.is_print:
                self.display_board(caption="After Fires")
        else:
            if self.is_print:
                print("\nNo Fires Started\n")
        self.burnt_to_dirt()

    def get_foliage_counts(self, neighbors: list):
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
                    if random.uniform(0, 1) <= self.foliage_growth_rate:
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
            ('T' for Foliage/Tree, 'F' for Fire, 'D' for Dirt, 'B' for Burnt)
        """
        char_forest = []
        for row in self.forest:
            new_row = []
            for elem in row:
                new_row.append(self.history.metadata['key'][elem.agent_type])
            char_forest.append(new_row)
        return char_forest
