import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *

class SimPortfolioControl:

	def __init__(self, symbolList, historicalsList, optionHistoricalsList, investment):

		self.initialInvestment = investment
		self.cash = investment
		self.invested = 0
		self.createStockPortfolios()

		@property
		def totalValue(self):
			return self.cash + self.invested

		@property
		def percentReturn(self):
			return (self.totalValue - self.initialInvestment)*100/self.initialInvestment

		def createStockPortfolios(self, symbolList, historicalsList, optionHistoricalsList):

			self.stockPortfolios = {}

			symbolIndex = 0

			for symbol in symbolList:

				self.stockPortfolios[symbol] = StockPortfolio(symbol, symbolList[symbolIndex], optionHistoricalsList[symbolIndex])
				symbolIndex += 1

class StockPortfolio:

	def __init__(self, symbol, historicals, optionHistoricals):

		self.symbol = symbol
		self.historicals = historicals
		self.optionHistoricals = optionHistoricals
