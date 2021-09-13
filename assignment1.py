### Assignment tasks ###

#Implement the following program and justify your results:
# 1. Create 5 Tsetlin Automata with actions “No” and “Yes”
# 2. Count the number of Tsetlin Automata that outputs a “Yes”-action
# 3. If the number of “Yes”-actions is M Then:
#    If M = 0 OR 1 OR 2 OR 3:   Give each Automaton a reward with probability M ∗ 0.2, otherwise a penalty
#    If M = 4 OR 5:             Give each Automaton a reward with probability 0.6 − (M−3) ∗ 0.2, otherwise a penalty
# 4. Goto 2 ( repeat an arbitrary number of times)


# interpretation:
# 5 tsetlin automata with two actions. States are assigned in code (randomly chosen, but total number can be a variable)
# environment class that counts number of yes votes, then independently distributes rewards with probabilities stated in description
# the machine then repeats the vote + count and reward/Penalty
# evaluate performance on many runs (each run has its own number of loops/iterations)

### Modified Example code ###
import math
import random


class Environment:
    def __init__(self, c_1, c_2):
        self.c_1 = c_1
        self.c_2 = c_2

    def penalty(self, yesVotes):
        if (yesVotes in [0,1,2,3]): #if number of yes-votes is 0, 1, 2 or 3:
            if random.random() <= yesVotes*self.c_1: # penalize with probability M*0.2
                return True
            else:
                return False
        elif (yesVotes in [4,5]): # if number of yes-votes is 4 or 5:
            if random.random() <= self.c_2-(yesVotes-3)*self.c_1: # penalize with probability 0.6 - (M-2)*0.2
                return True
            else:
                return False


class Tsetlin:
    def __init__(self, n, id):
        # n is the number of states per action
        self.n = n
        self.id = id

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n + 1])

    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2 * self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        elif self.state > self.n:
            self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 0
        else:
            return 1

def createMachines(n,s):
    a=[]
    for i in range(n):  # determines number of automatas, adds to automatas array
        a.append(Tsetlin(s, i))
    return a

env = Environment(0.2, 0.6)
runs = 100
states = 10 # holds maximum number of states for each machine, to be iterated through
n = 5 # number of automatas to vote
x = 5000 # number of loops per run; how many times should the automatas vote and be penalized/rewarded?


for state in range(1,states+1):
    totalHistory = []
    totalVotes = 0
    print("State: "+str(state))
    for run in range(runs):
        voteHistory = []
        indexHistory = []
        automatas = createMachines(n,state)
            # Each run of this loop is a single run (repeat loop for multiple runs)
        for iteration in range(x): # runs the loop x times
            yesVotes = 0  # number of yes-votes
            for currentAutomata in automatas: # go through each automata
                action = currentAutomata.makeDecision() # current automata gives a vote; yes or no
                yesVotes += action # counts the vote (1 if yes, 0 if no)

            # voting run is done, time to count the votes and penalize accordingly
            for currentAutomata in automatas:  # go through each automata
                penalty = env.penalty(yesVotes)  # boolean; penalized or not.
                if penalty:
                    currentAutomata.penalize()
                else:
                    currentAutomata.reward()
            #print("Yes-votes: "+ str(yesVotes))
            voteHistory.append(yesVotes)
            indexHistory.append(iteration)
        #print(voteHistory)
        totalHistory.append([indexHistory,voteHistory])
        totalVotes+=voteHistory[len(voteHistory)-1]
    average=totalVotes/runs
    import matplotlib.pyplot as plt
    plt.xlim(0,x)
    plt.ylim(-1,n+1)
    plt.xlabel("Vote iteration")
    plt.ylabel("Yes-votes")
    plt.title("Votes per iteration from "+str(n)+" machines with "+str(state)+" states voting in "+str(x)+" iterations\nCurrently plotting "+str(runs)+" separate runs, with an average final value of "+str(average))
    for pt in range (runs):
        plt.plot(totalHistory[pt][0],totalHistory[pt][1])
    plt.grid(True)
    #plt.show()
    plt.savefig("Assignment 1 plots/"+str(state)+".png")


### End of example code ###