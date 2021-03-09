import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import Models.MetricLoggers.MetricHelpers.curveFitting as cf
from Models.Stocks.StockHistory import *

import numpy as np

class InterdayMetrics:

	def __init__(self, stockHistory, volumeRecordLength, pressureRecordLength, priceRecordLength, interdayRecordLength):

		assert interdayRecordLength > 2, "interday record length must be greater than 2"

		self.recordLengths = {"volume" : volumeRecordLength, "price" : priceRecordLength, "pressure" : pressureRecordLength, "interday" : interdayRecordLength}

		self.stockHistory = stockHistory
		self.history = stockHistory.getHistory()
		self.historyList = list(self.history.items())

		self.priceMetrics = self.calculatePriceMetrics()
		self.volumeMetrics = self.calculatePriceMetrics()
		self.buyPressureMetrics = self.calculateBuyPressureMetrics()
		self.interdayMetrics = self.calculateInterdayMetrics()

	def lastVolumeMetric(self, date):

		dateMetrics = self.volumeMetrics[date]
		endTime = list(dateMetrics.keys())[-1]
		return dateMetrics[endTime]

	def lastPriceMetric(self, date):

		dateMetrics = self.priceMetrics[date]
		endTime = list(dateMetrics.keys())[-1]
		return dateMetrics[endTime]

	def lastPressureMetric(self, date):

		dateMetrics = self.buyPressureMetrics[date]
		endTime = list(dateMetrics.keys())[-1]
		return dateMetrics[endTime]

	def interdayMetric(self, date):

		return self.interdayMetrics[date]

	def calculateInterdayMetrics(self):

		interdayMetrics = {}
		recordLength = self.recordLengths["interday"]

		for i in range(recordLength - 1, len(self.historyList)):

			date, stockDay = self.historyList[i]
			times = stockDay.getIntervalStartTimes()

			prevDays = [entry[1] for entry in self.historyList[i - recordLength + 1: i + 1]]

			prevInterdayChanges = [calculateInterdayChange(prevDays[j], prevDays[j + 1]) for j in range(len(prevDays) - 1)]
			mean = np.mean(prevInterdayChanges)
			gradient, _ = cf.fit_linear_model(prevInterdayChanges)
			concavity, _, _ = cf.fit_quadratic_model(prevInterdayChanges)

			consecutiveIncreases = self.calculateConsecutiveChanges(i, 1)
			consecutiveDecreases = self.calculateConsecutiveChanges(i, -1)

			interdayMetrics[date] = {"mean" : mean, "gradient" : gradient, "concavity" : concavity, "consecutiveIncreases" : consecutiveIncreases, "consecutiveDecreases" : consecutiveDecreases}

		return interdayMetrics

	def calculateConsecutiveChanges(self, currentIndex, direction):

		consecutiveChanges = 0

		while currentIndex > 0:

			if direction == 1 and calculateInterdayChange(self.historyList[currentIndex - 1][1], self.historyList[currentIndex][1]) > 0:
				consecutiveChanges += 1
				currentIndex -= 1

			elif direction == -1 and calculateInterdayChange(self.historyList[currentIndex - 1][1], self.historyList[currentIndex][1]) < 0:
				consecutiveChanges += 1
				currentIndex -= 1

			else:
				break

		return consecutiveChanges


	def calculateVolumeMetrics(self):

		volumeMetrics = {}
		recordLength = self.recordLengths["volume"]

		for i in range(recordLength - 1, len(self.historyList)):

			date, stockDay = self.historyList[i]
			times = stockDay.getIntervalStartTimes()

			volumeMetrics[date] = {}

			volumeValues = self.compilePrevValues(i, lambda stockDay: stockDay.getAllVolumes(), recordLength)

			for i, volume in enumerate(stockDay.getAllVolumes()):

				volumeValues.append(volume)

				gradient, _ = cf.fit_linear_model(volumeValues)
				concavity, _, _ = cf.fit_quadratic_model(volumeValues)

				volumeMetrics[date][times[i]] = {"gradient" : gradient/np.mean(volumeValues[: len(times)]), "concavity" : concavity/np.mean(volumeValues[: len(times)])}

		return volumeMetrics

	def calculateBuyPressureMetrics(self):

		buyPressureMetrics = {}
		recordLength = self.recordLengths["pressure"]

		for i in range(recordLength - 1, len(self.historyList)):

			date, stockDay = self.historyList[i]
			times = stockDay.getIntervalStartTimes()

			buyPressureMetrics[date] = {}

			buyPressureValues = self.compilePrevValues(i, lambda stockDay: buyPressureGetter(stockDay), recordLength)

			for i, buyPressure in enumerate(buyPressureGetter(stockDay)):

				buyPressureValues.append(buyPressure)

				gradient, _ = cf.fit_linear_model(buyPressureValues)
				concavity, _, _ = cf.fit_quadratic_model(buyPressureValues)
				mean = np.mean(buyPressureValues)

				buyPressureMetrics[date][times[i]] = {"gradient" : gradient, "concavity" : concavity, "mean" : mean }

		return buyPressureMetrics

	def calculatePriceMetrics(self):

		priceMetrics = {}
		recordLength = self.recordLengths["price"]

		for i in range(recordLength - 1, len(self.historyList)):

			date, stockDay = self.historyList[i]
			times = stockDay.getIntervalStartTimes()

			priceMetrics[date] = {}

			priceValues = self.compilePrevValues(i, lambda stockDay: averagePriceGetter(stockDay), recordLength)

			for i, price in enumerate(averagePriceGetter(stockDay)):

				priceValues.append(price)

				gradient, _ = cf.fit_linear_model(priceValues)
				concavity, _, _ = cf.fit_quadratic_model(priceValues)

				priceMetrics[date][times[i]] = {"gradient" : gradient/np.mean(priceValues[: len(times)]), "concavity" : concavity/np.mean(priceValues[: len(times)])}

		return priceMetrics

	def compilePrevValues(self, currentIndex, attributeGetter, recordLength):

		assert currentIndex >= recordLength - 1, "Cannot compile records for day {0} with record length of {1}".format(currentIndex, self.recordLength)

		prevDays = [entry[1] for entry in self.historyList[currentIndex - recordLength + 1: currentIndex]]
		values = []

		for day in prevDays:
			values += attributeGetter(day)

		return values

def volumeGetter(stockDay):

	return stockDay.getAllVolumes()

def averagePriceGetter(stockDay):

	return stockDay.getAllPrices()

def buyPressureGetter(stockDay):

	openPrices = stockDay.getAllOpenPrices()
	closePrices = stockDay.getAllClosePrices()
	pairs = list(zip(openPrices, closePrices))

	buyPressures = []

	for pair in pairs:

		openPrice, closePrice = pair
		buyPressures.append(calculateBuyPressure(openPrice, closePrice))

	return buyPressures

def calculateBuyPressure(openPrice, closePrice):

	epsilon = (openPrice - closePrice)**2/(openPrice + closePrice)**2
	buyPressure = 10000*(1/(1 - epsilon) - 1)*(np.sign(closePrice - openPrice))
	return buyPressure

def calculateInterdayChange(stockDay1, stockDay2):

	openPrice, closePrice = stockDay2.getDailyOpenPrice(), stockDay1.getDailyClosePrice()
	return 100*(openPrice - closePrice)/closePrice






