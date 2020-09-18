import numpy as np

def addDataToRecords(data, currentRecords, recordLength):

	if len(currentRecords) == recordLength:

		currentRecords.pop(0)
		currentRecords.append(data)

	else:

		currentRecords.append(data)

def prepRecordsForRegression(currentRecords, attribute):

	xVals = []
	yVals = []
	

	for i in range(len(currentRecords)):

		xVals.append(i)
		yVals.append(currentRecords[i][attribute])
		

	return [xVals, yVals]

def regressionOrderN(currentRecords, attribute, degree):

	assert degree <= len(currentRecords) - 1, "Cannot fit a curve of degree " + str(degree) + " with only " + len(currentRecords) + " data points."

	[xVals, yVals] = prepRecordsForRegression(currentRecords, attribute)

	return np.polynomial.polynomial.polyfit(xVals, yVals, degree)

def linearRegression(currentRecords, attribute):

	coeffecients = regressionOrderN(currentRecords, attribute, 1)

	return coeffecients[1]

def cubicRegression(currentRecords, attribute):
	
	coeffecients = regressionOrderN(currentRecords, attribute, 3)

	x = len(currentRecords) - 1


	a1 = coeffecients[1]
	a2 = coeffecients[2]
	a3 = coeffecients[3]

	gradient = a1 + 2*a2*(x) + 3*a3*(x**2)
	concavity = 2*a2 + 6*a3*x
	jerk = 6*a3

	return {"gradient": gradient, "concavity": concavity, "jerk": jerk}

def desctructureCubic(regression):

	return [regression["jerk"], regression["concavity"], regression["gradient"]]