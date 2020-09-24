import matplotlib.pyplot as plt
import statistics
import sys, os
from Simulation import *
from SimPortfolioControl import *
from IndividualStockHistorical import *
sys.path.insert(1, "../Utils/datetime_funcs.py")
# from datetime_funcs import time_between

class Event:

	def __init__(self, Simulation, sym):

		self.Simulation = Simulation
		self.timeLeft = 100
		self.eventOptions = []

	def setStart(self, option):

		self.eventStartDate = option.purchaseDate
		self.eventStartTime = option.purchaseTime
		self.eventOptions.append(option)
		self.previousOption = option

	def checkIfOptionInEvent(self, option):

		if self.previousOption.purchaseDate == option.purchaseDate:
			if self.timeLeft - time_between(self.previousOption.purchaseTime, option.purchaseTime) >= 0:
				return True
		else:
			if self.timeLeft - time_between(self.previousOption.purchaseTime, 1300) - time_between(630, option.purchaseTime) >= 0:
				return True
		return False

	def addOptionToEvent(self, option):

		if self.previousOption.purchaseDate == option.purchaseDate:
			self.timeLeft -= time_between(self.previousOption.purchaseTime, option.purchaseTime)
		else:
			self.timeLeft - time_between(self.previousOption.purchaseTime, 1300) - time_between(630, option.purchaseTime)
		assert self.timeLeft >= 0, "Error, option that was not part of this event was added to this event"
		self.eventOptions.append(option)
		self.previousOption = option

	def closeEvent(self):

		self.eventEndDate = self.previousOption.purchaseDate
		self.eventEndTime = self.previousOption.purchaseTime
		self.percentChange = ((self.valueAtEventEnd(self.eventEndDate, self.eventEndTime, self.Simulation, self.sym) - self.valueAtEventStart(self.eventStartDate, self.eventStartTime, self.Simulation, self.sym)) / self.valueAtEventStart(self.eventStartDate, self.eventStartTime, self.Simulation, self.sym)) * 100

	def valueAtEventEnd(self, endDate, endTime, Simulation, sym):

		Simulation.portfolio.stockPortfolio(sym).historicals


