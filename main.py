import random
import tkinter as tk
from enum import Enum

class Location(Enum):
    A = "A"
    B = "B"

class Thing:
    """Represents any physical object that can appear in an Environment"""
    def __init__(self):
        self.__name__ = self.__class__.__name__
    
    def __repr__(self):
        return f'<{self.__name__}>'

class Dirt(Thing):
    pass

class Agent(Thing):
    """agent class (vacuum cleaner)"""
    def __init__(self, program):
        super().__init__()
        self.location = Location.A  # Initial location
        self.program = program      # Agent's program
        self.performance = 0        # Performance measure
        
class Environment:
    """Agent's environment (Location A and B)"""
    def __init__(self):
        self.status = {
            Location.A: random.choice(['Clean', 'Dirty']),
            Location.B: random.choice(['Clean', 'Dirty'])
        }
        self.agent = None
        self.percept_history = []
    
    def add_agent(self, agent):
        self.agent = agent
    
    def percept(self):
        """Returns the agent's current perception (location and status)"""
        return (self.agent.location, self.status[self.agent.location])
    
    def execute_action(self, action):
        """Executes the agent action and updates the environment"""
        if action == 'Right':
            self.agent.location = Location.B
            if self.status[self.agent.location] == 'Clean':
                self.agent.performance -= 1
        elif action == 'Left':
            self.agent.location = Location.A
            if self.status[self.agent.location] == 'Clean':
                self.agent.performance -= 1
        elif action == 'Suck':
            if self.status[self.agent.location] == 'Dirty':
                self.agent.performance += 10
                self.status[self.agent.location] = 'Clean'


def TableDrivenAgentProgram(table):
    """The agent selects an action based on the percept sequence"""
    percepts = []
    
    def program(percept):
        percepts.append(percept)
        action = table.get(tuple(percepts))
        print(percepts)
        return action if action else 'NoOp'
    
    print(percepts)
    
    return program

# Partial tabulation of the agent's function
table = {
    ((Location.A, 'Clean'),): 'Right',
    ((Location.A, 'Dirty'),): 'Suck',
    ((Location.B, 'Clean'),): 'Left',
    ((Location.B, 'Dirty'),): 'Suck',
    ((Location.A, 'Dirty'), (Location.A, 'Clean')): 'Right',
    ((Location.A, 'Clean'), (Location.B, 'Dirty')): 'Suck',
    ((Location.B, 'Clean'), (Location.A, 'Dirty')): 'Suck',
    ((Location.B, 'Dirty'), (Location.B, 'Clean')): 'Left',
    ((Location.A, 'Dirty'), (Location.A, 'Clean'), (Location.B, 'Dirty')): 'Suck',
    ((Location.B, 'Dirty'), (Location.B, 'Clean'), (Location.A, 'Dirty')): 'Suck'
}