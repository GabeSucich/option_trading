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
		self.purchaseDate = currentDate
		self.purchaseTime = currentTime
		self.currentDate = currentDate
		self.currentTime = po.roundTimeUp(currentTime)
		self.cost = self.openPrice
		self.quantity = quantity
		self.active = True
		self.sellDate = None
		self.sellTime = None
		self.history = []
		self.history.append({"date": self.currentDate, "time": self.currentTime, "value": self.price, "percentChange": self.percentChange})

	def processOptionData(self, optionData):

		for date in [key for key in list(optionData.keys()) if key != "id" and key != "scrubbed"]:

			for time in list(optionData[date].keys()):

				for attribute in list(optionData[date][time].keys()):

					if type(optionData[date][time][attribute]) == str:

						optionData[date][time][attribute] = eval(optionData[date][time][attribute])

		return optionData

	def setInactive(self):

		self.active = False

	def setSellDateAndTime(self):

		self.sellDate = self.currentDate
		self.sellTime = self.currentTime

	def setTime(self, date, time):

		self.currentDate = date
		lastValidTime = po.roundTimeDown(time)

		if not is_future(self.expirationDate, self.currentDate):

			self.setInactive()
			return

		if eval(lastValidTime) > eval(self.currentTime) or lastValidTime == "630":

			self.currentTime = lastValidTime
			self.updateHistory()


		
	def updateHistory(self):

		self.history.append({"date": self.currentDate, "time": self.currentTime, "value": self.price, "percentChange": self.percentChange})

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
	def totalProfit(self):

		return self.price - self.cost
	

	@property
	def percentChange(self):

		if not self.isActive():

			return None

		return (self.price - self.cost)*100/self.cost

	@property
	def finalPercentChange(self):

		if self.isActive():

			return self.history[-1]["percentChange"]

		else:

			return self.percentChange

	@property
	def finalDate(self):

		if self.isActive():

			return self.history[-1]["date"]

		else:

			return self.sellDate

	@property
	def finalTime(self):

		if self.isActive():

			return self.history[-1]["time"]

		else:

			return self.sellTime
	
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
		try:

			if not self.currentTime:
				return po.wholeDayOpenPrice(self.optionData, self.currentDate)*100

			return po.intervalOpenPrice(self.optionData, self.currentDate, self.currentTime)*100

		except:
			return 0

	@property
	def closePrice(self):
		if not self.currentDate:
			return 0

		try:
			if not self.currentTime:
				return po.wholeDayClosePrice(self.optionData, self.currentDate)*100

			return po.intervalClosePrice(self.optionData, self.currentDate, self.currentTime)*100
		except:
			return 0

	@property
	def highPrice(self):
		if not self.currentDate:
			return 0

		try:

			if not self.currentTime:
				return po.wholeDayHighPrice(self.optionData, self.currentDate)*100

			return po.intervalHighPrice(self.optionData, self.currentDate, self.currentTime)*100

		except:

			return 0

	@property
	def lowPrice(self):
		if not self.currentDate:
			return 0

		try:
			if not self.currentTime:
				return po.wholeDayLowPrice(self.optionData, self.currentDate)*100

			return po.intervalLowPrice(self.optionData, self.currentDate, self.currentTime)*100

		except:

			return 0

	@property
	def volume(self):
		if not self.currentDate:
			return 0

		try:

			if not self.currentTime:
				return po.wholeDayVolume(self.optionData, self.currentDate)

			return po.intervalVolume(self.optionData, self.currentDate, self.currentTime)

		except:

			return 0