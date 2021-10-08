### Connect 4 using tsetlin machines

def DataLoader():
    data = open("Data/connect-4.data")
    data_set = []
    eof = False
    while not eof:
        line_data = data.readline()
        if len(line_data) == 0:
            eof = True
        else:
            line_data = line_data.strip()
            line_data = line_data.split(',')
            new_line_data = []
            # each point in data is [X, O, Blank]
            # for winners: [X wins, O wins, Draw]
            for e in line_data:
                if e == 'b':
                    new_line_data.append([False, False, True])
                elif e == 'x':
                    new_line_data.append([True, False, False])
                elif e == 'o':
                    new_line_data.append([False, True, False])
                elif e == "win":
                    new_line_data.append([True, False, False])
                elif e == "draw":
                    new_line_data.append([False, False, True])
                else:
                    new_line_data.append([False, True, False])
            data_set.append(new_line_data)
    print(data_set[0])

    positions = ["a1", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b4", "b5", "b6", "c1", "c2", "c3", "c4", "c5",
                 "c6", "d1", "d2", "d3", "d4", "d5", "d6", "e1", "e2", "e3", "e4", "e5", "e6", "f1", "f2", "f3", "f4",
                 "f5", "f6", "g1", "g2", "g3", "g4", "g5", "g6"]
    full_data_type_i = []  # generate type-i feedback compatible data (only positive statements, no NOT literals)
    for line in data_set:  # for each line in the data set
        line_dict = {}  # new dictionary to hold all literals for that line
        for pos in range(len(positions)):  # for each position on a board
            line_dict[positions[pos] + "x"] = line[pos][0]  # update with the presence of X
            line_dict[positions[pos] + "o"] = line[pos][1]  # update with the presence of O
            line_dict[positions[pos] + "blank"] = line[pos][2]  # update if blank
        last_index = len(positions) - 1
        line_dict["Win"] = line[last_index][0]  # update if X wins
        line_dict["Loss"] = line[last_index][1]  # update if O wins
        line_dict["Draw"] = line[last_index][2]  # update if Draw
        full_data_type_i.append(line_dict)
    # print(full_data_type_i[0])

    full_data_type_ii = []  # generate type-ii feedback compatible data (with NOT-statements)
    for line in data_set:
        line_dict = {}
        for pos in range(len(positions)):
            line_dict[positions[pos] + "x"] = line[pos][0]
            line_dict[positions[pos] + "o"] = line[pos][1]
            line_dict[positions[pos] + "blank"] = line[pos][2]
            line_dict["NOT " + positions[pos] + "x"] = not line[pos][0]
            line_dict["NOT " + positions[pos] + "o"] = not line[pos][1]
            line_dict["NOT " + positions[pos] + "blank"] = not line[pos][2]
        last_index = len(positions) - 1
        line_dict["Win"] = line[last_index][0]  # update if X wins
        line_dict["Loss"] = line[last_index][1]  # update if O wins
        line_dict["Draw"] = line[last_index][2]  # update if Draw
        line_dict["NOT Win"] = not line[last_index][0]  # update if X wins
        line_dict["NOT Loss"] = not line[last_index][1]  # update if O wins
        line_dict["NOT Draw"] = not line[last_index][2]  # update if Draw
        full_data_type_ii.append(line_dict)
    full_data_type_i_classes = [[], [], []]
    full_data_type_ii_classes = [[], [], []]
    for a in full_data_type_i:
        if a["Win"] == True:
            full_data_type_i_classes[0].append(a)
        elif a["Loss"] == True:
            full_data_type_i_classes[1].append(a)
        else:
            full_data_type_i_classes[2].append(a)
    for a in full_data_type_ii:
        if a["Win"] == True:
            full_data_type_ii_classes[0].append(a)
        elif a["Loss"] == True:
            full_data_type_ii_classes[1].append(a)
        else:
            full_data_type_ii_classes[2].append(a)

    return [full_data_type_i_classes, full_data_type_ii_classes]


def DataLoaderNumeric():
    data = open("Data/connect-4.txt")
    data_set = []
    eof = False
    while not eof:
        line_data = data.readline()
        if len(line_data) == 0:
            eof = True
        else:
            line_data = line_data.strip()
            line_data = line_data.split(',')
            new_line_data = []
            # each point in data is [X, O, Blank]
            # for winners: [X wins, O wins, Draw]
            for e in line_data:
                if e == 'b':
                    new_line_data.append(-1)
                elif e == 'x':
                    new_line_data.append(1)
                elif e == 'o':
                    new_line_data.append(0)
                elif e == "win":
                    new_line_data.append(1)
                elif e == "draw":
                    new_line_data.append(-1)
                else:
                    new_line_data.append(0)
            data_set.append(new_line_data)
    data.close()
    return (data_set)


### Tsetlin machine to use the data set
from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
import random

print("Imports done")
# DataLoaderNumeric()
# train_data = np.loadtxt("Data/connect-4.txt")
data = DataLoaderNumeric()
print("Data loaded")
train_data = np.array(data)
X_train = train_data[:, 0:-1]
Y_train = train_data[:, -1]
print("Training data defined")
test_data_pre = []
for a in range(50):
    test_data_pre.append(random.choice(data))
test_data = np.array(test_data_pre)
X_test = test_data[:, 0:-1]
Y_test = test_data[:, -1]
print("Test data defined")
tm = MultiClassTsetlinMachine(20, 15, 10.0)  # , boost_true_positive_feedback=0)
print("Multiclass machine defined")
tm.fit(X_train, Y_train, epochs=1)
print("Machine fitted")
print("Accuracy:" + str(100 * (tm.predict(X_test) == Y_test).mean()) + "%")
print("Done :)")
exit(0)