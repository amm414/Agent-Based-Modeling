import random


"""
The Schelling Segregation Model (ABM)
"""


class AgentHistory:
    history: dict
    metadata: dict

    def __init__(self, agent_type, happy_status, location):
        self.metadata = {
            "times_moved": 0,
            "iterations_happy": 0,
            "iterations_unhappy": 0,
            "times_moved": 0,
            "times_moved": 0,

        }
        self.update_metadata
        self.update_history(agent_type, happy_status, location, False)

    def update_metadata(self):


    def update_history(self, agent_type, happy_status, location, has_moved):



class Agent:
    agent_type: str
    is_happy: bool
    location: tuple
    history: AgentHistory


