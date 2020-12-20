import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from StockDay import *

import Utils.jsonHelper as jh

class StockHistory:

	def __init__(self, symbol):

		self.history = createHistory(jh.loadStockHistoricals(symbol))

	def getHistory(self):

		return self.history


def createHistory(historicals):

	history = {}
	for date in historicals:
		history[date] = StockDay(date, historicals[date])

	return dict(sorted(history.items()))


