from Simulation import *
import statistics
import sys, os

class Learner:

	def __init__(self, names, optimizationOrder, initalVals, minVals, maxVals, stopCrits, maxLoop, formatFunc, assessmentFunc, symbolData, investment, stepCount=10):

		self.symbolData = symbolData
		self.optimizationOrder = optimizationOrder
		self.investment = investment
		self.stepCount = stepCount
		self.maxLoop = maxLoop
		self.formatFunc = formatFunc
		self.assessmentFunc = assessmentFunc
		self.names = names
		self.params = self.createParamsObj(names, initalVals, minVals, maxVals, stopCrits)
		self.bestParams = []

	def createParamsObj(self, names, initialVals, minVals, maxVals, stopCrits):

		paramObj = {}

		for i in range(len(names)):

			index, name, initial, maximum, minimum, stopCrit = str(i), names[i], initialVals[i], maxVals[i], minVals[i], stopCrits[i]
			valRange = maximum - minimum
			params = self.getParamRange(initial, valRange)
			paramObj[name] = {"initial": initial, "range": params, "rangeSize": valRange, "best": None, "prev3": [], "stopCrit": stopCrit, "locked": False }

		return paramObj


	def getParamRange(self, middleVal, valRangeSize):

		params = []
		interval = valRangeSize / self.stepCount
		halfCount = self.stepCount // 2

		for i in range(-halfCount, halfCount + 1):

			params.append(middleVal + i*interval)

		return params

	def updateParam(self, name):

		param = self.params[name]
		newInitial = param["best"]
		newRangeSize = (param["rangeSize"] / 2)

		self.addToPrev3(param, newInitial)

		param["initial"] = newInitial
		param["range"] = self.getParamRange(newInitial, newRangeSize)
		param["rangeSize"] = newRangeSize

		prev3 = param["prev3"]
		if len(prev3) == 3:
			if averageZScore(prev3) < param["stopCrit"]:
				param["locked"] = True

	def unlockParams(self):

		for param in self.params.values():

			param["locked"] = False

	def resetRangesAndPrev(self):

		for key in self.params.keys():

			param = self.params[key]
			param["rangeSize"] = 3*param["best"]
			param["range"] = self.getParamRange(param["initial"], param["rangeSize"])
			param["prev3"] = []



	def optimizeParam(self, variableParamName):

		print("Optimizing " + variableParamName)
		param = self.params[variableParamName]

		for i in range(self.maxLoop):

			self.optimizeParamForRange(variableParamName)
			if param["locked"]:
				print(variableParamName + " optimized!")
				return

		print("Optimization for " + variableParamName + " did not converge")

	def optimizeAllParams(self):

		paramNames = list(self.params.keys())
		for i in self.optimizationOrder:

			self.optimizeParam(paramNames[i])


	def optimizeNTimes(self, N):

		for i in range(N):

			if i > 0:
				self.resetRangesAndPrev()
				self.unlockParams()

			self.optimizeAllParams()



	def optimizeParamForRange(self, variableParamName):

		paramSets = self.createParamSets(variableParamName)
		variableIndex = list(self.params.keys()).index(variableParamName)
		bestValue = self.assessmentFunc(self.symbolData, self.investment, paramSets, self.formatFunc, variableIndex)

		param = self.params[variableParamName]
		param["best"] = bestValue
		self.updateParam(variableParamName)


	def createParamSets(self, variableParamName):

		variableParam = self.params[variableParamName]
		numParams = len(variableParam["range"])
		variableIndex = list(self.params.keys()).index(variableParamName)


		paramSets = [[] for i in range(numParams)]

		for i, param in enumerate(self.params.values()):

			if i == variableIndex:

				for j, paramVal in enumerate(param["range"]):

					paramSets[j].append(paramVal)

			else:

				for paramSet in paramSets:

					paramSet.append(param["initial"])
		
		return paramSets


	def addToPrev3(self, param, val):
		prev3 = param["prev3"]
		if len(prev3) == 3:
			prev3.pop(0)
			prev3.append(val)
		else:
			prev3.append(val)
		


def averageZScore(data):


	stdev = statistics.stdev(data)

	if stdev == 0:

		return 0

	mean = statistics.mean(data)
	zScores = [abs(value - mean)/stdev for value in data]
	return statistics.mean(zScores)


def volumeAnalysisPutsFormat(a, b, c, d, e):

	return [[a, b, c, d, e], [], 10]

def volumeAnalysisCallsFormat(a, b, c, d, e):

	return [[], [a, b, c, d, e], 10]

def volumeAnalysisAssessment(symbolData, investment, paramSets, formatFunc, variableIndex):

	maxValue = 0
	bestParams = None
	foundDifference = False

	for paramSet in paramSets:

		blockPrint()
		sim = Simulation(*symbolData, investment, "fiveMinute", volumeAnalysis, formatFunc(*paramSet))
		sim.runSimulation()
		enablePrint()
		totalValue = sim.portfolio.totalValue

		if totalValue > maxValue:

			maxValue = totalValue
			bestParams = paramSet

	print(maxValue)
	return bestParams[variableIndex]

def testFormat(a, b):
	return [a, b]

def testAssess(symbol, investment, paramSets, variableIndex):

	for paramSet in paramSets:

		if paramSet[0] > 5:

			return paramSet[variableIndex]

	return 0


def blockPrint():
	sys.stdout = open(os.devnull, 'w')

def enablePrint():
	sys.stdout = sys.__stdout__







		


