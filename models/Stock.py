import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


import stocks.processStockHistoricals as ps



class Stock:

	def __init__(self, symbol, historicals, currentDate, currentTime):
		self.symbol = symbol
		self.historicals = self.processHistoricals(historicals)
		self.currentDate = currentDate
		self.currentTime = currentTime

	def processHistoricals(self, historicals):
		for date in list(historicals.keys()):
			for time in list(historicals[date].keys()):
				for attribute in list(historicals[date][time].keys()):
					if type(historicals[date][time][attribute]) == str:
						historicals[date][time][attribute] = eval(historicals[date][time][attribute])
		return historicals

	def setTime(self, date, time=None):

		self.currentDate = date
		self.currentTime = time

	@property
	def price(self):

		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayAveragePrice(self.historicals, self.currentDate)

		return ps.intervalAveragePrice(self.historicals, self.currentDate, self.currentTime)

	@property
	def openPrice(self):
		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayOpenPrice(self.historicals, self.currentDate)

		return ps.intervalOpenPrice(self.historicals, self.currentDate, self.currentTime)

	@property
	def closePrice(self):
		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayClosePrice(self.historicals, self.currentDate)

		return ps.intervalClosePrice(self.historicals, self.currentDate, self.currentTime)

	@property
	def highPrice(self):
		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayHighPrice(self.historicals, self.currentDate)

		return ps.intervalHighPrice(self.historicals, self.currentDate, self.currentTime)

	@property
	def lowPrice(self):
		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayLowPrice(self.historicals, self.currentDate)

		return ps.intervalLowPrice(self.historicals, self.currentDate, self.currentTime)

	@property
	def volume(self):
		if not self.currentDate:
			return None

		if not self.currentTime:
			return ps.wholeDayVolume(self.historicals, self.currentDate)

		return ps.intervalVolume(self.historicals, self.currentDate, self.currentTime)

	


	

