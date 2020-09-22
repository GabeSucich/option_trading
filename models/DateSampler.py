from Learner import *
import random
import math

class DateSampler:

	def __init__(self, sampleSimulation, sampleFraction, sampleNumber):
		



def randomRange(lst, rangeFrac):

	assert rangeFrac < 1
	subLength = math.floor(len(lst)*rangeFrac)
	possibleStarts = lst[: -subLength + 1]
	possibleStartIndeces = [i for i in range(len(possibleStarts))]
	print(possibleStartIndeces)
	startIndex = random.choice(possibleStartIndeces)
	lastIndex = startIndex + subLength

	return lst[startIndex: lastIndex]

