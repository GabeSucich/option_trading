import matplotlib.pyplot as plt
import statistics
import sys, os
from Simulation import *
from SimPortfolioControl import *
from IndividualStockHistorical import *

class ProcessHistoricals:

	def __init__(self, Simulation):

		self.findOptionDataForEachStock(Simulation)
		self.goodOptions, self.badOptions = self.seperateOptions()
		self.goodCalls, self.badCalls = self.seperateCalls()
		self.goodPuts, self.badPuts = self.seperatePuts()
		self.totalProfit = self.findTotalProfit(Simulation)
		self.actions ,self.goodActions, self.badActions = findGoodandBadActions(Simulation)
		self.simulation = Simulation


	def findOptionDataForEachStock(self, Simulation):

		self.IndividualStockHistorical = {}
		self.options = []
		self.calls = []
		self.puts = []
		self.stockPortfolioSymbols = list(Simulation.portfolio.stockPortfolios.keys())
		for sym in self.stockPortfolioSymbols:
			self.IndividualStockHistorical[sym] = IndividualStockHistorical(Simulation.stockProfile(sym).options, sym, Simulation)
			for option in self.IndividualStockHistorical[sym].options:
				self.options.append(option)
				if option.optionType == "call":
					self.calls.append(option)
				else:
					self.puts.append(option)


	def findGoodandBadActions(self, Simulation):
		actions = []
		goodActions = []
		


	def findStockHistoricalFromSym(self, sym):

		assert sym in self.stockPortfolioSymbols, "The symbol {0} is not part of this simulation".format(sym)
		return self.IndividualStockHistorical[sym]

	def findTotalProfit(self, simulation):

		return simulation.portfolio.totalProfit

	def seperateOptions(self):

		goodOptions = []
		badOptions = []
		for option in self.options:
			if option.finalPercentChange > 0:
				goodOptions.append(option)
			else:
				badOptions.append(option)
		return [goodOptions, badOptions]

	def seperateCalls(self):

		goodCalls = [];
		badCalls = [];
		for call in self.calls:
			if call.finalPercentChange > 0:
				goodCalls.append(call)
			else:
				badCalls.append(call)
		return [goodCalls, badCalls]

	def seperatePuts(self):

		goodPuts = [];
		badPuts = [];
		for put in self.puts:
			if put.finalPercentChange > 0:
				goodPuts.append(put)
			else:
				badPuts.append(put)
		return [goodPuts, badPuts]

	def callCount(self):

		return len(self.calls)

	def callCountForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).callCount()

	def putCount(self):

		return len(self.puts)

	def putCountForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).putCount()

	def optionCount(self):

		return self.callCount() + self.putCount()

	def optionCountForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).optionCount()

	def findBestAndWorstCall(self):

		bestCall = None
		worstCall = None
		for call in self.calls:
			if worstCall is None or call.finalPercentChange < worstCall.finalPercentChange:
				worstCall = call
			if bestCall is None or call.finalPercentChange > bestCall.finalPercentChange:
				bestCall = call
		return [bestCall, worstCall]

	def findBestAndWorstCallForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findBestAndWorstCall()

	def findBestAndWorstPut(self):

		bestPut = None
		worstPut = None
		for put in self.puts:
			if worstPut is None or put.finalPercentChange < worstPut.finalPercentChange:
				worstPut = put
			if bestPut is None or put.finalPercentChange > bestPut.finalPercentChange:
				bestPut = put
		return [bestPut, worstPut]

	def findBestAndWorstPutForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findBestAndWorstPut()

	def findCallPercentIncreases(self):

		callPercentIncreases = []
		for call in self.goodCalls:
			callPercentIncreases.append(call.finalPercentChange)
		return callPercentIncreases

	def findCallPercentIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallPercentIncreases()

	def findAverageCallPercentIncrease(self):

		return statistics.mean(self.findCallPercentIncreases())

	def findAverageCallPercentIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallPercentIncrease()

	def findPutPercentIncreases(self):

		putPercentIncreases = [];
		for put in self.goodPuts:
			putPercentIncreases.append(put.finalPercentChange)
		return putPercentIncreases

	def findPutPercentIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutPercentIncreases()

	def findAveragePutPercentIncrease(self):

		return statistics.mean(self.findPutPercentIncreases())

	def findAveragePutPercentIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutPercentIncrease()

	def findCallPercentDecreases(self):

		callPercentDecreases = []
		for call in self.badCalls:
			callPercentDecreases.append(call.finalPercentChange)
		return callPercentDecreases

	def findCallPercentDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallPercentDecreases()

	def findAverageCallPercentDecrease(self):

		return statistics.mean(self.findCallPercentDecreases())

	def findAverageCallPercentDecreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallPercentDecrease()

	def findPutPercentDecreases(self):

		putPercentDecreases = []
		for put in self.badPuts:
			findPutPercentDecreases.append(put.finalPercentChange)
		return putPercentDecreases

	def findPutPercentDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutPercentDecreases()

	def findAveragePutPercentDecrease(self):

		return statistics.mean(self.findPutPercentDecreases())

	def findAveragePutPercentDecreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutPercentDecrease()

	def findOptionPercentIncreases(self):

		optionPercentIncreases = []
		for option in self.goodOptions:
			optionPercentIncreases.append(option.finalPercentChange)
		return optionPercentIncreases

	def findOptionPercentIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionPercentIncreases()

	def findAverageOptionPercentIncrease(self):

		return statistics.mean(self.findOptionPercentIncreases())

	def findAverageOptionPercentIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionPercentIncrease()

	def findOptionPercentDecreases(self):

		optionPercentDecreases = []
		for option in self.badOptions:
			optionPercentDecreases.append(option.finalPercentChange)
		return optionPercentDecreases

	def findOptionPercentDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionPercentDecreases()

	def findAverageOptionPercentDecrease(self):

		return statistics.mean(self.findOptionPercentDecreases())

	def findAverageOptionPercentDecreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionPercentDecrease()

	def findCallPercentChanges(self):

		return self.findCallPercentIncreases() + self.findCallPercentDecreases()

	def findCallPercentChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallPercentChanges()

	def findPutPercentChanges(self):

		return self.findPutPercentIncreases() + self.findPutPercentDecreases()

	def findPutPercentChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutPercentChanges()

	def findOptionPercentChanges(self):

		return self.findCallPercentChanges() + self.findPutPercentChanges()

	def findOptionPercentChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionPercentChanges()

	def findAverageCallPercentChange(self):

		return statistics.mean(self.findCallPercentChanges())

	def findAverageCallPercentChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallPercentChange()

	def findAveragePutPercentChange(self):

		return statistics.mean(self.findPutPercentChanges())

	def findAveragePutPercentChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutPercentChange()

	def findAverageOptionPercentChange(self):

		return statistics.mean(self.findOptionPercentChanges())

	def findAverageOptionPercentChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionPercentChange()

	def findCallMoneyIncreases(self):

		callMoneyIncreases = []
		for call in self.goodCalls:
			callMoneyIncreases.append(call.totalProfit)
		return callMoneyIncreases

	def findCallMoneyIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallMoneyIncreases()

	def findAverageCallMoneyIncrease(self):

		return statistics.mean(self.findCallMoneyIncreases())

	def findAverageCallMoneyIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallMoneyIncrease()

	def findCallMoneyDecreases(self):

		callMoneyDecreases = []
		for call in self.badCalls:
			callMoneyDecreases.append(call.totalProfit)
		return callMoneyDecreases

	def findCallMoneyDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallMoneyDecreases()

	def findAverageCallMoneyDecrease(self):

		return statistics.mean(self.findCallMoneyDecreases())

	def findAverageCallMoneyDecreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallMoneyDecrease()

	def findPutMoneyIncreases(self):

		putMoneyIncreases = []
		for put in self.goodPuts:
			putMoneyIncreases.append(put.totalProfit)
		return putMoneyIncreases

	def findPutMoneyIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutMoneyIncreases()

	def findAveragePutMoneyIncrease(self):

		return statistics.mean(self.findPutMoneyIncreases())

	def findAveragePutMoneyIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutMoneyIncrease()

	def findPutMoneyDecreases(self):

		putMoneyDecreases = []
		for put in self.badPuts:
			putMoneyDecreases.append(put.totalProfit)
		return putMoneyDecreases

	def findPutMoneyDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutMoneyDecreases()

	def findAveragePutMoneyIncrease(self):

		return statistics.mean(self.findPutMoneyDecreases())

	def findAveragePutMoneyIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutMoneyIncrease()

	def findOptionMoneyIncreases(self):

		optionMoneyIncreases = []
		for option in self.goodOptions:
			optionMoneyIncreases.append(option.totalProfit)
		return optionMoneyIncreases

	def findOptionMoneyIncreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionMoneyIncreases()

	def findAverageOptionMoneyIncrease(self):

		return statistics.mean(self.findOptionMoneyIncreases())

	def findAverageOptionMoneyIncreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionMoneyIncrease()

	def findOptionMoneyDecreases(self):

		optionMoneyDecreases = []
		for option in self.badOptions:
			optionMoneyDecreases.append(option.totalProfit)
		return optionMoneyDecreases

	def findOptionMoneyDecreasesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionMoneyDecreases()

	def findAverageOptionMoneyDecrease(self):

		return statistics.mean(self.findOptionMoneyDecreases())

	def findAverageOptionMoneyDecreaseForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionMoneyDecrease()

	def findCallMoneyChanges(self):

		return self.findCallMoneyIncreases() + self.findCallMoneyDecreases()

	def findCallMoneyChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findCallMoneyChanges()

	def findAverageCallMoneyChange(self):

		return statistics.mean(self.findCallMoneyChanges())

	def findAverageCallMoneyChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageCallMoneyChange()

	def findPutMoneyChanges(self):

		return self.findPutMoneyIncreases() + self.findPutMoneyDecreases()

	def findPutMoneyChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findPutMoneyChanges()

	def findAveragePutMoneyChange(self):

		return statistics.mean(self.findPutMoneyChanges())

	def findAveragePutMoneyChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAveragePutMoneyChange()

	def findOptionMoneyChanges(self):

		return self.findCallMoneyChanges() + self.findPutMoneyChanges()

	def findOptionMoneyChangesForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findOptionMoneyChanges()

	def findAverageOptionMoneyChange(self):

		return statistics.mean(self.findOptionMoneyChanges())

	def findAverageOptionMoneyChangeForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).findAverageOptionMoneyChange()

	def writeReport(self):

		print("The simulation made a total profit of ${0} starting from an initial investment of ${1}".format(self.totalProfit, self.simulation.portfolio.initialInvestment))
		print("a total of {0} options were traded, with {1} of those being calls and {2} being puts".format(self.optionCount(), self.callCount(), self.putCount()))
		print("of the {0} options, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.optionCount(), round(self.percentGoodOptions(), 2), round(self.percentBadOptions(), 2)))
		print("of the {0} calls, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.callCount(), round(self.percentGoodCalls(), 2), round(self.percentBadCalls(), 2)))
		print("of the {0} puts, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.putCount(), round(self.percentGoodPuts(), 2), round(self.percentBadPuts(), 2)))

	def writeReportForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).writeReport()

	def getXAxisValues(self):

		return [5*i for i in range(len(self.simulation.history))]

	def getYAxisValues(self):

		portfolioValues = [];
		for dataPoint in self.simulation.history:
			portfolioValues.append(dataPoint["totalValue"])
		return portfolioValues

	def plot(self):

		xAxis = self.getXAxisValues()
		yAxis = self.getYAxisValues()
		plt.plot(xAxis, yAxis)
		plt.title('Portfolio Value Over Time')
		plt.xlabel('Minutes')
		plt.ylabel('Portfolio Value')
		plt.show()

	def plotForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).plot()

	def percentGoodOptions(self):

		if len(self.goodOptions) + len(self.badOptions) == 0:
			return 0
		return len(self.goodOptions)/(len(self.goodOptions) + len(self.badOptions))

	def percentGoodOptionsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentGoodOptions()

	def percentBadOptions(self):

		if len(self.goodOptions) + len(self.badOptions) == 0:
			return 0
		return len(self.badOptions)/(len(self.goodOptions) + len(self.badOptions))

	def percentBadOptionsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentBadOptions()

	def percentGoodCalls(self):

		if len(self.goodCalls) + len(self.badCalls) == 0:
			return 0
		return len(self.goodCalls)/(len(self.goodCalls) + len(self.badCalls))

	def percentGoodCallsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentGoodCalls()

	def percentBadCalls(self):

		if len(self.goodCalls) + len(self.badCalls) == 0:
			return 0
		return len(self.badCalls)/(len(self.goodCalls) + len(self.badCalls))

	def percentBadCallsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentBadCalls()

	def percentGoodPuts(self):

		if len(self.goodPuts) + len(self.badPuts) == 0:
			return 0
		return len(self.goodPuts)/(len(self.goodPuts) + len(self.badPuts))

	def percentGoodPutsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentGoodPuts()

	def percentBadPuts(self):

		if len(self.goodPuts) + len(self.badPuts) == 0:
			return 0
		return len(self.badPuts)/(len(self.goodPuts) + len(self.badPuts))

	def percentBadPutsForStock(self, sym):

		return self.findStockHistoricalFromSym(sym).percentBadPuts()