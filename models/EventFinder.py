from Simulation import *
from SimPortfolioControl import *
from ProcessHistoricals import *
from IndividualStockHistorical import *
import statistics
import sys, os

class EventFinder:

	def __init__(self, Simulation, sym):

		self.morningChaos = self.findMorningChaos(Simulation, sym)

	def findMorningChaos(self, Simulation, sym):

		previousDayData = None
		chaosEvents = []
		for date in list(Simulation.stockProfile(sym).stock.historicals.keys()):
			for time in list(Simulation.stockProfile(sym).stock.historicals[date].keys()):
				data = Simulation.stockProfile(sym).stock.historicals[date][time]
				if time == "1255":
					previousDayDate = date
					previousDayTime = time
					previousDayData = data
				if int(time) >= 630 and int(time) <= 700:
					if previousDayData is not None:
						overnightPercentChange = self.percentChange(previousDayData["close_price"], data["open_price"])
					if previousDayData is not None and abs(overnightPercentChange) >= 3:
						print("Found a morning chaos event from {0} at {1} to {2} at {3}. There was a percent change of {4}%".format(previousDayDate, previousDayTime, date, time, round(overnightPercentChange, 2)))
						chaosEvents.append({"start": previousDayData, "end": data})
						previousDayData = None
		return chaosEvents

	def percentChange(self, prevValue, nextValue):

		return ((prevValue - nextValue)/prevValue)*100
