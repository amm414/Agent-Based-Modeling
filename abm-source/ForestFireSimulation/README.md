# My Forest Fire Simulation Project

This subfolder will contain the source code to run the Forest Fire Simulation.
This subproject is a simple model that is designed to be easy as a first step into 
agent-based modeling (ABM). 

## Summary of Forest Fire Model

This model will simulate a forest in a discrete grid of X by X size. The trees 
or foliage will randomly grow from growth iteration to growth iteration (could be thought as 
time, like year-to-year). The likelihood that a tree will grow in an empty (dirt) cell 
will have a probability distribution depending on factors (such as number of neighboring 
trees). Additionally, each growth iteration (or year of growth) has the chance to 
start a forest fire. There maybe more than 1 fire (again, depends on probability distribution).
The fire will continue until no fire left, then growth iterations will continue. The fire can 
spread to any of the 8 neighboring cells (may become modifiable). There is, again, a 
probability with how the fire spreads. 

The goal of the model is to show how forests fluctuate from dense to sparse and how the 
denser the forest, generally, there must have been a lack of fire for years to allow 
the foliage to overgrow. Then, when a fire starts, it becomes destructive and wipes 
out much of the forest. 

I will take my finished models and perform statistical analyses on the data generated. 
These analyses will be uploaded both to this repository 
(under the Agent-Based-Modeling/abm-analyses subfolder) and the finalized written reports
to my website under my academic-styled blog posts section.

## Current Goals

- Finish the Forest Fire Simulation in a primitive state. Hopefully by end of August 2021.

- Finish the GUI for my website to showcase the model with basic visualization. 
  Slated for release by the start of September.  

- Incorporate a 'history' component to the model to track different variables and values
  over time to analyze later for macro-level trends. Hopefully, throughout 
  September 2021 - November 2021.  
  
- Create a PyGame version and release here on my GitHub. This is not expected 
  until October 2021 as I hope to start the Schelling Segregation ABM, and to analyze both 
  the Forest Fire Model and the Schelling Segregation ABM for trends.



## Future Ideas to Add

- Incorporate more hyper-parameters for the model to be chosen by the user to run 
  different types of simulations and view the effects from variables. I will implement 
  some hyper-parameters in the initial model releases, but I hope to expand the flexibility 
  of this model.
  
- May add new components that adds more randomness to growth of trees and spread of fire. 
  For example, I may include components to simulate the years of large tree growth 
  versus the years of drought and lackluster tree growth.

- I may add to this model weather and climate effects. This change would require a different 
  simulation of weather and more importantly climate. This could affect the likelihood of 
  rain or drought or heat waves or cold snaps; resulting in different effects on foliage 
  growth, fire spread (and starting), likelihood for tree/foliage to die off, ect. 
  Many of these components are not in the base model and would increase complexity.

