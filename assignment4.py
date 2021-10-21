### Clasify text samples
import math

import numpy
import seaborn as seaborn
import sns as sns
from matplotlib import pyplot as plt
from sklearn import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import seaborn as sns
import string

def Remove_Punctuation(s):
    b="" # string builder
    special_chars = "!\"\n#$()*,.@[\]^_`{|}~\t&+/:;<=>?" # string literal of any replaceable punctuation
    for letter in s: # for each letter in the string
        if letter not in special_chars: # if the letter is not replacable punctuation
            b+=letter # add the letter to the string builder
        else: b+=" " # if the letter is replaceable punctuation, replace with a spcae
    return b # return the built string

def Get_Stop_Words():
    file = open("Data/stop_words.txt") # open stop-words text file
    data = file.read() # read the stop words
    return data.split("\n") # return list of words separated on the newline character

def Normallize(s):
    return Remove_Punctuation(s.lower()).split(" ")

def Get_Frequencies_By_Category_Dict(dataset):
    map = {"All_Words":{"Total":0, "Debates":0}} # dict to hold frequencies for each word per category
    stop_words = Get_Stop_Words() # get stop words
    for label in dataset["target"]:
        map[ dataset["target_names"][label] ] = {"Total":0, "Debates":0} # Dict to hold dict for each category, with each word
    #   ----------- populate map with categories respective word frequencies
    for debate in range(len(dataset["data"])): # loop through each debate
        map["All_Words"]["Debates"]+=1 # increment total number of debates
        debate_label = dataset["target_names"] [dataset["target"] [debate]] # get debate's label
        map[debate_label]["Debates"]+=1 #increment number of debates in <debate_label> category
        debate_data = Normallize(dataset["data"] [debate]) # get debate's data [word1, word2, word3, etc]
        for word in debate_data:
            if word not in stop_words:
                if word not in map[debate_label].keys(): # if word is not in dict, initialize entries
                    map[debate_label][word] = 1
                    map[debate_label]["Total"] += 1
                    map["All_Words"][word] = 1
                    map["All_Words"]["Total"] += 1
                else: # word is already in dict, increment entries instead
                    map[debate_label][word] += 1
                    map[debate_label]["Total"] += 1
                    map["All_Words"][word] += 1
                    map["All_Words"]["Total"] += 1
    # convert flat occurrence to relative occurrence
    for label in map.keys(): # for all categories
        total = map[label]["Total"] # get the total number of words of that category
        for word in map[label].keys(): # for each word in a category
            if word not in ["Debates", "Total"]: # if word is not "Debates" or "Total"
                map[label][word] = map[label][word] / total # divide the occurrence by the total number for that category
                map["All_Words"][word] = map["All_Words"][word] / map["All_Words"]["Total"] #divide the occurrence of each word in the whole dataset by the total number of words in the dataset
    #   ------------ return populated map
    return map # map = p(o1, o2, o3, ... | h1, h2, h3, h4, ...)

def Predict_Category_From_Text(text, training_data):
    prediction = {}  # dict to hold prediction values
    nTD = training_data["All_Words"]["Debates"]  # number of total debates
    for category in training_data.keys(): #for all categories in the training data set
        if category!="All_Words": #if the category is not "All_Words"
            prediction[category] = 1.0  # set a starting prediction of 0 because 10^0 = 1
    # Naive Baies assumption NB: P(o1, o2, o3, … | hj) = prod( P(oi|hj)
    # P(h|o) = P(o|h)*P(h)
    # p(category|text) = NB *p(category)
    for word in Normallize(text): #for each word in text:
        if len(word)>1:
            for category in training_data.keys(): # for every hypothesis/category:
                if category!="All_Words": # if the category is not "All_Words":
                    if word in training_data[category].keys(): # if word occurrs for this category
                        prediction[category] *= training_data[category][word] # update the product with the probability of observation "word" given hypothesis "category", or p(word1, word2, word3, ...|category)
    sum = 0
    for a in prediction.keys(): # for each category
        nCD = training_data[a]["Debates"] # number of category debates
        ph = nCD/nTD
        poh = prediction[a] # p(o|h)
        sum+=poh
        prediction[a] = (poh*ph)#/po # prediction = p(h|o)*p(h)/p(o)
    print(sum)
    exit()
    return prediction
# Main
print("Get training data")
# get complete map of all categories, with the relative frequency of all occurring words within each
train_data = Get_Frequencies_By_Category_Dict(datasets.fetch_20newsgroups(data_home=None, subset='train', categories=None, shuffle=True, random_state=42, remove=('headers', 'footers', 'quotes'), download_if_missing=True, return_X_y=False))
# get test data
print("Get test data")
test_data = datasets.fetch_20newsgroups(data_home=None, subset='test', categories=None, shuffle=True, random_state=42, remove=('headers', 'footers', 'quotes'), download_if_missing=True, return_X_y=False)
print("start processing")
all_predictions = []  # all predictions
all_truths = []  # all truths
i = 0  # counter for # of predictions
#for debate_n in range(len(test_data["data"])):
for debate_n in range(500):
    debate = test_data["data"][debate_n]
    truth = test_data["target_names"][test_data["target"][debate_n]]
    all_predictions.append(Predict_Category_From_Text(debate, train_data))
    all_truths.append(truth)
    if i%100==0:
        print("predicting "+str(i))
    i+=1


print("done predicting, now formatting")
corrects = 0
totals = 0
for prediction_dict_num in range(len(all_predictions)):
    totals+=1
    currentMax=test_data["target_names"][0]
    current_prediction = all_predictions[prediction_dict_num] # current prediction dictionary
    for a in current_prediction.keys():
        if a!="All_Words":
            if current_prediction[a]>current_prediction[currentMax]:
                currentMax=a
    if currentMax == all_truths[prediction_dict_num]:
        corrects+=1




print("Accuracy: "+str(100*corrects/totals)+"%")


exit()
