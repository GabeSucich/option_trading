import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from Models.Stocks.StockHistory import *

class InterdayChanges:

	def __init__(self, stockHistory):

		self.stockHistory = stockHistory
		self.interdayChanges = produceInstantDailyChanges(stockHistory)

	def getInterdayChanges(self):
		return self.interdayChanges


def openClosePercentChange(stockDay1, stockDay2):
	openPrice, closePrice = stockDay2.getFirstHourAveragePrice(), stockDay1.getDailyClosePrice()
	return round((openPrice - closePrice)*100/closePrice , 2)

def produceInstantDailyChanges(stockHistory):

	data = {}

	prevDate = None
	prevStockDay = None

	for date, stockDay in stockHistory.getHistory().items():

		data[date] = {}

		if prevDate:

			percentChange = openClosePercentChange(prevStockDay, stockDay)
			data[date]["prev_day_change"] = percentChange
			data[prevDate]["next_day_change"] = percentChange

		prevDate, prevStockDay = date, stockDay

	return data











