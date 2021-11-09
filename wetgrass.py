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
#   Not rain = NR,       Not Sprinkler = NS,    etc.

RP = 155/366 # probability of rain. 155 days of rain in 2020 (leap year) = 155/366
SP = ((3/24)*7*4*4)/365   # probability of sprinkler on: 3 hours * 7 days/week * 4 weeks/month * 4 months/year
WP = {"NRNS": 0.0001, "NRS": 0.0001,  "RNS": 0.999, "RS": 0.999}  # probability of wilson given rain and sprinkler. (Probability does not change with sprinkler, as it is independent)
HP = {"NRNS": 0.0001, "NRS": 0.8,     "RNS": 0.999, "RS": 0.9999999}  # probability of holmes given rain and sprinkler
RS = [["NRNS","NRS"],["RNS","RS"]]  # list of state combinations
MBs = {"R": "WHSR", "S": "WHSR", "H": "WHSR", "W": "WHSR", } # dict of markov blankets for each node
formulas = {"R": "alpha * RP * HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]] * WP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]",
            "S": "alpha * SP * HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]",
            "W": "alpha * WP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]",
            "H": "alpha * HP[RS[mb_activations[\"R\"]][mb_activations[\"S\"]]]",
             }
# Set states of observed nodes to observations, and all unobserved nodes to random
activations = {"R": 0, "S": 0, "H": 0, "W": 0}
totals = {"R": 0, "S": 0, "H": 0, "W": 0}
names = {"R": "It rains", "S": "The sprinkler is on", "H": "Holmes' grass is wet", "W": "Watson's grass is wet"}
probabilities = {"R": 0, "S": 0, "H": 0, "W": 0}
for runs in range(1000): # for 1000 runs of the algorithm (since subsequent probabilities are very dependent on the first set, producing either close to 0 or close to 1)
    R = int(random() < RP)  # set state of rain given p(rain)
    S = int(random() < SP)  # set state of sprinkler given p(sprinkler)
    H = int(random() < HP[RS[R][S]])  # set state of Holmes given the current rain and sprinkler
    W = int(random() < WP[RS[R][S]])  # set state of Watson given the current rain
    # trying with "true random" activation, not caring about probabilities
    states = {"R":R, "S":S, "H": H, "W":W}
    alpha = 1.0 # alpha value.
    for a in range(500):
        current = choice(["R","S","H","W"]) #  Randomly select a node
        mb_activations = {}  # get activation of each node (which are "on" i.e. is it raining, is the sprinkler on, wet grass)
        for node in "WHRS":
            mb_activations[node] = states[node]
        # get probability of <node> activating using formula
        # formula for each node only uses the markov blanket, so there is no need to explicitly get and use it here
        form = (formulas[current])
        new_probability = eval(form)
        new_activation = int(random() < new_probability)
        #print("New activation",new_activation)
        totals[current]+=1
        activations[current]+=new_activation
        #print(current,new_activation,new_probability)
print("Final probabilities:")
for a in totals.keys():
    try:
        print("P(",names[a],") = ",activations[a]/totals[a])
        probabilities[a] = activations[a]/totals[a]
    except:
        print(a,"didn't get updated")
    # set new value/probability of <node> based on new distribution?

print("Queries")
print("P(Rain|Holmes,Watson) = P(Holmes|Rain)*P(Watson|Rain)*P(Rain)/ P(Watson)*P(Holmes) = ",(HP["RNS"]*(1-probabilities["S"]) + HP["RS"]*probabilities["S"])*WP["RNS"]*probabilities["R"]/(probabilities["H"]*probabilities["W"]))
print("P(Rain|Sprinkler,Holmes = P(Sprinkler,Holmes|Rain)*P(Rain)/P(Sprinkler)*P(Holmes) = ",probabilities["S"]*(HP["RNS"]*(1-probabilities["S"]) + HP["RS"]*probabilities["S"])*probabilities["R"]/(probabilities["S"]*probabilities["H"]))
print("P(Sprinkler|Rain) = P(Rain|Sprinkler)*P(Sprinkler)/P(Rain) = ",probabilities["S"]*probabilities["R"]/probabilities["R"])
print("P(Rain|Watson) = P(Watson|Rain) * P(Rain)/P(Watson) = ", WP["RNS"]*probabilities["R"]/probabilities["W"])
exit()