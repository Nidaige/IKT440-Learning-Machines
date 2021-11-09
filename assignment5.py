from random import random, choice


class sourceNode:  # class for rain and sprinkler
    def __init__(self, p, c, n):
        self.Probability = p  # numerical probability
        self.Children = c  # list of child nodes
        self.Name = n  # string literal of name
        self.Rain_Probability = [[[0,0],[0,0]],[[0,0],[0,0]]]  # [Sprinkler][Holmes][Watson]
        self.Sprinkler_Probability = [[0,0],[0,0]]  # [Rain][Holmes]
        self.State = 0

    def set_probability(self, new_p):  # sets probability of activation
        self.Probability = new_p

    def add_child(self, new_c):  # Adds new child node to list of children
        self.Children.append(new_c)

    def roll(self):  # returns True with p = Probability
        if random() <= self.Probability:
            self.State=1
        else:
            self.State=0


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
        self.State = 0

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
        if random()<=self.evaluate():
            self.State = 1
        else:
            self.State = 0

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
Sprinkler = sourceNode(random(), [], "Sprinkler")
Holmes = effectNode([Rain,Sprinkler],[[0, 0.8],[0.99, 1.0]], "Holmes")
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

# step 4: update probability of nodes based on their markov blanket
# calculate p(rain|wet grass)
# p(rain|wet grass) = P(wet grass|rain) * p(rain)/p(wet grass)
# p(wet grass|rain) = sum of conditional probabilities of wet grass when rain
# p(rain) = estimated
# p(wet grass) = sum of all conditional probabilities times the probability of their condition
#       p(holmes grass wet) = P(holmes grass wet|rain)* p(rain) + p(hoolmes grass wet|sprinkler)* p(sprinkler)
# p(holmes grass wet|rain) is the sum of p(holmes grass wet|rain,sprinkler) and p(holmes grass wet|rain, not sprinkler)
# these are again dependent on p(sprinkler), which is unobserved(?)
# if we randomize the sprinkler's value, we get a 50% split of ON and OFF, which in turn make the lawn wet in 40% of the cases, regardless of sprinkler state
# p(holmes grass wet|rain) = p(rain)*0.4 = 620/3660 = 0.169


# stochastic simulation:
# choose 1 node randomly
# get its markov blanket
# for each node in blanket:
# if observed, set its value
# if not observed, set a random value
# calculate the probability of activation for the node given the state of the blanket
# say we look at holmes. His blanket consists of Rain and Sprinkler. P(Rain) is based on a good guess, P(Sprinkler) is randomly set.
# then we calculate the probabilities for holmes' lawn; P(wet|R,S), p(wet|!R,S), p(wet|R,!S) and p(wet|!R,!S)
# by keeping the values in each step, we can through iterations have rain's influence spread.
# sprinkler gets updated everytime holmes or rain is chosen.
# after calculating a distribution, randomly set a value/activation for the node based on the probabilities.
iterations = 15
# randomly set starting states based on probabilities
Sprinkler.roll()
Rain.roll()
Watson.roll()
Holmes.roll()
# begin iterating
for iteration in range(iterations):
    currentNode = choice([Rain,Sprinkler,Watson,Holmes])
    markovBlanket = currentNode.get_markov_blanket()
    if currentNode.Name == "Rain": # calculations if the node is Rain
        Rain.Rain_Probability[Sprinkler.State][Holmes.State][Watson.State] = 0 # how to calculate this?
            # p(rain|states) = P(states|rain)*P(states)/P(rain)?
    if currentNode.Name == "Sprinkler":  # calculations if the node is Sprinkler
        Sprinkler.Sprinkler_Probability[Rain.State][Holmes.State] = 0 # how to calculate this?
            # p(sprinkler|states) = P(states|sprinkler)*P(states)/p(Sprinkler)?
    if currentNode.Name == "Watson":  # calculations if the node is Watson
            Watson.Probabilities[Rain.State] = 0
    if currentNode.Name == "Holmes":  # calculations if the node is Holmes
            Holmes.Probabilities[Rain.State][Sprinkler.State] = 0

# start over? delete everything?
# dict approach, how does it allow for combined probabilities?
