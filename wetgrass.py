'''
How to represent a table?
List of lists approach: node.prob[w1][w2][w3]...[wn] = p(node|w1,w2,w3,...,wn)
    Pros:
    - Can iterate with indices
    Cons:
    - difficult to read
Dictionary approact: node.prob["w1w2w3...wn"]
    Pros:
    - EXTREMELY readable
    - Can iterate with dict.keys()
    Cons:
    - Manually adding each probability
'''
from random import random, choice

# Rain is represented by R
# Sprinkler is represented by S
# Watson is represented by W
# Holmes is represented by H
# Negations are represented by a leading N

RP = 155/366 # probability of rain. 155 days of rain in 2020 (leap year) = 155/366
SP = (3*16*7)/365   # probability of sprinkler on: 3 hours * 7 days/week * 4 weeks/month * 4 months/year
WP = {"NRNS": 0.0001, "NRS": 0.0001,  "RNS": 0.999, "RS": 0.999}  # probability of wilson given rain.
HP = {"NRNS": 0.0001, "NRS": 0.8,     "RNS": 0.999, "RS": 0.9999999}  # probability of holmes given rain and sprinkler
RS = [["NRNS","NRS"],["RNS","RS"]]  # list of state combinations
MBs = {"R": "WHS" ,"S": "HR" ,"H": "RS", "W": "R"} # dict of markov blankets for each node
formulas = {"R": "alpha*RP*HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]*WP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]", # p(rain|world) = alpha * p(rain)*p(wilson|rain)*p(holmes|rain,sprinkler)
            "S": "alpha*SP*HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]*WP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]", # p(sprinkler|world) = alpha * P(sprinkler)*p(wilson|rain)*p(holmes|rain, sprinkler)
            "W": "alpha*WP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]", # p(W|world) = alpha * p(W|Rain,Sprinkler) = p(W|rain)
            "H": "alpha*HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]" # p(W|world) = alpha * p(W|Rain,Sprinkler) = p(W|rain)
             }


# Set states of observed nodes to observations, and all unobserved nodes to random
R = int(random() > RP)  # set state of rain given p(rain)
S = int(random() > SP)  # set state of sprinkler given p(sprinkler)
H = int(random() > HP[RS[R][S]])  # set state of Holmes given rain and sprinkler
W = int(random() > WP[RS[R][S]])  # set state of Watson given rain (value does not depend on sprinkler)
alpha = 1.0
for a in range(10):
    current = choice(["R","S","H","W"]) #  Randomly select a node
    print("current",current)
    mb = MBs[current] # Get its markov blanket
    # get the states in markov blanket
    mb_activations = {}
    for node in mb:
        mb_activations[node] = eval(node)
    print("markov blanket with states:",mb_activations)
    form = (formulas[current])
    print(form)
    print(str(alpha * RP * HP[RS[mb_activations["R"]][mb_activations["S"]]] * WP[RS[mb_activations["R"][mb_activations["S"]]]]))
    # no parents case:
    # p(rain | W_rain) = a . P(rain) . P(W|rain) . P(h|rain,sprinkler)
    # now calculate p(node=state| markov blanket) for each state (0 and 1)








