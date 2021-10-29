'''
Assignment text (pasted from canvas)
Assignment–Bayesian Networks
•Implement data structure for Wet Grass Bayesian Network (slide 7), including graph and probability tables
•Assign appropriate probabilities to the probability tables
•Implement Stochastic Simulation inference scheme
•Estimate P(Rain | Holmes’ Grass is Wet, Watson’s  Grass is Wet) and 3 other queries you select.


Network model

- Nodes
    - Rain
    - Sprinkler
    - Watson's lawn
    - Holmes' lawn

- Connections/edges:
    - Rain to watson's lawn and holmes' lawn
    - Sprinkler to watson's lawn
    - No connection between sprinkler and holmes' lawn
    - No connection between watson's lawn and holmes' lawn

- Probability
    - Holmes' lawn will have an activation probability given Rain is active/has a given value
    - Watson's lawn will have an activation probability given Rain is active/has a given value
    - Watson's lawn will have an activation probability given Sprinkler is active/has a given value


[Rain]                          [Sprinkler]
True = P(Rain)                  True = P(Sprinkler)

[Holmes' Lawn]                  [Watson's lawn]

R |   P                         R|S|P
T | P(H|R)                      T | T | P(W|R)  + P(W|S)
F | P(H|!R)                     T | F | P(W|R)  + P(W|!S)
                                F | T | P(W|!R) + P(W|S)
                                F | F | P(W|!R) + P(W|!S)

How to represent probability tables on nodes?  - 2D lists

Each node is a class Node
    - List of parents
    - List of lists of probabilities
    - Parents are not affected by children, so having a list of children is kind of useless

'''
from random import random


class sourceNode:  # class for rain and sprinkler
    def __init__(self, p, c, n):
        self.Probability = p  # numerical probability
        self.Children = c  # list of child nodes
        self.Name = n  # string literal of name

    def set_probability(self, new_p):  # sets probability of activation
        self.Probability = new_p

    def add_child(self, new_c):  # Adds new child node to list of children
        self.Children.append(new_c)

    def roll(self):  # returns True with p = Probability
        return random() <= self.Probability

class effectNode: # class for lawns/grass
    def __init__(self, Pa, Pr, Na):
        self.Parents = Pa
        self.Probabilities = Pr
        self.Name = Na

    def Evaluate(self):
        prob = 0
        for parent in self.Parents:
            prob += (self.Probabilities[parent.Name]*parent.Probability)
        return prob

    def Roll(self):
        return random()<=self.Evaluate()


# Probabilities for rain and sprinkler
p_Rain = 2/21  # Two days every three weeks
p_Sprinkler = 1/7  # Three times per week for four months a year

# init source nodes (Rain and Sprinkler)
Rain = sourceNode(2/21, [], "Rain")
Sprinkler = sourceNode(1/7, [], "Sprinkler")

# Conditional probabilities for watson
p_Watson_rain = 1.0  # p(watson|rain)
p_Watson_not_rain = 0.0  # p(watson|not rain)
p_Watson_sprinkler = 0.8  # p(watson|sprinkler)
p_Watson_not_Sprinkler = 0.0  # p(watson| not sprinkler

# init watson node with rain and sprinkler nodes as parents. Add Watson as child for rain and sprinkler nodes
Watson = effectNode([Rain,Sprinkler],{"Rain":p_Watson_rain, "NOT Rain":p_Watson_not_rain, "Sprinkler":p_Watson_sprinkler, "NOT Sprinkler": p_Watson_not_Sprinkler}, "Watson")
Rain.add_child(Watson)
Sprinkler.add_child(Watson)

# conditional probabilities for holmes
p_Holmes_Rain = 1.0  # p(holmes|rain)
p_Holmes_not_Rain = 0.0  # p(holmes|not rain)

# init holmes node with rain as parent. Add holmes as child for rain node
Holmes = effectNode([Rain], {"Rain":p_Holmes_Rain, "NOT Rain": p_Holmes_not_Rain}, "Holmes")
Rain.add_child(Holmes)

# Evaluating probability of activation given parents
print(Watson.Name,Watson.Evaluate())
print(Holmes.Name,Holmes.Evaluate())

