import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Utils.datetime_funcs import *
from Stock import *

import options.processOptionHistoricals as po
from Option import *

class SimPortfolioControl:

	def __init__(self, symbolList, historicalsList, optionHistoricalsList, investment, currentDate, currentTime):

		self.initialInvestment = investment
		self.cash = investment
		self.invested = 0
		self.createStockPortfolios(symbolList, historicalsList, optionHistoricalsList, currentDate, currentTime)

	@property
	def totalValue(self):
		return self.cash + self.invested

	@property
	def percentReturn(self):
		return (self.totalValue - self.initialInvestment)*100/self.initialInvestment

	def increaseInvested(self, amt):
		if amt > self.cash:
			print("Cannot invest more than you have in cash!")
			return

		self.cash -= amt
		self.invested += amt

	def decreaseInvested(self, amt):
		if amt > self.invested:
			print("You cannot increase your cash by more than you have invested!")
			return
		self.cash += amt
		self.invested -= amt

	def updateInvestedAmt(self):

		self.invested = 0
		for stockPortfolio in list(self.stockPortfolios.values()):

			self.invested += stockPortfolio.invested


	def createStockPortfolios(self, symbolList, historicalsList, optionHistoricalsList, currentDate, currentTime):

		self.stockPortfolios = {}

		symbolIndex = 0

		for symbol in symbolList:

			self.stockPortfolios[symbol] = StockPortfolio(symbol, historicalsList[symbolIndex], optionHistoricalsList[symbolIndex], currentDate, currentTime, self)
			symbolIndex += 1

	def updateTime(self, date, time):

		for stockPortfolio in list(self.stockPortfolios.values()):

			stockPortfolio.setTime(date, time)

		self.updateInvestedAmt()

	def stockProfile(self, symbol):

		try:
			return self.stockPortfolios[symbol]

		except:

			print(symbol + " is not included in portfolio.")

	def getStock(self, symbol):

		return self.stockProfile(symbol).stock


class StockPortfolio:

	def __init__(self, symbol, historicals, optionHistoricals, currentDate, currentTime, mainPortfolio):

		self.mainPortfolio = mainPortfolio
		self.invested = 0
		self.options = []
		self.symbol = symbol
		self.historicals = historicals
		self.optionHistoricals = optionHistoricals
		self.stock = Stock(symbol, historicals, currentDate, currentTime)
		self.currentDate = currentDate
		self.currentTime = currentTime
		self.options = []

	@property
	def availableCash(self):
		return self.mainPortfolio.cash

	@property
	def stockPrice(self):
		return self.stock.price
	
	def purchaseUpdate(self, purchaseCost):

		self.invested += purchaseCost
		self.mainPortfolio.increaseInvested(purchaseCost)

	def saleUpdate(self, sellAmt):

		self.invested -= sellAmt
		self.mainPortfolio.decreaseInvested(sellCmt)

	def setOptionTimes(self):

		for option in self.options:

			if option.isActive():

				option.setTime(self.currentDate, self.currentTime)

	def updateInvested(self):

		self.invested = 0

		for option in self.options:

			if option.isActive():

				self.invested += option.totalValue


	def setTime(self, date, time=None):

		self.currentDate = date
		self.currentTime = time
		self.stock.setTime(date, time)
		self.setOptionTimes()
		self.updateInvested()


	def getOptionData(self, optionType, expirationDate, strikePrice):

		strikePrice = po.formatStrikePrice(strikePrice)
		return self.processOptionData(self.optionHistoricals[expirationDate][optionType + "s"][strikePrice])

	def processOptionData(self, optionData):

		for date in [key for key in list(optionData.keys()) if key != "id" and key != "scrubbed"]:

			for time in list(optionData[date].keys()):

				for attribute in list(optionData[date][time].keys()):

					if type(optionData[date][time][attribute]) == str:

						optionData[date][time][attribute] = eval(optionData[date][time][attribute])

		return optionData

	def findShortestTermOption( self, optionType , purchaseMax ):

		assert purchaseMax <= self.availableCash, 
		
		if optionType == "call":

			


	def shortestTermHeper(self, optionType, purchaseMax, interval=1):

		if optionType == "call":

			optionInfo = po.nearestCall(self.stockPrice, self.currentDate, self.optionHistoricals, interval = 1)
			roundedTime = po.roundTimeUp(self.currentTime)
			price = 




	def purchaseOption(self, optionType, expirationDate, strikePrice, quantity):

		assert is_future(expirationDate, self.currentDate), "Cannot purchase an option which has expired!"

		optionData = self.getOptionData(optionType, expirationDate, strikePrice)

		roundedTime = po.roundTimeUp(self.currentTime)
		
		purchase_cost = quantity*(optionData[self.currentDate][roundedTime]["open_price"])*100

		if purchase_cost >= self.availableCash:

			print("Not enough to purchase this option!")
			return
		
		self.options.append( Option(optionType, strikePrice, expirationDate, quantity, optionData, self.currentDate, self.currentTime) )
		self.purchaseUpdate(purchase_cost)

	def sellOption(self, option):

		assert option.isActive(), "Cannot sell an inactive item"

		if eval(self.currentTime) < eval(option.currentTime):

			print("Trying to sell in future. Not an error!")
			return

		sellAmt = option.totalValue
		option.setInactive()
		option.setSellDate()
		self.saleUpdate(sellAmt)





