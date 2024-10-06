'''
Name: Leslie Atterbury
Date: 10-11-23

Assignment 4
This program uses sklearn's SGD classifier and Naive Bayes classifier.
Dataset is a chemical analysis of wines.
Program also uses shuffle to test the model.
'''

import random

# constants
TRAINING_SET_PERCENT = 0.8
FILE_PATH = "wine\wine.txt"
PARSE_STRING = ","
OUTCOME_1 = 1
OUTCOME_2 = 2

# important constants
DO_SHUFFLE = False
USE_PIPELINE = False

# functions
def getEvaluationMetrics(predicted, actual):
    
    # this should never happen
    if(len(predicted) != len(actual)):
        print("Error in evaluation metrics calculations.")
        exit
    
    totalInstances = len(predicted)

    truePositive = 0
    falsePositive = 0
    trueNegative = 0
    falseNegative = 0

    # calculates loss matrix values
    for i in range(totalInstances):
        if(actual[i] == OUTCOME_1):
            if(predicted[i] == OUTCOME_1):
                truePositive += 1
            elif(predicted[i] == OUTCOME_2):
                falseNegative += 1
        elif(actual[i] == OUTCOME_2):
            if(predicted[i] == OUTCOME_1):
                falsePositive += 1
            elif(predicted[i] == OUTCOME_2):
                trueNegative += 1
    
    # if statements prevent division by 0 in weird cases
    if(totalInstances == 0):
        accuracy = 1.0
    else:
        accuracy = (truePositive + trueNegative)/totalInstances
    
    if((truePositive + falseNegative) == 0):
        sensitivity = 1.0
    else:
        sensitivity = truePositive/(truePositive + falseNegative)
    
    if((trueNegative + falsePositive) == 0):
        specificity = 1.0
    else:
        specificity = trueNegative/(trueNegative + falsePositive)
    
    if((truePositive + falsePositive) == 0):
        precision = 1.0
    else:
        precision = truePositive/(truePositive + falsePositive)
    
    f1Score = 2 * (precision * sensitivity)/(precision + sensitivity)
    
    # print("tp: ", truePositive, " fp: ", falsePositive, " tn: ", trueNegative, " fn: ", falseNegative)

    return [accuracy, sensitivity, specificity, precision, f1Score]

# copy info from file
f = open(FILE_PATH, "r")
filedata = f.readlines()
f.close()

# shuffles the data
if(DO_SHUFFLE):
    random.shuffle(filedata)

# create variables to hold data
trainMaxIndex = int(len(filedata) * TRAINING_SET_PERCENT)
index = 0

trainX = []
trainY = []
testX = []
testY = []

# translates the string list into the variables
for lineStr in filedata:
    
    lineParsed = lineStr.split(PARSE_STRING)
    tempX = []
    tempY = 0

    # translates the string into numbers and number lists
    for i in range(len(lineParsed)):
        if(i == 0):
            tempY = int(lineParsed[0])
        else:
            tempX.append(float(lineParsed[i]))

    # moves the data to the correct list
    if(index < trainMaxIndex):
        trainX.append(tempX)
        trainY.append(tempY)
    else:
        testX.append(tempX)
        testY.append(tempY)
    
    index += 1

# use model thing
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import log_loss

if(USE_PIPELINE):
    logReg = make_pipeline(StandardScaler(), SGDClassifier(loss='log_loss', shuffle=False))
else:
    logReg = SGDClassifier(loss="log_loss",shuffle=False, penalty=None)

logReg.fit(trainX,trainY)

naiveBayes = GaussianNB()
naiveBayes.fit(trainX,trainY)

# get evaluation metrics
logRegTrainingEM = getEvaluationMetrics(logReg.predict(trainX), trainY)
logRegTestingEM = getEvaluationMetrics(logReg.predict(testX), testY)

nbTrainingEM = getEvaluationMetrics(naiveBayes.predict(trainX), trainY)
nbTestingEM = getEvaluationMetrics(naiveBayes.predict(testX), testY)

# get log loss
prob = logReg.predict_proba(trainX)
prob = prob[:, 1]
logRegTrainingLL = log_loss(trainY, prob)

prob = logReg.predict_proba(testX)
prob = prob[:, 1]
logRegTestingLL = log_loss(testY, prob)

prob = naiveBayes.predict_proba(trainX)
prob = prob[:, 1]
nbTrainingLL = log_loss(trainY, prob)

prob = naiveBayes.predict_proba(testX)
prob = prob[:, 1]
nbTestingLL = log_loss(testY, prob)

# print evaluation metrics
print("\nTraining Dataset Evaluation Metrics:\n")
print("Logistic Regression:               Naive Bayes:\n")
print("Accuracy:    ", f'{logRegTrainingEM[0]:.10f}', "       ", "Accuracy:    ", f'{nbTrainingEM[0]:.10f}')
print("Sensitivity: ", f'{logRegTrainingEM[1]:.10f}', "       ", "Sensitivity: ", f'{nbTrainingEM[1]:.10f}')
print("Specificity: ", f'{logRegTrainingEM[2]:.10f}', "       ", "Specificity: ", f'{nbTrainingEM[2]:.10f}')
print("Precision:   ", f'{logRegTrainingEM[3]:.10f}', "       ", "Precision:   ", f'{nbTrainingEM[3]:.10f}')
print("F1 Score:    ", f'{logRegTrainingEM[4]:.10f}', "       ", "F1 Score:    ", f'{nbTrainingEM[4]:.10f}')
print("Log Loss:    ", f'{logRegTrainingLL:.10f}',    "       ", "Log Loss:    ", f'{nbTrainingLL:.10f}')

print("\nTesting Dataset Evaluation Metrics:\n")
print("Logistic Regression:               Naive Bayes:\n")
print("Accuracy:    ", f'{logRegTestingEM[0]:.10f}', "       ", "Accuracy:    ", f'{nbTestingEM[0]:.10f}')
print("Sensitivity: ", f'{logRegTestingEM[1]:.10f}', "       ", "Sensitivity: ", f'{nbTestingEM[1]:.10f}')
print("Specificity: ", f'{logRegTestingEM[2]:.10f}', "       ", "Specificity: ", f'{nbTestingEM[2]:.10f}')
print("Precision:   ", f'{logRegTestingEM[3]:.10f}', "       ", "Precision:   ", f'{nbTestingEM[3]:.10f}')
print("F1 Score:    ", f'{logRegTestingEM[4]:.10f}', "       ", "F1 Score:    ", f'{nbTestingEM[4]:.10f}')
print("Log Loss:    ", f'{logRegTestingLL:.10f}',    "       ", "Log Loss:    ", f'{nbTestingLL:.10f}')

if(not(USE_PIPELINE)):
    print("\nLogistic Regression parameter vector:\n")
    # moves the parameter vector numbers into a single list
    temp = logReg.coef_.copy()
    temp = temp[0]
    lrParameterVector = []
    lrParameterVector.append(logReg.intercept_[0])
    for i in range(len(temp)):
        lrParameterVector.append(temp[i])
    print(lrParameterVector, "\n")
