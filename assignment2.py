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


# Type 1 and 2 feedback part --------------------------------------------------------------------------

MemorySize = 50000 # The total range of how forgotten/remembered a given feature is
MemoryInitVal = math.floor(MemorySize*0.5) # The initial value of every feature in memory. Half of the memory size
MemoryIterations = 5 # How many remember/forget iterations will be done with the memory before extracting a rule?

class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value

    def get_memory(self):
        return self.memory

    def get_literals(self):
        return list(self.memory.keys())

    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= MemoryInitVal:
                condition.append(literal)
        return condition

    def memorize(self, literal):
        if random.random() <= self.memorize_value and self.memory[literal] < MemorySize:
            self.memory[literal] += 1

    def forget(self, literal):
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < MemorySize:
            self.memory[literal] += 1

def type_i_feedback(observation, memory): # function that gives type i feedback on a memory:
    remaining_literals = memory.get_literals() # gets all the literals (features)
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation: # iterate through features in observation
            if observation[feature] == True: # if the feature exists
                memory.memorize(feature) # memorize the feature
                remaining_literals.remove(feature)
            elif observation[feature] == False: # if the feature does not exist in the observation
                memory.memorize('NOT ' + feature) # memorize the negative (NOT) feature instead
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals: # for any non-memorized feature,
        memory.forget(literal) # forget about it


def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation: # for any feature in the observation,
            if observation[feature] == False: # if the feature exists,
                memory.memorize_always(feature) # memorize the feature
            elif observation[feature] == True: # if the feature does not exist:
                memory.memorize_always('NOT ' + feature) # memorize the negative (NOT) feature

def classify(observation, recurrence_rules, non_recurrence_rules):
    vote_sum = 0
    for rule in recurrence_rules:
        if evaluate_condition(observation, rule.get_condition()) == True:
            vote_sum += 1
    for rule in non_recurrence_rules:
        if evaluate_condition(observation, rule.get_condition()) == True:
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-recurrence"

Recurring_Patients = [
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:True,  Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:False, Inv35:False, Inv68:True,   DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
]

Non_Recurring_Patients = [
{Menopge40:False, Menoplt40:True, Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:True,  DegMalg2:False, DegMalg1:False},
{Menopge40:True,  Menoplt40:False,Menopremeno:False, Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:True,  DegMalg1:False},
{Menopge40:False, Menoplt40:False,Menopremeno:True,  Inv02:True,  Inv35:False, Inv68:False,  DegMalg3:False, DegMalg2:False, DegMalg1:True},
]

# All features, starting value of 5, goes from 0 to 10, where 0 is most forgotten, 10 is most remembered
RecurranceAllFeatures = {Menopge40: MemoryInitVal,NotMenopge40: MemoryInitVal, Menoplt40: MemoryInitVal, NotMenoplt40: MemoryInitVal, Menopremeno: MemoryInitVal, NotMenopremeno: MemoryInitVal, Inv02: MemoryInitVal, NotInv02: MemoryInitVal, Inv35: MemoryInitVal, NotInv35: MemoryInitVal, Inv68: MemoryInitVal, NotInv68: MemoryInitVal, DegMalg3: MemoryInitVal, NotDegMalg3: MemoryInitVal, DegMalg2: MemoryInitVal, NotDegMalg2: MemoryInitVal, DegMalg1: MemoryInitVal, NotDegMalg1: MemoryInitVal}

Recurring_Rule= Memory(0.8,0.2,RecurranceAllFeatures) # initialize memory with forget-value 0.8, remember-value 0.2, and the above memory.
Non_Recurring_Rule= Memory(0.8,0.2,RecurranceAllFeatures) # initialize memory with forget-value 0.8, remember-value 0.2, and the above memory.
for a in range(MemoryIterations): # do 100 runs
    # Recurring memory learns
    id = random.choice([0,1,2]) # randomly select a patient id
    type = random.choice([0,1]) # randomly choose feedback type
    if (type==1):
        type_i_feedback(Recurring_Patients[id], Recurring_Rule) # feedback type i
    else:
        type_ii_feedback(Recurring_Patients[id], Recurring_Rule) # feedback type ii
    # Non-recurring memory learns
    id = random.choice([0,1,2]) # randomly select a patient id
    type = random.choice([0,1]) # randomly choose feedback type
    if (type==1):
        type_i_feedback(Non_Recurring_Patients[id], Non_Recurring_Rule) # feedback type i
    else:
        type_ii_feedback(Non_Recurring_Patients[id], Non_Recurring_Rule) # feedback type ii

for patient in patients:
    print(classify(patient, [Recurring_Rule], [Non_Recurring_Rule]))