from Simulation import *
import random
import math

class DateSampler:

	def __init__(self, sampleStockHistoricals, sampleNum=4, sampleFrac=.55, startDate = None, endDate = None):
		

	
		self.sampleNum = sampleNum
		self.sampleFrac = sampleFrac
		self.stockHistoricals = sampleStockHistoricals
		self.fullDateList = Simulation.createDateList(self.stockHistoricals, startDate, endDate)
		self.randomDateSamples = self.getRandomDateSamples()

	
	def dateSample(self, i):
		return self.randomDateSamples[i]

	
	def startDate(self, i):
		return self.dateSample(i)[0]

	
	def endDate(self, i):
		return self.dateSample(i)[-1]
	

	def refreshRandomDateSamples(self):

		self.randomDateSamples = self.getRandomDateSamples()

	def getRandomDateSamples(self):

		randomDateSamples = []

		for i in range(self.sampleNum):

			randomDateSamples.append(self.randomDateSample())

		return randomDateSamples

	def randomDateSample(self):

		return randomRange(self.fullDateList, self.sampleFrac)


def randomRange(lst, rangeFrac):

	assert rangeFrac < 1
	subLength = math.floor(len(lst)*rangeFrac)
	possibleStarts = lst[: -subLength + 1]
	possibleStartIndeces = [i for i in range(len(possibleStarts))]
	
	startIndex = random.choice(possibleStartIndeces)
	lastIndex = startIndex + subLength

	return lst[startIndex: lastIndex]


