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


class VacuumUI:
    """Graphical interface for the vacuum cleaner environment"""
    def __init__(self, environment):
        self.env = environment
        self.root = tk.Tk()
        self.root.title("Vacuum cleaner")
        
        # interface
        self.canvas = tk.Canvas(self.root, width=400, height=200)
        self.canvas.pack()
        
        # Next button
        self.step_button = tk.Button(self.root, text="Next", command=self.step)
        self.step_button.pack()
        
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack()
        
        self.draw_environment()
    
    def draw_environment(self):
        self.canvas.delete("all")
        
        # locations A and B
        self.canvas.create_rectangle(50, 50, 150, 150, outline="black")
        self.canvas.create_rectangle(250, 50, 350, 150, outline="black")
        
        # labels
        self.canvas.create_text(100, 30, text="A")
        self.canvas.create_text(300, 30, text="B")
        
        # Show status (clean or dirty)
        if self.env.status[Location.A] == 'Dirty':
            self.canvas.create_text(100, 130, text="Dirty")
        if self.env.status[Location.B] == 'Dirty':
            self.canvas.create_text(300, 130, text="Dirty")
        if self.env.status[Location.A] == 'Clean':
            self.canvas.create_text(100, 130, text="Clean")
        if self.env.status[Location.B] == 'Clean':
            self.canvas.create_text(300, 130, text="Clean")
        
        if self.env.status[Location.A] == 'Clean' and self.env.status[Location.B] == 'Clean':
            self.canvas.create_text(200, 180, text="Finish")
        # Show agent
        agent_x = 100 if self.env.agent.location == Location.A else 300
        self.canvas.create_oval(agent_x-20, 80, agent_x+20, 120, fill="blue")
        
        # Show performance
        self.info_label.config(text=f"Performance: {self.env.agent.performance}")
    
    def step(self):
        percept = self.env.percept()
        action = self.env.agent.program(percept)
        self.env.execute_action(action)
        self.draw_environment()
    
    def run(self):
        # Run the interface
        self.root.mainloop()


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

# Main program
if __name__ == "__main__":
    env = Environment()
    agent = Agent(TableDrivenAgentProgram(table))
    env.add_agent(agent)
    
    # Create the graphical interface
    ui = VacuumUI(env)
    ui.run()