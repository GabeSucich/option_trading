import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import options.processOptionHistoricals as po
from Utils.datetime_funcs import *

class Option:

	def __init__(self, optionType, strikePrice, expirationDate, quantity, optionData, currentDate, currentTime):

		self.optionType = optionType
		self.expirationDate = expirationDate
		self.strikePrice = strikePrice
		self.optionData = optionData
		self.currentDate = currentDate
		self.currentTime = po.roundTimeUp(currentTime)
		self.cost = self.openPrice
		self.quantity = quantity
		self.active = True
		self.sellDate = None

	def processOptionData(self, optionData):

		for date in [key for key in list(optionData.keys()) if key != "id" and key != "scrubbed"]:

			for time in list(optionData[date].keys()):

				for attribute in list(optionData[date][time].keys()):

					if type(optionData[date][time][attribute]) == str:

						optionData[date][time][attribute] = eval(optionData[date][time][attribute])

		return optionData

	def setInactive(self):

		self.active = False

	def setSellDate(self):

		self.sellDate = self.currentDate

	def setTime(self, date, time):

		self.currentDate = date
		lastValidTime = po.roundTimeDown(time)
		if lastValidTime > self.currentTime:

			self.currentTime = lastValidTime

		if not is_future(self.expirationDate, self.currentDate):

			self.currentDate = None
			self.currentTime = None
			self.setInactive()

	def isActive(self):
		if self.active:

			return True

		return False
	
	@property
	def totalValue(self):
		if not self.isActive():

			return 0

		return self.quantity*self.price

	@property
	def percentChange(self):

		if not self.isActive():

			return None

		return (self.price - self.cost)*100/self.cost



	@property
	def price(self):

		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayAveragePrice(self.optionData, self.currentDate)*100

		return po.intervalAveragePrice(self.optionData, self.currentDate, self.currentTime)*100

	@property
	def openPrice(self):
		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayOpenPrice(self.optionData, self.currentDate)*100

		return po.intervalOpenPrice(self.optionData, self.currentDate, self.currentTime)*100

	@property
	def closePrice(self):
		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayClosePrice(self.optionData, self.currentDate)*100

		return po.intervalClosePrice(self.optionData, self.currentDate, self.currentTime)*100

	@property
	def highPrice(self):
		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayHighPrice(self.optionData, self.currentDate)*100

		return po.intervalHighPrice(self.optionData, self.currentDate, self.currentTime)*100

	@property
	def lowPrice(self):
		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayLowPrice(self.optionData, self.currentDate)*100

		return po.intervalLowPrice(self.optionData, self.currentDate, self.currentTime)*100

	@property
	def volume(self):
		if not self.currentDate:
			return 0

		if not self.currentTime:
			return po.wholeDayVolume(self.optionData, self.currentDate)

		return po.intervalVolume(self.optionData, self.currentDate, self.currentTime)