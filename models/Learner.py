from Simulation import *
import statistics
import sys, os
import random
from LearnerParam import *


class Learner:

	def __init__(self, names, initialVals, rangeSizes , formatFunc, assessmentFunc, symbolData, investment, maxLoop = 10, stepCount=10, stopCrit=.75):

		self.symbolData = symbolData
		self.initialVales = initialVals

		self.optimizationOrder = [i for i in range(len(names))]

		self.investment = investment
		self.stepCount = stepCount
		self.stopCrit = stopCrit

		self.maxLoop = maxLoop
		self.formatFunc = formatFunc
		self.assessmentFunc = assessmentFunc

		self.bestResults = []
		self.bestParams = []
		self.bestRunningValue = investment
		
		self.params = self.createParamsObj(names, initialVals, rangeSizes)


	@property
	def stopCritMet(self):

		if len(self.bestResults) == 3 and variation(self.bestResults) < self.stopCrit:

			return True

		return False

	def createParamsObj(self, names, initialVals, rangeSizes):

		params = {}

		for i, name in enumerate(names):

			params[str(i)] = Param(name, initialVals[i], rangeSizes[i], self.stopCrit, self.stepCount)

		return params

	def createParamSets(self, paramIndex):

		param = self.paramByIndex(paramIndex)
		paramSets = [[] for i in range(len(param.range))]

		for i, param in enumerate(self.params.values()):

			for j in range(len(paramSets)):

				if i == paramIndex:

					paramSets[j].append(param.range[j])

				else:

					paramSets[j].append(param.initial)

		return paramSets

	
	def testParamRange(self, paramIndex):

		paramSets = self.createParamSets(paramIndex)
		param = self.paramByIndex(paramIndex)

		bestValue = None
		bestParamSet = None
		foundChange = False

		for paramSet in paramSets:
			
			result = self.assessmentFunc(self.symbolData, self.investment, paramSet, self.formatFunc)
				
			print(result)
			if not bestValue:

				bestValue = result
				if result > self.bestRunningValue:

					self.bestRunningValue = result
					foundChange = True
					bestParamSet = paramSet

			else:

				if result > bestValue:

					foundChange = True
					bestValue = result
					bestParamSet = paramSet
	

		if not bestParamSet:

			param.didNotOptimize()

		else:

			param.foundBest(bestParamSet[paramIndex])

	def optimizeParam(self, paramIndex):

		param = self.paramByIndex(paramIndex)

		print("Optimizing " + param.name)

		loopCounter = 0

		while not param.locked and loopCounter < self.maxLoop:

			self.testParamRange(paramIndex)
			loopCounter += 1

		if loopCounter == self.maxLoop:

			print("Optimization for " + param.name + " did not converge.")

	def unlockAllParams(self):

		for param in self.params.values():

			param.unlock()

	def optimizeAllParamsOnce(self):

		self.unlockAllParams()

		self.shuffleOptimizationOrder()

		for index in self.optimizationOrder:

			self.optimizeParam(index)


	def noOptimizationReset(self):

		for param in self.params.values():

			param.fullReset()
		

	def optimizeAllParams(self):

		loopCounter = 0

		while loopCounter < self.maxLoop:

			self.optimizeAllParamsOnce()

			newBestParams = self.getBestParams()
			self.bestParams = newBestParams

			result = self.evaluateParams(newBestParams)

			if result == self.investment:

				self.noOptimizationReset()


			else:
				

				self.updateBestResults(result)

				if self.stopCritMet:

					print("Optimization complete!")
					return

		print("Max loop was reached without convergence")

	def getBestParams(self):

		params = []

		for param in self.params.values():

			params.append(param.initial)

		return params

	def evaluateParams(self, bestParams):

		return self.assessmentFunc(self.symbolData, self.investment, bestParams, self.formatFunc)

		
	def updateBestResults(self, result):

			if len(self.bestResults) == 3:

				self.bestResults.pop(0)
				self.bestResults.append(result)

			else:

				self.bestResults.append(result)


	def paramByIndex(self, i):

		return self.params[str(i)]

	def shuffleOptimizationOrder(self):

		random.shuffle(self.optimizationOrder)


# -------------------------------------------------------------- #

def volumeAnalysisPutsFormat(a, b, c, d, e, f, g):

	return [[a, b, c, d, e], [], [f, g], 20]

def volumeAnalysisCallsFormat(a, b, c, d, e, f, g):

	return [[], [a, b, c, d, e], [f, g], 20]

def volumeAnalysisAssessment(symbolData, investment, paramSet, formatFunc):

	blockPrint()
	sim = Simulation(*symbolData, investment, "fiveMinute", volumeAnalysis, formatFunc(*paramSet), startDate = "2020-08-31", endDate = "2020-09-09")
	sim.runSimulation()
	enablePrint()

	return sim.portfolio.totalValue

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







		


