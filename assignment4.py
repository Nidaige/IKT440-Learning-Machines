# Group information
# Group name: THE GROUP
# Group members:
# - Tone Liestøl Olsen
# - Alexander Nordnes Strand
# - Henning Blomfeldt Thorsen

#  Clasify text samples
from math import log2 as log
from sklearn import *


def remove_punctuation(s):  # removes punctuation
    b = ""  # string builder
    special_chars = "!\"\n#$()*,.@[\\]^_`{|}~\t&+/:;<=>?"  # string literal of any replaceable punctuation
    for letter in s:  # for each letter in the string
        if letter not in special_chars:  # if the letter is not replacable punctuation
            b += letter  # add the letter to the string builder
        else:
            b += " "  # if the letter is replaceable punctuation, replace with a spcae
    return b  # return the built string


def get_stop_words():  # gets words to exclude from file
    file = open("Data/stop_words.txt")  # open stop-words text file
    data = file.read()  # read the stop words
    return data.split("\n")  # return list of words separated on the newline character


def normalize(s):  # Takes string, returns array of words
    return remove_punctuation(s.lower()).split(" ")


def get_frequencies_by_category_dict(dataset):  # Gets dictionary with categories, each with frequency per word
    data_map = {"All_Words": {"Total": 0, "Debates": 0}}  # dict to hold frequencies for each word per category
    stop_words = get_stop_words()  # get stop words
    for label in dataset["target"]:
        data_map[dataset["target_names"][label]] = {"Total": 0,
                                                    "Debates": 0}  # Dict to hold dict for each category + words
    #   ----------- populate map with categories respective word frequencies
    for post in range(len(dataset["data"])):  # loop through each debate
        data_map["All_Words"]["Debates"] += 1  # increment total number of debates
        debate_label = dataset["target_names"][dataset["target"][post]]  # get debate's label
        data_map[debate_label]["Debates"] += 1  # increment number of debates in <debate_label> category
        debate_data = normalize(dataset["data"][post])  # get debate's data [word1, word2, word3, etc]
        for word in debate_data:
            if word not in stop_words:
                if word not in data_map[debate_label].keys():  # if word is not in dict, initialize entries
                    for category in dataset["target_names"]:
                        data_map[category][word] = 1
                        data_map[category]["Total"] += 1
                    data_map["All_Words"][word] = 1
                    data_map["All_Words"]["Total"] += 1
                else:  # word is already in dict, increment entries instead
                    data_map[debate_label][word] += 1
                    data_map[debate_label]["Total"] += 1
                    data_map["All_Words"][word] += 1
                    data_map["All_Words"]["Total"] += 1

    # convert flat occurrence to relative occurrence
    for label in data_map.keys():  # for all categories
        total = data_map[label]["Total"]  # get the total number of words of that category
        for word in data_map[label].keys():  # for each word in a category
            data_map[label][word] = data_map[label][
                                        word] / total  # divide the occurrence by the total number for that category
    #   ------------ return populated map
    return data_map  # map = p(o1, o2, o3, ... | h1, h2, h3, h4, ...)


def predict_category_from_text(text, training_data):
    prediction = {}  # dict to hold prediction values
    NormalizedText = normalize(text)
    p_o = 0.0
    for category in training_data.keys():  # initialize prediction dict with all categories:
        if category != "All_Words":
            prediction[category] = 0  # log inv(0) = 1
    for word in NormalizedText:  # for each word
        if word in training_data["All_Words"].keys():  # makes sure the word is in the dataset before trying to evaluate
            p_o += log(training_data["All_Words"][word])  # product of all p(word), assumes order is irrelevant
            for category in training_data.keys():  # for each category
                if category != "All_Words":
                    prediction[category] += log(training_data[category][word])
    # Now to calculate p(h|o) = p(o|h) * P(h) / p(o)
    for h in training_data.keys():  # for every category h:
        if h != "All_Words":
            p_o_h = prediction[h]
            p_h = (training_data[h]["Debates"]) / (training_data["All_Words"]["Debates"])
            p_h_o = p_o_h + p_h - p_o  # inverse log after using them to divide/multiply
            prediction[h] = p_h_o
    return prediction


# Main
print("Getting training data")
# get complete map of all categories, with the relative frequency of all occurring words within each
train_data = get_frequencies_by_category_dict(
    datasets.fetch_20newsgroups(data_home=None, subset='train', categories=None, shuffle=True, random_state=42,
                                remove=('headers', 'footers', 'quotes'), download_if_missing=True, return_X_y=False))
# get test data
print("Getting test data")
test_data = datasets.fetch_20newsgroups(data_home=None, subset='test', categories=None, shuffle=True, random_state=42,
                                        remove=('headers', 'footers', 'quotes'), download_if_missing=True,
                                        return_X_y=False)
print("Starting predictions")
all_predictions = []  # all predictions
all_truths = []  # all truths
i = 0  # counter for # of predictions

# loop through test data, get predictions
for debate_n in range(len(test_data["data"])):  # for each post in test data
    debate = test_data["data"][debate_n]  # current debate
    truth = test_data["target_names"][test_data["target"][debate_n]]  # get true category
    all_predictions.append(predict_category_from_text(debate, train_data))  # get predictions dict for post
    all_truths.append(truth)  # add true category to array
    if i % 100 == 0:
        print("predicting sample " + str(i))  # print status every 100 samples
    i += 1

print("Predictions done, evaluating accuracy")
corrects = 0
totals = 0
for prediction_dict_num in range(len(all_predictions)):  # for each prediction,
    totals += 1  # increment total number of predictions made
    currentMax = test_data["target_names"][0]  # holds currently best category for this prediction
    current_prediction = all_predictions[prediction_dict_num]  # current prediction dictionary
    for a in current_prediction.keys():  # for each category,
        if a != "All_Words":  # if the category isn't "All_Words",
            if current_prediction[a] > current_prediction[currentMax]:  # and the probability of the category is best,
                currentMax = a  # update the best prediction
    if currentMax == all_truths[prediction_dict_num]:  # if the best prediction is correct,
        corrects += 1  # increment number of correct guesses
print("Accuracy: " + str(100 * corrects / totals) + "%")  # prints # of correct guesses / # of total guesses
exit()
