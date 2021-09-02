# Agent-Based Modeling
 My Public Repository on Agent-Based Modeling (ABM). This will expand over time as I am interested in modeling using autonomous agents that choose actions based on factors and parameters entered into the model initially. 
 
# Contents

## Forest Fire Simulation

A simple agent-based model that shows forest growth and forest fires as a cycle. There are parameters accossiated with the model that can be modified to analyze certain variables more closely. Like the rate fire occurs or the growth rate of foliage/trees or the likelihood fire spreads to a neighboring tree/foliage cell. The model has a visualization built into my website [here](https://andrew-morgan-website.herokuapp.com/agent-based-modeling/forest-fire). 

The source code located here (under abm-source/ForestFireSimulation) with more details on the source code. I should upload some automated tests shortly (by September 8th). The model is simple, but an intial step into the ABM world. It uses some composition (rather than object-oriented inheritancce) to create the individual agents and world. I will improve the model over the next 1-2 months (through October 2021).


## Schelling Segregation ABM

Not uploaded to GitHub yet. The goal is to show that mild preferences for same-race neighboring agents cause segregation to become widespread. I will incorportate composition to allow each agent to potentially have different preferences and decision-making functions. The goal is to analyze how the "world" becomes segregated over time. I expect this to be completed by September 15th, 2021.
