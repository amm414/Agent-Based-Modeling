from ForestFire import ForestFireSim

fire_sim = ForestFireSim(fire_spread=0.5, is_print=True)

while fire_sim.growth_iterations < 100:
    fire_sim.simulate_iteration()