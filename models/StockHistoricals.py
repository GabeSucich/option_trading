from Simulation import *
from SimPortfolioControl import *
from ProcessHistoricals import *
import statistics
import sys, os

class StockHistoricals:

	def __init__(self, optionList):

		self.findStockSpecificOptionData(optionList)
		self.options = optionList
		self.puts = self.optionPercentChangesAndTimes["puts"]
		self.calls = self.optionPercentChangesAndTimes["calls"]
		self.goodOptions, self.badOptions = self.seperateOptions()
		self.goodCalls, self.badCalls = self.seperateCalls()
		self.goodPuts, self.badPuts = self.seperatePuts()


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
				self.puts.append(puts)
				self.optionCounter["puts"] += 1;
				self.optionCounter["total"] += 1;
				self.optionPercentChangesAndTimes["puts"][option.purchaseDate + option.purchaseTime] = {"percentChange" : option.finalPercentChange, "sellDate" : option.finalDate, "sellTime" : option.finalTime, "profit" : option.totalProfit}


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
			if worstCall is None or call.finalPercentChange() < worstCall.finalPercentChange():
				worstCall = call
			if bestCall is None or call.finalPercentChange() > bestCall.finalPercentChange():
				bestCall = call
		return [bestCall, worstCall]

	def findBestAndWorstPut(self):

		bestPut = None
		worstPut = None
		for put in self.puts:
			if worstPut is None or put.finalPercentChange() < worstPut.finalPercentChange():
				worstPut = put
			if bestPut is None or put.finalPercentChange() > bestPut.finalPercentChange():
				bestPut = put
		return [bestPut, worstPut]

	def findCallPercentIncreases(self):

		callPercentIncreases = []
		for call in self.goodCalls:
			callPercentIncreases.append(call.finalPercentChange())
		return callPercentIncreases

	def findAverageCallPercentIncrease(self):

		return statistics.mean(self.findCallPercentIncreases())

	def findPutPercentIncreases(self):

		putPercentIncreases = [];
		for put in self.goodPuts:
			putPercentIncreases.append(put.finalPercentChange())
		return putPercentIncreases

	def findAveragePutPercentIncrease(self):

		return statistics.mean(self.findPutPercentIncreases())

	def findCallPercentDecreases(self):

		callPercentDecreases = []
		for call in self.badCalls:
			callPercentDecreases.append(call.finalPercentChange())
		return callPercentDecreases

	def findAverageCallPercentDecrease(self):

		return statistics.mean(self.findCallPercentDecreases())

	def findPutPercentDecreases(self):

		putPercentDecreases = []
		for put in self.badPuts:
			findPutPercentDecreases.append(put.finalPercentChange())
		return putPercentDecreases

	def findAveragePutPercentDecrease(self):

		return statistics.mean(self.findPutPercentDecreases())

	def findOptionPercentIncreases(self):

		optionPercentIncreases = []
		for option in self.goodOptions:
			optionPercentIncreases.append(option.finalPercentChange())
		return optionPercentIncreases

	def findAverageOptionPercentIncrease(self):

		return statistics.mean(self.findOptionPercentIncreases())

	def findOptionPercentDecreases(self):

		optionPercentDecreases = []
		for option in self.badOptions:
			optionPercentDecreases.append(option.finalPercentChange())
		return optionPercentDecreases

	def findAverageOptionPercentDecrease(self):

		return statistics.mean(self.findOptionPercentDecreases())

	def findCallPercentChanges(self):

		return self.findCallPercentIncreases().append(self.findOptionPercentDecreases())

	def findPutPercentChanges(self):

		return self.findPutPercentIncreases().append(self.findPutPercentDecreases())

	def findOptionPercentChanges(self):

		return self.findCallPercentChanges().append(self.findPutPercentChanges())

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

		return self.findCallMoneyIncreases().append(self.findCallMoneyDecreases())

	def findAverageCallMoneyChange(self):

		return statistics.mean(self.findCallMoneyChanges())

	def findPutMoneyChanges(self):

		return self.findPutMoneyIncreases().append(self.findPutMoneyDecreases())

	def findAveragePutMoneyChange(self):

		return statistics.mean(self.findPutMoneyChanges())

	def findOptionMoneyChanges(self):

		return self.findCallMoneyChanges().append(self.findPutMoneyChanges())

	def findAverageOptionMoneyChange(self):

		return statistics.mean(self.findOptionMoneyChanges())





		
