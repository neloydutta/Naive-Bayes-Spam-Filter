import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

training_data = {}
word_table = {}
#class_frequency = {}


def train(body, label):
    with open('trainingdata.json') as td:
        traindata = json.load(td)
    training_data = traindata
    training_data[body] = label
    print training_data
    with open('trainingdata.json', 'w+') as td:
        json.dump(training_data, td)


def generate_frequency_table():
    with open('trainingdata.json') as td:
        training_data = json.load(td)
    with open('frequency.json') as cf:
        class_frequency = json.load(cf)

    for i in training_data.keys():
        words = word_tokenize(i, language='english')
        for word in words:
            if word.lower() not in stopwords.words():
                if word not in word_table.keys():
                    word_table[word] = []
                word_table[word].append(training_data[i])

    for i in word_table.keys():
        if i not in class_frequency.keys():
            class_frequency[i] = [0, 0]
        for cat in word_table[i]:
            if cat == 'spam':
                class_frequency[i][0] += 1
            else:
                class_frequency[i][1] += 1
    with open('wordtable.json', 'w+') as wt:
        json.dump(word_table, wt)
    with open('frequency.json', 'w+') as cf:
        json.dump(class_frequency, cf)


def class_probability(classidx):
    with open('frequency.json') as cf:
        class_frequency = json.load(cf)
    p = 0.0
    t = 0.0
    for i in class_frequency.keys():
        p += int(class_frequency[i][classidx])
        t += int(class_frequency[i][0] + class_frequency[i][1])
    return p / t


def likelihood_spam_word(word, classidx):
    with open('frequency.json') as cf:
        class_frequency = json.load(cf)
    if word not in class_frequency.keys():
        return 0.0
    p = class_frequency[word][classidx]
    t = 0.0
    for i in class_frequency.keys():
        t += class_frequency[i][classidx]
    return p/t


def predictor_prior_probabilityf(word):
    with open('frequency.json') as cf:
        class_frequency = json.load(cf)
    p = 0.0
    t = 0.0
    if word not in class_frequency.keys():
        return 0.0
    for i in class_frequency.keys():
        t += class_frequency[i][0] + class_frequency[i][1]
        if i == word:
            p += class_frequency[word][0] + class_frequency[word][1]
    return p/t


def classify(text):
    words = word_tokenize(text, language='english')
    posterior_probability_spam = 0.0  # P(spam/x)
    posterior_probability_not_spam = 0.0  # P(not_spam/x)
    likelihood_spam = 0.0  # P(x/spam)
    likelihood_not_spam = 0.0  # P(x/not_spam)
    prior_probability_spam = 0.0  # P(spam)
    prior_probability_not_spam = 0.0  # P(not_spam)
    predictor_prior_probability = 0.0  # P(x)

    prior_probability_spam = class_probability(0)
    prior_probability_not_spam = class_probability(1)

    for i in words:
        likelihood_spam += likelihood_spam_word(i.lower(), 0)
        likelihood_not_spam += likelihood_spam_word(i.lower(), 1)
        predictor_prior_probability += predictor_prior_probabilityf(i.lower())

    if predictor_prior_probability == 0.0:
        predictor_prior_probability = -1.0

    posterior_probability_spam = (likelihood_spam * prior_probability_spam) / predictor_prior_probability
    posterior_probability_not_spam = (likelihood_not_spam * prior_probability_not_spam) / predictor_prior_probability

    return posterior_probability_spam, posterior_probability_not_spam


if __name__ == "__main__":
    generate_frequency_table()
    spam, not_spam = classify("is this a spam!")
    print "Spam: " + str(spam)
    print "Not_Spam: " + str(not_spam)
