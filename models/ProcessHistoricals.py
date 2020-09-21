from Simulation import *
from SimPortfolioControl import *
from StockHistoricals import *
import statistics
import sys, os

class ProcessHistoricals:

	def __init__(self, Simulation):

		self.findOptionDataForEachStock(Simulation)
		# self.putsSold, self.putPercentChanges = findPutPercentChanges(ranSimulation);
		# self.averageCallPercentChange = statistics.mean(self.callPercentChanges);
		# self.averagePutPercentChange = statistics.mean(self.putPercentChanges);
		# self.overallPercentChange = findOverallPercentChange(ranSimulation);
		# self.optionsSold = self.callsSold + self.putsSold;
		# self.greatestCallPercentIncrease = max(self.callPercentChanges);
		# self.greatestPutPercentIncrease = max(self.putPercentChanges);
		# self.greatestCallPercentDecrease = min(self.callPercentChanges);
		# self.greatestPutPercentDecrease = min(self.putPercentChanges);
		# writeReport(self)

	def findOptionDataForEachStock(self, Simulation):

		self.stockSpecificOptions = {}
		self.options = []
		for sym in list(Simulation.portfolio.stockPortfolios.keys()):
			self.stockSpecificOptions[sym] = StockHistoricals(Simulation.stockProfile(sym).options)
			self.options.append(StockHistoricals(Simulation.stockProfile(sym).options))


	def seperateOptions(self):

		goodOptions = []
		badOptions = []
		for option in self.options:
			if option.finalPercentChange() > 0:
				goodOptions.append(option)
			else:
				badOptions.append(option)
		return [goodOptions, badOptions]

	def seperateCalls(self):

		goodCalls = [];
		badCalls = [];
		for call in self.calls:
			if call.finalPercentChange() > 0:
				goodCalls.append(call)
			else:
				badCalls.append(call)
		return [goodCalls, badCalls]

	def seperatePuts(self):

		goodPuts = [];
		badPuts = [];
		for put in self.puts:
			if put.finalPercentChange() > 0:
				goodPuts.append(put)
			else:
				badPuts.append(put)
		return [goodPuts, badPuts]

