import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

class IntradayChanges:

	def __init__(self, stockHistory):

		self.stockHistory = stockHistory
		self.dailyChanges = self.calculateDailyChanges()


	def calculateDailyChanges(self):

		dailyChanges = {}
		prevDate = None
		prevStockDay = None

		for date, currentStockDay in self.stockHistory.getHistory():

			if prevDate:

				closeOPenDiff = percentChange(prevStockDay, currentStockDay)
				dailyChanges[prevDate][""]

			prevDate = date
			prevStockDay = currentStockDay



def percentChange(stockDay1, stockDay2):
	openPrice, closePrice = stockDay2.getOpenPrice(), stockDay1.getClosePrice()
	return (openPrice - closePrice)*100/closePrice