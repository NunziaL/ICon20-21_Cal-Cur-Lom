#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:32:41 2021

@author: antoniocurci
"""

import pandas as pd
from math import sqrt
from math import pi
from math import exp
import warnings
warnings.filterwarnings(action='ignore')
       
def separate_by_class():
    separated = dict()
    i=1960
    for decade in ['6', '7', '8', '9', '0', '1']:
        dfs = [pd.read_csv(f'archive/dataset-of-{decade}0s.csv')]
        data = pd.concat(dfs, axis=0).sample(frac=1.0, random_state=1).reset_index(drop=True)
        data['decade']=i
        separated[i]=data
        i=i+10
    return separated

# Calculate the mean of a list of numbers
def mean(numbers):
	return sum(numbers)/float(len(numbers))

# Calculate the standard deviation of a list of numbers
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)

# Calculate the mean, stdev and count for each column in a dataset
def summarize_dataset(dataset):
    summaries  = []
    for column in dataset.columns[3:]:
        summaries.append([(mean(dataset[column]), stdev(dataset[column]), len(dataset[column]))])
    del(summaries[-1])
    return summaries

# Split dataset by class then calculate statistics for each row
def summarize_by_class():
    separated = dict()
    separated = separate_by_class()
    summaries = dict()
    for key in separated:
        summaries[key] = summarize_dataset(separated[key])
    return summaries

# Calculate the Gaussian probability distribution function for x
def calculate_probability(x, mean, stdev):
	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	return (1 / (sqrt(2 * pi) * stdev)) * exponent
 
# Calculate the probabilities of predicting each class for a given row
def calculate_class_probabilities(summaries, row):
    total_rows = sum([summaries[label][0][0][2] for label in summaries])
    probabilities = dict()
    for class_value in summaries:
        probabilities[class_value] = summaries[class_value][0][0][2]/float(total_rows)
        i=0
        for col in row.columns[0:]:
            mean, stdev, count = summaries[class_value][i][0]
            probabilities[class_value] *= calculate_probability(row[col], mean, stdev)
            i=i+1
    return probabilities 

def classificatore_bayesiano(X):
    summaries = summarize_by_class()
    probabilities = calculate_class_probabilities(summaries, X)
    anno=0
    for key in probabilities:
        if(probabilities[key]>anno):
            anno=probabilities[key]
            X['decade']=key
    return X