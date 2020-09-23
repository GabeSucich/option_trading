import statistics

class Param:

	def __init__(self, name, initialVal, paramSign, stopCriteria=.75, stepCount=10):

		assert paramSign in [1, 0, -1]

		self.paramSign = paramSign
		self.firstGuess = initialVal
		self.initialRangeSize = 2*abs(self.firstGuess) or 40

		self.name = name
		self.initial = initialVal
		
		self.rangeSize = self.initialRangeSize
		self.stopCriteria = stopCriteria
		self.stepCount = stepCount
		self.setParamRange()
		self.locked = False
		self.best = None
		self.prevValues = []
		self.noOptimization = False

	def stretchParamRange(self):

		self.initial = self.firstGuess
		self.rangeSize = self.initialRangeSize


	def setParamRange(self):

		params = []
		interval = self.rangeSize / self.stepCount
		halfCount = self.stepCount // 2

		for i in range(-halfCount, halfCount + 1):

			params.append(self.initial + i*interval)

		if self.paramSign == 1:

			self.range = [param for param in params if param >= 0]

		elif self.paramSign == -1:

			self.range = [param for param in params if param <= 0]

		else:

			self.range = params



	def shrinkParamRange(self):

		self.rangeSize = 2 * self.rangeSize / self.stepCount
		self.setParamRange()

	def resetParamRange(self):

		if self.noOptimization:

			self.rangeSize = self.initialRangeSize

		else:

			self.rangeSize = max(3*self.initial, 1)

		self.setParamRange()

	def clearPrev(self):

		self.prevValues = []

	def fullReset(self):

		self.stretchParamRange()
		self.unlock()
		self.clearPrev()

	def lock(self):
		self.locked = True

	def unlock(self):
		self.locked = False

	def didNotOptimize(self):

		self.noOptimization = True
		self.lock()
		self.resetParamRange()
		self.clearPrev()

	def optimized(self):

		self.lock()
		self.resetParamRange()
		self.clearPrev()

	def foundBest(self, bestParam):

		self.best = bestParam
		self.initial = bestParam
		self.notOptimized = False
		self.addToPrev(bestParam)

		if self.stopCritMet:

			self.optimized()

		else:

			self.shrinkParamRange()

	def addToPrev(self, val):

		if len(self.prevValues) == 3:

			self.prevValues.pop(0)
			self.prevValues.append(val)

		else:

			self.prevValues.append(val)

	def getPrevVariation(self):

		return variation(self.prevValues)

	@property
	def stopCritMet(self):


		if len(self.prevValues) == 3 and self.getPrevVariation() <= self.stopCriteria:
			
			return True

		return False

def variation(data):
	stdev = statistics.stdev(data)

	if stdev == 0:

		return 0

	mean = statistics.mean(data)
	zScores = [abs(value - mean)/stdev for value in data]
	return statistics.mean(zScores)


	
	
