import random
patients = [
{'Menop.-ge40':True, 'NOT Menop.-ge40':False, 'Menop.-lt40':False,'NOT Menop.-lt40':True,'Menop.-premeno':False, 'NOT Menop.-premeno':True, 'Inv-nodes-0-2':False, 'NOT Inv-nodes-0-2':True, 'Inv-nodes-3-5':True, 'NOT Inv-nodes-3-5':False, 'Inv-nodes-6-8':False, 'NOT Inv-nodes-6-8':True, 'Deg-malg-3':True, 'NOT Deg-malg-3':False,'Deg-malg-2':False, 'NOT Deg-malg-2':True,'Deg-malg-1':False, 'NOT Deg-malg-1':True,},
{'Menop.-ge40':False, 'NOT Menop.-ge40':True, 'Menop.-lt40':True,'NOT Menop.-lt40':False,'Menop.-premeno':False, 'NOT Menop.-premeno':True, 'Inv-nodes-0-2':True, 'NOT Inv-nodes-0-2':False, 'Inv-nodes-3-5':False, 'NOT Inv-nodes-3-5':True, 'Inv-nodes-6-8':False, 'NOT Inv-nodes-6-8':True, 'Deg-malg-3':True, 'NOT Deg-malg-3':False,'Deg-malg-2':False, 'NOT Deg-malg-2':True,'Deg-malg-1':False, 'NOT Deg-malg-1':True,},
{'Menop.-ge40':True, 'NOT Menop.-ge40':False, 'Menop.-lt40':False,'NOT Menop.-lt40':True,'Menop.-premeno':False, 'NOT Menop.-premeno':True, 'Inv-nodes-0-2':False, 'NOT Inv-nodes-0-2':True, 'Inv-nodes-3-5':False, 'NOT Inv-nodes-3-5':True, 'Inv-nodes-6-8':True, 'NOT Inv-nodes-6-8':False, 'Deg-malg-3':True, 'NOT Deg-malg-3':False,'Deg-malg-2':False, 'NOT Deg-malg-2':True,'Deg-malg-1':False, 'NOT Deg-malg-1':True,},
{'Menop.-ge40':True, 'NOT Menop.-ge40':False, 'Menop.-lt40':False,'NOT Menop.-lt40':True,'Menop.-premeno':False, 'NOT Menop.-premeno':True, 'Inv-nodes-0-2':True, 'NOT Inv-nodes-0-2':False, 'Inv-nodes-3-5':False, 'NOT Inv-nodes-3-5':True, 'Inv-nodes-6-8':False, 'NOT Inv-nodes-6-8':True, 'Deg-malg-3':False, 'NOT Deg-malg-3':True,'Deg-malg-2':True, 'NOT Deg-malg-2':False,'Deg-malg-1':False, 'NOT Deg-malg-1':True,},
{'Menop.-ge40':False, 'NOT Menop.-ge40':True, 'Menop.-lt40':False,'NOT Menop.-lt40':True,'Menop.-premeno':True, 'NOT Menop.-premeno':False, 'Inv-nodes-0-2':True, 'NOT Inv-nodes-0-2':False, 'Inv-nodes-3-5':False, 'NOT Inv-nodes-3-5':True, 'Inv-nodes-6-8':False, 'NOT Inv-nodes-6-8':True, 'Deg-malg-3':True, 'NOT Deg-malg-3':False,'Deg-malg-2':False, 'NOT Deg-malg-2':True,'Deg-malg-1':False, 'NOT Deg-malg-1':True,},
{'Menop.-ge40':False, 'NOT Menop.-ge40':True, 'Menop.-lt40':False,'NOT Menop.-lt40':True,'Menop.-premeno':True, 'NOT Menop.-premeno':False, 'Inv-nodes-0-2':True, 'NOT Inv-nodes-0-2':False, 'Inv-nodes-3-5':False, 'NOT Inv-nodes-3-5':True, 'Inv-nodes-6-8':False, 'NOT Inv-nodes-6-8':True, 'Deg-malg-3':False, 'NOT Deg-malg-3':True,'Deg-malg-2':False, 'NOT Deg-malg-2':True,'Deg-malg-1':True, 'NOT Deg-malg-1':False,},
]

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


rule1 = [{'Deg-malg-3','NOT Menop.-lt40'}]
rule2 = [{'Deg-malg-3','NOT Menop.-lt40'}]
rule3 = [{'Inv-nodes-0-2'}]

for patient in patients:
    print(evaluate_condition(patient,rule1))


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