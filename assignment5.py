# implement wet grass model

class Node:
    def __init__(self):
        self.Name = "Undefined" # name to use as key
        self.State = 0 # state / activation
        self.Connections = {} # connections + conditional probabilities
        self.Probability = 1.0 # flat probability

    def set_Name(self, new_Name):
        self.Name = new_Name

    def get_Name(self):
        return self.Name

    def add_Connection(self,other, conditional_probability, direction):
        self.Connections[other.Name] = {"node": other, "conditional_probability": conditional_probability, "direction": direction}

    def set_State(self, new_state):
        self.State = new_state

    def get_State(self):
        return self.State

    def set_Probability(self, new_Probability):
        print("set_prob")

    def get_Probability(self):
        print("get_prob")


# nodes
rain = Node()
sprinkler = Node()
watson_lawn = Node()
holmes_lawn = Node()


