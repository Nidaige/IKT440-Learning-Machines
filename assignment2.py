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
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition

    def memorize(self, literal):
        if random.random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1

    def forget(self, literal):
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1


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
