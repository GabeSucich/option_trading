import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import basicStockMetrics as bsm
import Utils.jsonHelper as jh


class StockDay:

	def __init__(self, date, priceData):

		self.date = date
		self.priceData = convertPricesToNumeric(priceData)

		self.openPrice = bsm.dailyOpenPrice(self.priceData)
		self.closePrice = bsm.dailyClosePrice(self.priceData)
		self.highPrice = bsm.dailyHighPrice(self.priceData)
		self.lowPrice = bsm.dailyLowPrice(self.priceData)

		self.averagePrice = bsm.dailyAveragePrice(self.priceData)

	"""Returns the date."""
	def getDate(self):
		return self.date

	"""These functions return basic metrics of the price."""
	def getOpenPrice(self):
		return self.openPrice

	def getClosePrice(self):
		return self.closePrice

	def getHighPrice(self):
		return self.highPrice

	def getLowPrice(self):
		return self.lowPrice

	def getAveragePrice(self):
		return self.averagePrice


class QuartileStockDay(StockDay):

	def __init__(self, date, priceData):

		q1 = bsm.getIntervalTimes(priceData, "630", "805")
		q2 = bsm.getIntervalTimes(priceData, "810", "940")
		q3 = bsm.getIntervalTimes(priceData, "945", "1120")
		q4 = bsm.getIntervalTimes(priceData, "1125", "1255")

		self.q1AveragePrice = bsm.intervalAveragePrice(priceData, q1)
		self.q2AveragePrice = bsm.intervalAveragePrice(priceData, q2)
		self.q3AveragePrice = bsm.intervalAveragePrice(priceData, q3)
		self.q4AveragePrice = bsm.intervalAveragePrice(priceData, q4)

		self.q1Volume = bs.intervalVolume(priceData, q1)
		self.q2Volume = bs.intervalVolume(priceData, q2)
		self.q3Volume = bs.intervalVolume(priceData, q3)
		self.q4Volume = bs.intervalVolume(priceData, q4)

		super().__init__(date, priceData)


