from Simulation import *
from SimPortfolioControl import *
from ProcessHistoricals import *
from Event import *
import statistics
import sys, os

class IndividualStockHistorical:

	def __init__(self, optionList, sym, simulation):

		self.simulation = simulation
		self.sym = sym
		self.findStockSpecificOptionData(optionList)
		self.options = optionList
		self.goodOptions, self.badOptions = self.seperateOptions()
		self.goodCalls, self.badCalls = self.seperateCalls()
		self.goodPuts, self.badPuts = self.seperatePuts()
		self.totalProfit = self.findTotalProfit(simulation)


	def findStockSpecificOptionData(self, optionList):

		self.optionCounter = {"calls" : 0, "puts": 0, "total": 0}
		self.optionPercentChangesAndTimes = {"calls": {}, "puts": {}};
		self.calls = []
		self.puts = []
		for option in optionList:
			if option.optionType == "call":
				self.calls.append(option)
				self.optionCounter["calls"] += 1;
				self.optionCounter["total"] += 1;
				self.optionPercentChangesAndTimes["calls"][option.purchaseDate + option.purchaseTime] = {"percentChange" : option.finalPercentChange, "sellDate" : option.finalDate, "sellTime" : option.finalTime, "profit" : option.totalProfit}
			else:
				self.puts.append(option)
				self.optionCounter["puts"] += 1;
				self.optionCounter["total"] += 1;
				self.optionPercentChangesAndTimes["puts"][option.purchaseDate + option.purchaseTime] = {"percentChange" : option.finalPercentChange, "sellDate" : option.finalDate, "sellTime" : option.finalTime, "profit" : option.totalProfit}

	# def findHourlyEvents(self, Simulation, sym):

	# 	self.events = []
	# 	self.goodEvents = []
	# 	self.badEvents = []
	# 		makeNewEvent = True;
	# 		for option in Simulation.stockProfile(sym).options:
	# 			if !makeNewEvent:
	# 				if currentEvent.checkIfOptionInEvent(option):
	# 					currentEvent.addOptionToEvent(option)
	# 				else:
	# 					currentEvent.closeEvent()
	# 					self.events.append(currentEvent)
	# 					if currentEvent.percentChange() > 0:
	# 						self.goodEvents.append(currentEvent)
	# 					else:
	# 						self.badEvents.append(currentEvent)
	# 					makeNewEvent = True
	# 			if makeNewEvent:
	# 				currentEvent = Event(Simulation, sym)
	# 				currentEvent.setStart(option)
	# 				makeNewEvent = False
	# 	return [self.events, self.goodEvents, self.badEvents]

	def findEvents(self, Simulation):

		self.events =  EventFinder(Simulation)

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

		return self.optionCounter["calls"]

	def putCount(self):

		return self.optionCounter["puts"]

	def optionCount(self):

		return self.callCount() + self.putCount()

	def findBestAndWorstCall(self):

		bestCall = None
		worstCall = None
		for call in self.calls:
			if worstCall is None or call.finalPercentChange < worstCall.finalPercentChange:
				worstCall = call
			if bestCall is None or call.finalPercentChange> bestCall.finalPercentChange:
				bestCall = call
		return [bestCall, worstCall]

	def findBestAndWorstPut(self):

		bestPut = None
		worstPut = None
		for put in self.puts:
			if worstPut is None or put.finalPercentChange < worstPut.finalPercentChange:
				worstPut = put
			if bestPut is None or put.finalPercentChange > bestPut.finalPercentChange:
				bestPut = put
		return [bestPut, worstPut]

	def findCallPercentIncreases(self):

		callPercentIncreases = []
		for call in self.goodCalls:
			callPercentIncreases.append(call.finalPercentChange)
		return callPercentIncreases

	def findAverageCallPercentIncrease(self):

		return statistics.mean(self.findCallPercentIncreases())

	def findPutPercentIncreases(self):

		putPercentIncreases = [];
		for put in self.goodPuts:
			putPercentIncreases.append(put.finalPercentChange)
		return putPercentIncreases

	def findAveragePutPercentIncrease(self):

		return statistics.mean(self.findPutPercentIncreases())

	def findCallPercentDecreases(self):

		callPercentDecreases = []
		for call in self.badCalls:
			callPercentDecreases.append(call.finalPercentChange)
		return callPercentDecreases

	def findAverageCallPercentDecrease(self):

		return statistics.mean(self.findCallPercentDecreases())

	def findPutPercentDecreases(self):

		putPercentDecreases = []
		for put in self.badPuts:
			findPutPercentDecreases.append(put.finalPercentChange)
		return putPercentDecreases

	def findAveragePutPercentDecrease(self):

		return statistics.mean(self.findPutPercentDecreases())

	def findOptionPercentIncreases(self):

		optionPercentIncreases = []
		for option in self.goodOptions:
			optionPercentIncreases.append(option.finalPercentChange)
		return optionPercentIncreases

	def findAverageOptionPercentIncrease(self):

		return statistics.mean(self.findOptionPercentIncreases())

	def findOptionPercentDecreases(self):

		optionPercentDecreases = []
		for option in self.badOptions:
			optionPercentDecreases.append(option.finalPercentChange)
		return optionPercentDecreases

	def findAverageOptionPercentDecrease(self):

		return statistics.mean(self.findOptionPercentDecreases())

	def findCallPercentChanges(self):

		return self.findCallPercentIncreases() + self.findOptionPercentDecreases()

	def findPutPercentChanges(self):

		return self.findPutPercentIncreases() + self.findPutPercentDecreases()

	def findOptionPercentChanges(self):

		return self.findCallPercentChanges() + self.findPutPercentChanges()

	def findAverageCallPercentChange(self):

		return statistics.mean(self.findCallPercentChanges())

	def findAveragePutPercentChange(self):

		return statistics.mean(self.findPutPercentChanges())

	def findAverageOptionPercentChange(self):

		return statistics.mean(self.findOptionPercentChanges())

	def findCallMoneyIncreases(self):

		callMoneyIncreases = []
		for call in self.goodCalls:
			callMoneyIncreases.append(call.totalProfit())
		return callMoneyIncreases

	def findAverageCallMoneyIncrease(self):

		return statistics.mean(self.findCallMoneyIncreases())

	def findCallMoneyDecreases(self):

		callMoneyDecreases = []
		for call in self.badCalls:
			callMoneyDecreases.append(call.totalProfit())
		return callMoneyDecreases

	def findAverageCallMoneyDecrease(self):

		return statistics.mean(self.findCallMoneyDecreases())

	def findPutMoneyIncreases(self):

		putMoneyIncreases = []
		for put in self.goodPuts:
			putMoneyIncreases.append(put.totalProfit())
		return putMoneyIncreases

	def findAveragePutMoneyIncrease(self):

		return statistics.mean(self.findPutMoneyIncreases())

	def findPutMoneyDecreases(self):

		putMoneyDecreases = []
		for put in self.badPuts:
			putMoneyDecreases.append(put.totalProfit())
		return putMoneyDecreases

	def findAveragePutMoneyIncrease(self):

		return statistics.mean(self.findPutMoneyDecreases())

	def findOptionMoneyIncreases(self):

		optionMoneyIncreases = []
		for option in self.goodOptions:
			optionMoneyIncreases.append(option.totalProfit())
		return optionMoneyIncreases

	def findAverageOptionMoneyIncrease(self):

		return statistics.mean(self.findOptionMoneyIncreases())

	def findOptionMoneyDecreases(self):

		optionMoneyDecreases = []
		for option in self.badOptions:
			optionMoneyDecreases.append(option.totalProfit())
		return optionMoneyDecreases

	def findAverageOptionMoneyDecrease(self):

		return statistics.mean(self.findOptionMoneyDecreases())

	def findCallMoneyChanges(self):

		return self.findCallMoneyIncreases() + self.findCallMoneyDecreases()

	def findAverageCallMoneyChange(self):

		return statistics.mean(self.findCallMoneyChanges())

	def findPutMoneyChanges(self):

		return self.findPutMoneyIncreases() + self.findPutMoneyDecreases()

	def findAveragePutMoneyChange(self):

		return statistics.mean(self.findPutMoneyChanges())

	def findOptionMoneyChanges(self):

		return self.findCallMoneyChanges() + self.findPutMoneyChanges()

	def findAverageOptionMoneyChange(self):

		return statistics.mean(self.findOptionMoneyChanges())

	def writeReport(self):

		print("The stock {2} made a total profit of ${0} starting from an initial investment of ${1}".format(self.totalProfit, self.simulation.portfolio.initialInvestment, self.sym))
		print("a total of {0} options were traded, with {1} of those being calls and {2} being puts".format(self.optionCount(), self.callCount(), self.putCount()))
		print("of the {0} options, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.optionCount(), round(self.percentGoodOptions(), 2), round(self.percentBadOptions(), 2)))
		print("of the {0} calls, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.callCount(), round(self.percentGoodCalls(), 2), round(self.percentBadCalls(), 2)))
		print("of the {0} puts, {1}% of them traded for a profit and {2}% of them traded for a loss".format(self.putCount(), round(self.percentGoodPuts(), 2), round(self.percentBadPuts(), 2)))

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
		plt.title('Stock Portfolio for {0} Value Over Time'.format(self.sym))
		plt.xlabel('Minutes')
		plt.ylabel('{0} Portfolio Value'.format(self.sym))
		plt.show()

	def percentGoodOptions(self):
		if len(self.goodOptions) + len(self.badOptions) == 0:
			return 0
		return len(self.goodOptions)/(len(self.goodOptions) + len(self.badOptions))

	def percentBadOptions(self):
		if len(self.goodOptions) + len(self.badOptions) == 0:
			return 0
		return len(self.badOptions)/(len(self.goodOptions) + len(self.badOptions))

	def percentGoodCalls(self):
		if len(self.goodCalls) + len(self.badCalls) == 0:
			return 0
		return len(self.goodCalls)/(len(self.goodCalls) + len(self.badCalls))

	def percentBadCalls(self):
		if len(self.goodCalls) + len(self.badCalls) == 0:
			return 0
		return len(self.badCalls)/(len(self.goodCalls) + len(self.badCalls))

	def percentGoodPuts(self):
		if len(self.goodPuts) + len(self.badPuts) == 0:
			return 0
		return len(self.goodPuts)/(len(self.goodPuts) + len(self.badPuts))

	def percentBadPuts(self):
		if len(self.goodPuts) + len(self.badPuts) == 0:
			return 0
		return len(self.badPuts)/(len(self.goodPuts) + len(self.badPuts))



		
