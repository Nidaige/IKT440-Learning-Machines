import math
import random


def evaluate_condition(observation, condition):     # copied from https://github.com/cair/TsetlinMachineBook/blob/main/Chapter_1.ipynb
    truth_value_of_condition = True
    for feature in observation:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition





# Evaluating rules part ------------------------------------------------------------------

# Positive Features
Menopge40 = 'Menopge40'
Menoplt40 = 'Menoplt40'
Menopremeno = 'Menopremeno'
Inv02 = 'Inv02'
Inv35 = 'Inv35'
Inv68 = 'Inv68'
DegMalg3 = 'DegMalg3'
DegMalg2 = 'DegMalg2'
DegMalg1 = 'DegMalg1'

# Negative Features
NotMenopge40 = 'NOT Menopge40'
NotMenoplt40 = 'NOT Menoplt40'
NotMenopremeno = 'NOT Menopremeno'
NotInv02 = 'NOT Inv02'
NotInv35 = 'NOT Inv35'
NotInv68 = 'NOT Inv68'
NotDegMalg3 = 'NOT DegMalg3'
NotDegMalg2 = 'NOT DegMalg2'
NotDegMalg1 = 'NOT DegMalg1'

# all patients from data set
patients = [
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:True,  Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:False, Menoplt40:True, Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:False, Inv68:True,   DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:True,  DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:False, DegMalg1:True},
]

# array to hold recurrence verdict of each patient
patientsRecurrence = []

# Rule definitions
rule1 = [DegMalg3, NotMenoplt40]  # Rule 1: Deg Malg 3 and Not Menop. Lt 40 means recurrence
rule2 = [DegMalg3, NotMenoplt40]  # Rule 2: Same as Rule 1
rule3 = [Inv02]  # Rule 3: If Inv. Nodes 0-2, then not recurrence


# Iterate through patients and evaluate each rule
for patient in patients:
    patientCount = 0  # counts number of indicators for or against recurrence

    if evaluate_condition(patient, rule1):  # outcome of rule 1
        patientCount += 1

    if evaluate_condition(patient, rule2):  # outcome of rule 2
        patientCount += 1

    if evaluate_condition(patient, rule3):  # outcome of rule 3
        patientCount -= 1  # Special case: r3 indicates non-recurrence when true, hence the minus

    patientsRecurrence.append(patientCount)
for a in range(len(patientsRecurrence)):
    print("Patient: "+str(a)+", Recurrence votes: "+str(patientsRecurrence[a]))

print("|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|")
# Type 1 and 2 feedback part --------------------------------------------------------------------------



class Memory: # Class for a memory unit
    def __init__(self, forget_value, memorize_value, memory): # constructor call
        self.memory = memory # initialize memory
        self.forget_value = forget_value # initialize forget_value
        self.memorize_value = memorize_value # initialize memorize_value

    def get_memory(self): # returns the whole memory
        return self.memory

    def get_literals(self): # returns the features represented in the memory
        return list(self.memory.keys())

    def get_condition(self): # returns a rule learned by the memory
        condition = [] # it starts empty
        for literal in self.memory: # check all literals / features:
            if self.memory[literal] >= Memory_Init_Val: # if they are in the "remembered" area, keep them
                condition.append(literal)
        return condition # return the learned rule

    def memorize(self, literal): # increments "remember" value to make a feature/literal more memorized with p = memory_value
        if random.random() <= self.memorize_value and self.memory[literal] < Memory_Size:
            self.memory[literal] += 1

    def forget(self, literal): # decrements "remember" value to make a feature/literal less memorized - more forgotten, with p = forget_value
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal): # same as memorize, but always remembers, p = 1
        if self.memory[literal] < Memory_Size:
            self.memory[literal] += 1

def type_i_feedback(observation, memory): # function that gives type i feedback on a memory based on an observation:
    remaining_literals = memory.get_literals() # gets all the literals (features) in memory
    if evaluate_condition(observation, memory.get_condition()) == True: # check if the observation matches the currently learned rule
        for feature in observation: # iterate through features in observation
            if observation[feature] == True: # if the feature exists
                memory.memorize(feature) # memorize the feature
                remaining_literals.remove(feature)
            elif observation[feature] == False: # if the feature does not exist in the observation
                memory.memorize('NOT ' + feature) # memorize the negative (NOT) feature instead
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals: # for any non-memorized feature,
        memory.forget(literal) # forget about it


def type_ii_feedback(observation, memory): # function that gives type 2 feedback:
    if evaluate_condition(observation, memory.get_condition()) == True: # check if the observation matches the currently learned rule
        for feature in observation: # for any feature in the observation,
            if observation[feature] == False: # if the feature exists and is False,
                memory.memorize_always(feature) # memorize the feature as is
            elif observation[feature] == True: # if the feature exists, and is True,
                memory.memorize_always('NOT ' + feature) # memorize the negative (NOT) feature instead.

def classify(observation, recurrence_rules, non_recurrence_rules): # function that returns "Recurrence" or "Non-recurrence", depending on how many rules vote for/against
    vote_sum = 0 # initially 0 votes
    for rule in recurrence_rules: # check each rule that predicts recurrence
        if evaluate_condition(observation, rule) == True: # if rule matches, add a vote for recurrence
            vote_sum += 1
    for rule in non_recurrence_rules: # check each rule that predicts non-recurrence,
        if evaluate_condition(observation, rule) == True: # if rule matches, add vote for non-recurrence, aka a negative vote for recurrence
            vote_sum -= 1
    if vote_sum >= 0: # return the most frequent classification among the rules:
        return "Recurrence"
    else:
        return "Non-recurrence"

Recurring_Patients = [ # list of patients within the recurring class
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:True,  Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:False, Inv68:True,   DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
]

Non_Recurring_Patients = [ # list of patients within the non-recurring class
{Menopge40:False, Menoplt40:True, Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:True,  DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:False, DegMalg1:True},
]

All_Patients = [Recurring_Patients,Non_Recurring_Patients] # list of all patients

Memory_Size = 500 # The total range of how forgotten/remembered a given feature is
Memory_Init_Val = math.floor(Memory_Size * 0.5) # The initial value of every feature in memory. Half of the memory size
Memory_Iterations = 1000 # How many remember/forget iterations will be done with the memory before extracting a rule?
Rule_Count = 100 # How many rules will we find?
Rules = [[],[]] # array holding array of recurring rules and non-recurring rules
Remember_Value = 0.8 # What is probability of remembering in the case of an observation?
Forget_Value = 0.2 # What is probability of forgetting in the case of an observation?

# All features, starting value of 5, goes from 0 to 10, where 0 is most forgotten, 10 is most remembered
Recurrance_All_Features = {Menopge40: Memory_Init_Val, NotMenopge40: Memory_Init_Val, Menoplt40: Memory_Init_Val, NotMenoplt40: Memory_Init_Val, Menopremeno: Memory_Init_Val, NotMenopremeno: Memory_Init_Val, Inv02: Memory_Init_Val, NotInv02: Memory_Init_Val, Inv35: Memory_Init_Val, NotInv35: Memory_Init_Val, Inv68: Memory_Init_Val, NotInv68: Memory_Init_Val, DegMalg3: Memory_Init_Val, NotDegMalg3: Memory_Init_Val, DegMalg2: Memory_Init_Val, NotDegMalg2: Memory_Init_Val, DegMalg1: Memory_Init_Val, NotDegMalg1: Memory_Init_Val}

# How to extract rules, before evaluating with them:
# For each rule, do this:
# 1. Initialize memory
# 2. Randomly select data set (or alternate)
# 3. Repeat 4-6
# 4. Randomly select feedback type
# 5. Randomly select patient from correct data set
# 6. Update memory based on selected patient, using selected feedback type
# 7. Extract memory with the memory.get_condition function



for mem in range(Rule_Count): # repeat the rule extraction a number of times
    New_Rule = Memory(Remember_Value, Forget_Value, Recurrance_All_Features)  # initialize memory with forget-value 0.8, remember-value 0.2, and the above memory.
    Data_Set_ID = random.choice([0,1]) # Randomly select recurrence or non-recurrence to generate rules for; 0 is yes, 1 is no.
    for it in range(Memory_Iterations): # iterate the memory so it can learn a rule
        Feedback_Type = random.choice([1,2]) # select feedback type
        Patient = All_Patients[Data_Set_ID][math.floor(random.random()*len(All_Patients[Data_Set_ID]))] # Get randomly selected patient from chosen dataset
        if Feedback_Type == 1: # feedback type i
            type_i_feedback(Patient, New_Rule)
        else: # not feedback type i, so it must be type ii.
            type_ii_feedback(Patient, New_Rule)
    if len(New_Rule.get_condition())!=0: # makes sure a rule was learned
        Rules[Data_Set_ID].append(New_Rule.get_condition()) # add rule to set of rules, based on what it predicts.

Recurrence = 'Recurrence'
Non_recurrence = 'Non-recurrence'

Truth = [Recurrence, Non_recurrence,Recurrence, Non_recurrence,Recurrence, Non_recurrence] # Truth value of each patient, the actual value that patient has
Corrects = 0 # counts number of correct predictions
for p in range (len(patients)): # Check all patients
    verdict = classify(patients[p], Rules[0],Rules[1]) # Classify each patient with the newly developed rules
    correctness = verdict == Truth[p] # if the verdict matches the truth, this is True.
    print("Verdict: "+verdict+", Truth: "+Truth[p]+". "+str(verdict==Truth[p])) # prints out verdict, truth, and whether the guess was right or not
    if correctness: # increments number of correct guesses if it was right
        Corrects +=1
print("Accuracy: "+str(100*(Corrects/6))+"%") # prints out accuracy of guesses

# un-comment to show average performance
#exit()


# Average accuracy over N runs:

runs = 20
print("Average accuracy in 20 runs: ")
Current_Accuracy = 0
for run in range(runs):
    print("Run: "+str(run))
    for mem in range(Rule_Count):  # repeat the rule extraction a number of times
        New_Rule = Memory(Remember_Value, Forget_Value,
                          Recurrance_All_Features)  # initialize memory with forget-value 0.8, remember-value 0.2, and the above memory.
        Data_Set_ID = random.choice(
            [0, 1])  # Randomly select recurrence or non-recurrence to generate rules for; 0 is yes, 1 is no.
        for it in range(Memory_Iterations):  # iterate the memory so it can learn a rule
            Feedback_Type = random.choice([1, 2])  # select feedback type
            Patient = All_Patients[Data_Set_ID][math.floor(
                random.random() * len(All_Patients[Data_Set_ID]))]  # Get randomly selected patient from chosen dataset
            if Feedback_Type == 1:  # feedback type i
                type_i_feedback(Patient, New_Rule)
            else:  # not feedback type i, so it must be type ii.
                type_ii_feedback(Patient, New_Rule)
        if len(New_Rule.get_condition()) != 0:  # makes sure a rule was learned
            Rules[Data_Set_ID].append(New_Rule.get_condition())  # add rule to set of rules, based on what it predicts.

    Truth = [Recurrence, Non_recurrence, Recurrence, Non_recurrence, Recurrence,
             Non_recurrence]  # Truth value of each patient, the actual value that patient has
    Corrects = 0  # counts number of correct predictions
    for p in range(len(patients)):  # Check all patients
        verdict = classify(patients[p], Rules[0], Rules[1])  # Classify each patient with the newly developed rules
        correctness = verdict == Truth[p]  # if the verdict matches the truth, this is True.
        if correctness:  # increments number of correct guesses if it was right
            Corrects += 1
    Current_Accuracy += (Corrects / 6)/runs
print("Average accuracy in "+str(runs)+" runs: "+str(Current_Accuracy))