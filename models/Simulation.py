import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

file_path = __file__

import json

import Utils.login
from Utils.datetime_funcs import *
from SimPortfolioControl import *
from SimCalendar import *
from Stock import *
from Option import *

import StrategyFuncs
from StrategyFuncs.volumeAnalysis import volumeAnalysis


class Simulation:

	def __init__(self, symbolList, historicalsList, optionHistoricalsList, investment, timeStep, stratFunc, stratParams):

		self.timeStep = timeStep
		self.stratFunc = stratFunc
		self.stratParams = stratParams
		self.dateList = self.createDateList(historicalsList[0])
		self.calendar = SimCalendar(self.dateList, self.timeStep)
		self.currentDate = self.calendar.currentDate
		self.currentTime = self.calendar.currentTime

		self.portfolio = SimPortfolioControl(symbolList, historicalsList, optionHistoricalsList, investment, self.currentDate, self.currentTime)
		
	
		self.persistentVariables = {}

	def createDateList(self, sampleHistoricals):

		return [date for date in list(sampleHistoricals.keys())]

	def getNextPoint(self):

		dateInfo = self.calendar.getNextPoint()
		if dateInfo:
			[date, time] = dateInfo
			print(date, time)
			self.currentDate, self.currentTime = date, time
			self.updatePortfolio()
		else:
			print("Simulation Finished!")

	def runSimulation(self):

		while not self.calendar.finished:
			
			self.stratFunc(*self.stratParams, self)
			
			self.getNextPoint()


			

			





	def updatePortfolio(self):

		self.portfolio.updateTime(self.currentDate, self.currentTime)


def get_stock_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(stock_json_filename(symbol))

def stock_json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return os.path.dirname(os.path.dirname(os.path.realpath(file_path))) + "/stocks/stockJSON/" + symbol + ".json"

def get_option_json_object(symbol):
	"""Returns the json object from the associated json file of name SYMBOL.json"""
	return read_json(option_json_filename(symbol))

def option_json_filename(symbol):
	"""Appends .json to the string SYMBOL"""
	return os.path.dirname(os.path.dirname(os.path.realpath(file_path))) + "/options/optionJSON/" + symbol + ".json"

def read_json(filename):
	"""FILENAME is the name of a json file containing option information. This function loads the json object into the script 
	to be edited. The return object is the option dictionary to be edited."""

	data_file = open(filename, "r")
	data = json.load(data_file)
	data_file.close()

	return data
