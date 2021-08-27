from ForestFire import ForestFireSim
import time
import json


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


start_time = time.time()
fire_sim = ForestFireSim(length=50, fire_spread_chance=1, is_print=False)
fire_sim.simulate_for_n_iterations(100)
end_time = time.time()

print("Took: " + str(end_time - start_time) + " Time!\n\n\n\n\n\n")

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
    input_str = input("Hit enter to view the next iteration...")
    if input_str == "q":
        break
    print(entry["iteration_type"] + " Iteration #" + str(entry["iteration_number"]))
    print_board(entry['state'])
    print("\n\n")

with open("C:/GitHub/Agent-Based-Modeling/abm-source/ForestFireSimulation/source/data/testRun.json", 'w') as outfile:
    json.dump(ff_sim_history, outfile)
