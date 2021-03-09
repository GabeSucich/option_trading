import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import Models.Stocks.basicStockMetrics as bsm
import Utils.jsonHelper as jh


class StockDay:

	def produceIntervalData(self):

		self.averagePriceData, self.volumeData, self.openPriceData, self.closePriceData, self.highPriceData, self.lowPriceData = getIntervalTradeData(self.intervals, self.priceData)

	def __init__(self, date, priceData):

		self.date = date
		self.priceData = priceData

		self.dailyOpenPrice = bsm.dailyOpenPrice(self.priceData)
		self.dailyClosePrice = bsm.dailyClosePrice(self.priceData)
		self.dailyHighPrice = bsm.dailyHighPrice(self.priceData)
		self.dailyLowPrice = bsm.dailyLowPrice(self.priceData)

		self.firstHourAveragePrice = bsm.firstHourAverage(self.priceData)

		self.dailyAveragePrice = bsm.dailyAveragePrice(self.priceData)
		self.dailyVolume = bsm.dailyVolume(priceData)

		if not hasattr(self, "intervals"):
			self.intervals = [("630", "1255")]

		self.produceIntervalData()

		self.metrics = {}

	"""Returns the date."""
	def getDate(self):
		return self.date

	def getIntervalStartTimes(self):

		times = []
		for interval in self.intervals:
			times.append(interval[0])

		return times



	"""These functions return metrics for the entirety of the day."""
	def getDailyOpenPrice(self):
		return self.dailyOpenPrice

	def getDailyClosePrice(self):
		return self.dailyClosePrice

	def getDailyHighPrice(self):
		return self.dailyHighPrice

	def getDailyLowPrice(self):
		return self.dailyLowPrice

	def getDailyAveragePrice(self):
		return self.dailyAveragePrice

	def getFirstHourAveragePrice(self):
		return self.firstHourAveragePrice

	"""These functions return metrics specific to the granularity of the day."""

	def intervalIndexOfTime(self, time):

		time = eval(time)

		for index, (startTime, endTime) in enumerate(self.intervals):

			if eval(startTime) <= time and eval(endTime) >= time:

				return index

	def getAllPrices(self):
		return self.averagePriceData

	def getAllVolumes(self):
		return self.volumeData

	def getAllOpenPrices(self):
		return self.openPriceData

	def getAllClosePrices(self):
		return self.closePriceData

	def getAllHighPrices(self):
		return self.highPriceData

	def getAllLowPrices(self):
		return self.lowPriceData

	def firstAveragePrice(self):
		return self.averagePriceData[0]

	def lastAveragePrice(self):
		return self.averagePriceData[-1]

	def firstHighPrice(self):
		return self.highPriceData[0]

	def lastHighPrice(self):
		return self.highPriceData[-1]

	def firstLowPrice(self):
		return self.lowPriceData[0]

	def lastLowPrice(self):
		return self.lowPriceData[-1]

	def averagePriceForTime(self, time):
		return self.averagePriceData[self.intervalIndexOfTime(time)]

	def volumeForTime(self, time):
		return self.volumeData[self.intervalIndexOfTime(time)]

	def highPriceForTime(self, time):
		return self.highPriceData[self.intervalIndexOfTime(time)]

	def lowPriceForTime(self, time):
		return self.lowPriceData[self.intervalIndexOfTime(time)]

	def closePriceForTime(self, time):
		return self.closePriceData[self.intervalIndexOfTime(time)]

	def openPriceForTime(self, time):
		return self.openPriceData[self.intervalIndexOfTime(time)]

	"""These functions set more advanced metrics."""

	def setMetric(self, name, value):
		self.metrics[name] = value

	def getMetric(self, name):
		return self.metrics[name]


class SemiStockDay(StockDay):

	def __init__(self, date, priceData):

		self.intervals = [("630", "940"), ("945", "1255")]

		super().__init__(date, priceData)


class QuartileStockDay(StockDay):

	def __init__(self, date, priceData):

		self.intervals = [("630", "805"), ("810", "940"), ("945", "1120"), ("1125", "1255")]

		super().__init__(date, priceData)


class HalfHourlyStockDay(StockDay):

	def __init__(self, date, priceData):

		self.intervals = [("630", "655"), ("700", "725"), ("730", "755"), ("800", "825"), ("830", "855"), ("900", "925"), ("930", "955"),
					("1000", "1025"), ("1030", "1055"), ("1100", "1125"), ("1130", "1155"), ("1200", "1225"), ("1230", "1255")]

		super().__init__(date, priceData)


def getIntervalTradeData(intervals, priceData):

	intervalPriceData = []
	intervalVolumeData = []
	intervalOpenPriceData = []
	intervalClosePriceData = []
	intervalHighPriceData = []
	intervalLowPriceData = []

	for startTime, endTime in intervals:

		intervalTimes = bsm.getIntervalTimes(priceData, startTime, endTime)

		intervalPriceData.append(bsm.intervalAveragePrice(priceData, intervalTimes))
		intervalVolumeData.append(bsm.intervalVolume(priceData, intervalTimes))
		intervalOpenPriceData.append(bsm.intervalOpenPrice(priceData, intervalTimes))
		intervalClosePriceData.append(bsm.intervalClosePrice(priceData, intervalTimes))
		intervalHighPriceData.append(bsm.intervalHighPrice(priceData, intervalTimes))
		intervalLowPriceData.append(bsm.intervalLowPrice(priceData, intervalTimes))

	return intervalPriceData, intervalVolumeData, intervalOpenPriceData, intervalClosePriceData, intervalHighPriceData, intervalLowPriceData



		






