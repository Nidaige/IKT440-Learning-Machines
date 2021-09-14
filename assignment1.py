
import math
import random

# Classes and methods

class Environment:
    def __init__(self, c_1, c_2):
        self.c_1 = c_1
        self.c_2 = c_2

    def penalty(self, yesVotes):
        if (yesVotes in [0,1,2,3]): #if number of yes-votes is 0, 1, 2 or 3:
            if random.random() <= yesVotes*self.c_1: # reward with probability M*0.2
                return False
            else:
                return True
        elif (yesVotes in [4,5]): # if number of yes-votes is 4 or 5:
            if random.random() <= self.c_2-(yesVotes-3)*self.c_1: # reward with probability 0.6 - (M-2)*0.2
                return False
            else:
                return True


class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n

        # Initial state selected randomly
        self.state = random.choice([self.n, self.n + 1])

    # machine gets reward, goes deeper into curent state
    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2 * self.n:
            self.state += 1

    # machine gets penalized, less certain about current state
    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        elif self.state > self.n:
            self.state -= 1

    # machine gives yes or no vote based on current state
    def makeDecision(self):
        if self.state <= self.n:
            return 0
        else:
            return 1
# creates n machines with s states
def createMachines(n,s):
    a=[]
    for i in range(n):  # determines number of automatas, adds to automatas array
        a.append(Tsetlin(s))
    return a

# Running the program #

env = Environment(0.2, 0.6) # Setup environment with the probabilities given
runs = 100 # Number of independent runs of the experiment
states = 100 # Number of states for each machine (Iterates from 1 to this number)
n = 5 # number of automatas
x = 500 # number of loops per run; how many times should the automatas vote and be penalized/rewarded?


state = 65
totalHistory = [] # array to hold combined history of each iteration with belonging number of votes
totalVotes = 0 # starting value of votes is 0
rewardsThisState = [] # holds history of rewards for this state

for run in range(runs): # iterate through the runs
    voteHistory = [] # holds how many voted yes each iteration (array)
    indexHistory = [] # holds the iterations (array)
    automatas = createMachines(n,state) # create n machines with "state" number of states
    rewardsThisRun = [] # holds rewards for this run (array)

    for iteration in range(x): # iterate x times, repeating vote-penalty cycle x times
        yesVotes = 0  # number of yes-votes
        rewardsThisIteration = 0 # number of rewards

        for currentAutomata in automatas: # go through each automata
            action = currentAutomata.makeDecision() # current automata gives a vote; yes or no
            yesVotes += action # counts the vote (1 if yes, 0 if no)
            # voting run is done, time to count the votes and penalize accordingly

        for currentAutomata in automatas:  # go through each automata
            penalty = env.penalty(yesVotes)  # boolean; penalized or not.
            if penalty: # penalized; give penalty
                currentAutomata.penalize()
            else: # not penalized; give reward
                currentAutomata.reward()
                rewardsThisIteration += 1 # add reward to counter
        # after conducting the vote, record number of votes, the iteration number, and the number of rewards given this iteration
        voteHistory.append(yesVotes)
        indexHistory.append(iteration)
        rewardsThisRun.append(rewardsThisIteration)
    # After all iterations are done, record the number of rewards and votes from this run
    rewardsThisState.append(rewardsThisRun)
    totalHistory.append([indexHistory,voteHistory])
    totalVotes+=voteHistory[len(voteHistory)-1]
# After all runs, it's time to find the average reward
totalRewards = [] # empty array to hold reward values
for u in range(x): # initialize it with x zeroes
    totalRewards.append(0)

for runIt in range(len(rewardsThisState)): # for each run that was conducted:
    currentRun = rewardsThisState[runIt]   # find the array of rewards for that run

    for iterIt in range(len(currentRun)): # for each reward in a run:
        currentReward = currentRun[iterIt] # find the reward for a given iteration
        totalRewards[iterIt] += (currentReward/runs) # add the reward to the total reward for that iteration, divided by total number of runs (sums up to the average)
        # at the end, totalRewards is an array of the average reward from each individual run.

# Setup plots
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2)
fig.set_size_inches(12.5, 8.5)
plt.xlim(0,x)
plt.ylim(-1,n+1)

# Format vote plot
ax[0].set_xlabel("Vote iteration")
ax[0].set_ylabel("Yes-votes")
ax[0].grid(True)
ax[0].set_title("Votes per iteration from "+str(n)+" machines with "+str(state)+" states voting in "+str(x)+" iterations\nCurrently plotting "+str(runs)+" separate runs, with an average final reward of "+str(totalRewards[len(totalRewards)-1]))

# Format reward plot
ax[1].set_xlabel("Vote iteration")
ax[1].set_ylabel("Average reward")
ax[1].grid(True)

# Plot
for pt in range (runs):
    ax[0].plot(totalHistory[pt][0],totalHistory[pt][1])
    ax[1].plot(totalHistory[pt][0], totalRewards)

# Show plot, or save to file

plt.show()
#plt.savefig("Assignment 1 plots/"+str(state)+".png")
plt.close("all")
