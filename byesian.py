#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from math import sqrt
from math import pi
from math import exp
import warnings
warnings.filterwarnings(action='ignore')
       
"""
Crea un dizionario in cui i dati sono separati per decennio, leggendo dai file .csv
"""
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

"""
Calcola la media tra i numeri all'imnterno di una lista
"""
def mean(numbers):
	return sum(numbers)/float(len(numbers))

"""
Calcola la deviazione standard tra i numeri all'imnterno di una lista
"""
def stdev(numbers):
	avg = mean(numbers)
	variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
	return sqrt(variance)

"""
Calcola la media, la deviazione standard per ogni colonna del dataset, contandone i valori
"""
def summarize_dataset(dataset):
    summaries  = []
    for column in dataset.columns[3:]:
        summaries.append([(mean(dataset[column]), stdev(dataset[column]), len(dataset[column]))])
    del(summaries[-1])
    return summaries

"""
Split del dataset per classe per calcolare le statistiche per ogni riga
"""
def summarize_by_class():
    separated = dict()
    separated = separate_by_class()
    summaries = dict()
    for key in separated:
        summaries[key] = summarize_dataset(separated[key])
    return summaries

"""
Calcola la probabilità di distribuzione Gaussiana per x
"""
def calculate_probability(x, mean, stdev):
	exponent = exp(-((x-mean)**2 / (2 * stdev**2 )))
	return (1 / (sqrt(2 * pi) * stdev)) * exponent
 
"""
Calcola la probabilità di predire ogni classe per una data riga
"""
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

"""
Restituisce il decennio predetto grazie al metodo di classificazione bayesiano, 
utilizzando i metodi precedenti 
"""
def classificatore_bayesiano(X):
    summaries = summarize_by_class()
    probabilities = calculate_class_probabilities(summaries, X)
    annoProb=0
    
    #Individua l'anno in base alla probabilità maggiore
    for key in probabilities:
        if(probabilities[key]>annoProb):
            annoProb=probabilities[key]
            anno=key
    return anno