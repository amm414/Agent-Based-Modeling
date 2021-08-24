from ForestFire import ForestFireSim

def print_board(board):
    string_board = ""
    for row in board:
        for elem in row:
            if elem == 'Foliage':
                string_board += "T"
            elif elem == "Fire":
                string_board += "F"
            elif elem == "Dirt":
                string_board += "."
            elif elem == "Burnt":
                string_board += "B"
        string_board += "\n"
    string_board += "\n"
    print(string_board)


fire_sim = ForestFireSim(fire_spread_chance=0.5, is_print=False)

while fire_sim.growth_iterations < 20:
    fire_sim.simulate_iteration()

print("\n\n\n\n\nTry to Print out my Own Results from Dict. Response:\n")

ff_sim_history = fire_sim.history.get_dict_forest_history()
print("Metadata:")
for key, value in ff_sim_history['metadata']['hyper-parameters'].items():
    print(f'{key}: {value}')
print("Number of fires that occurred: " + str(ff_sim_history['metadata']['number_of_fires']))
print("Number of Growth Iterations that occurred: " +
      str(ff_sim_history['metadata']['number_of_growth_iterations']))

print("\n\nStart of Printing Forest States:\n")
print("*" * int(ff_sim_history['metadata']['hyper-parameters']['length'] +
                ff_sim_history['metadata']['hyper-parameters']['length'] / 2))
for entry in ff_sim_history['forest']:
    input("Hit enter to view the next iteration...")
    print(entry["iteration_type"] + " Iteration #" + str(entry["iteration_number"]))
    print_board(entry['state'])
    print("\n\n")
