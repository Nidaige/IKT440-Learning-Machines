### Connect 4 using tsetlin machines

### Function for loading data. Converts each line of b/x/o/win/loss/draw into -1 for blank/draw, 1 for x/win and 0 for o/loss
def DataLoaderNumeric():
    data = open("Data/connect-4.txt")  # open file
    data_set = []  # array to hold data
    eof = False  # bool indicating end of file
    while not eof:  # iterate until eof
        line_data = data.readline()  # read line
        if len(line_data) == 0: # if line is empty
            eof = True  # indicate eof
        else:
            line_data = line_data.strip() # remove newline characters from each line
            line_data = line_data.split(',') # split on every comma
            new_line_data = [] # array to hold numeric values
            for e in line_data: # for each element (letter) in a line:
                if e == 'b': # if b (blank), set 2
                    new_line_data.append(2)
                elif e == 'x': # if x (x) set 1
                    new_line_data.append(1)
                elif e == 'o': # if o (o) set 0
                    new_line_data.append(0)
                elif e == "win": # if x wins, set 1
                    new_line_data.append(1)
                elif e == "draw": # if draw, set 2
                    new_line_data.append(2)
                else: # if X loses (o wins), set 0
                    new_line_data.append(0)
            data_set.append(new_line_data) # add numeric version of current line to array of lines
    data.close() # close file after all lines are read
    print(len(data_set)) # print number of lines
    return (data_set) # return the list of lines


### Tsetlin machine to use the data set
# imports
from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
import random

data = DataLoaderNumeric() # load data
train_data = np.array(data).astype(np.int) # convert data from list to nparray of ints
X_train = train_data[:, 0:-1] # define what values are data
Y_train = train_data[:, -1] # define what values are the predictor (win/loss/draw)
test_data_pre = [] # array to hold testing data before conversion to nparray
for a in range(50): # extract 50 randomly selected samples from data set
    test_data_pre.append(random.choice(data))
test_data = np.array(test_data_pre).astype(np.int) # convert selected test data to nparray of ints
X_test = test_data[:, 0:-1] # define data of test data
Y_test = test_data[:, -1] # define predictor (win/loss/draw) of test data
tm = MultiClassTsetlinMachine(500, 88, 27.0)  # initialize tsetlin machine with # of clauses, T and s in order
tm.fit(X_train, Y_train, epochs=50) # train the tsetlin machine on the training data, running for 50 epochs
print("Accuracy:" + str(100 * (tm.predict(X_test) == Y_test).mean()) + "%") # print the average result against test result
exit(0) # exit, optional