from Learner import *

class MasterLearner:

	def __init__(self, learnerParams, stopCrit):

		self.stopCrit = stopCrit
		self.learnerParams = learnerParams
		self.createLearner()
		self.bestParamSets = []
		self.finalBestParams = None

	def createLearner(self):

		self.learner = Learner(*self.learnerParams)

	def getBestParams(self):

		return self.finalBestParams

	def optimize(self):

		optimized = False

		while not optimized:

			self.learner.optimizeAllParams()
			self.addToBestParams(self.learner.getBestParams())
			print("BestParamSets: " + str(self.bestParamSets))

			if self.evaluateParamConvergence():

				optimized = True

			else:

				self.createLearner()

		print("Optimization complete!")

	def addToBestParams(self, params):

		if len(self.bestParamSets) == 3:

			self.bestParamSets.pop(0)
			self.bestParamSets.append(params)

		else:

			self.bestParamSets.append(params)

	def evaluateParamConvergence(self):

		stopCritExceeders = 0

		if len(self.bestParamSets) == 3:

			for i in range(len(self.bestParamSets)):

				likeParams = [params[i] for params in self.bestParamSets]

				if variation(likeParams) > self.stopCrit:

					stopCritExceeders += 1

			return stopCritExceeders <= 2

		return False


