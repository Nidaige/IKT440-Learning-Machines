'''
Assignment text (pasted from canvas)
Assignment–Bayesian Networks
•Implement data structure for Wet Grass Bayesian Network (slide 7), including graph and probability tables
    - Graph can be done with nodes
    - Probability tables can be multi-dimensional arrays/lists:
        if the order is P1, P2, P3, then P(x|p1, p2, p3) = p[p1][p2][p3]
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

    def get_markov_blanket(self):
        children = self.Children
        parents = []
        for child in children:
            ch_parents = (child.Parents)
            for parent in ch_parents:
                if parent.Name!=self.Name:
                    parents.append(parent)
        return children + parents

    def update_probability_weighted(self,adjustment):
        self.Probability+=adjustment

class effectNode: # class for lawns/grass
    def __init__(self, Pa, Pr, Na):
        self.Parents = Pa
        self.Probabilities = Pr
        self.Name = Na
        self.ParentIds = [0,1]

    def evaluate(self):
        prob = 0
        parent_probs = []
        for a in self.Parents:
            parent_probs.append(a.Probability)
        # for a given node, multiply its conditional probabilities with the probability of the parent it depends on
        rain_prob = [1-parent_probs[0],parent_probs[0]]
        sprinkler_prob = [1.0,1.0]
        if len(self.Parents)!=1:
            sprinkler_prob = [1-parent_probs[1], parent_probs[1]]
        for a in range(len(self.Probabilities)):  # For each state of rain:
            r = self.Probabilities[a] # current subset of probs given current state of rain
            for b in range(len(r)):  # For each state of sprinkler:
                prob += r[b]*rain_prob[a]*sprinkler_prob[b]
        return min(prob,1)


    def roll(self):
        return random()<=self.evaluate()

    def get_markov_blanket(self):
        return self.Parents

    def update_probability(self,rain,sprinkler,val):
        self.Probabilities[rain][sprinkler] = val

    def update_probability_weighted(self,rain,sprinkler,val, adjustment):
        self.Probabilities[rain][sprinkler] = val+adjustment


def weighted_random(old_value):
    roll = random()
    adjustment = 0.05
    if roll>old_value:
        roll-=adjustment
    elif roll<old_value:
        roll+=adjustment
    return roll


# step 0: build node network
Rain = sourceNode(155/366, [], "Rain")
Sprinkler = sourceNode(0.0823, [], "Sprinkler")  # applying base rate to days without rain: 1/7*211/366 = 0.0823
Holmes = effectNode([Rain,Sprinkler],[[0,0.8],[0.99,1.0]], "Holmes")
Rain.add_child(Holmes)
Watson = effectNode([Rain], [[0],[1]], "Watson")
Rain.add_child(Watson)
Sprinkler.add_child(Holmes)
# step 1: set conditional probabilities
# done in initialization of nodes
# step 2: set value of observed nodes
''' what nodes are observed?
    - conditional probabilities for watson and holmes 
'''
# step 3: randomize non-observed nodes
''' what nodes are not observed?
    - Rain
    - Sprinkler
'''
Rain.set_probability(random())
Sprinkler.set_probability(random())
print("Prior: ",Rain.Name,Rain.Probability,Sprinkler.Name,Sprinkler.Probability)
# step 4: update probability of nodes based on their markov blanket
