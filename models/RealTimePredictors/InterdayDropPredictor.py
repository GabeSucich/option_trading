import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import numpy as np
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier

from stocks.stockhistoricals import *
from Models.Stocks.StockHistory import *
from Models.MetricLoggers.InterdayMetrics import *
from Models.EventLoggers.InterdayChanges import *

import Utils.jsonHelper as jh
root = '/Users/gabrielsucich/Desktop/option_trading/'
tracked_stocks_JSON = jh.readJSON(root + "stocks/stockJSON/tracked_stocks.json")
tracked_stocks = list(tracked_stocks_JSON.keys())

class InterdayDropPredictor:

	def __init__(self, date_list, granularity, volumeRecordLength, pressureRecordLength, priceRecordLength, interdayRecordLength):


		self.granularity, self.volumeRecordLength, self.pressureRecordLength, self.priceRecordLength, self.interdayRecordLength = granularity, volumeRecordLength, pressureRecordLength, priceRecordLength, interdayRecordLength
		self.date_list = date_list
		self.date_list.sort()

		self.training_data = self.import_training_data()
		
		self.model = self.create_model()

		self.stock_histories, self.metrics, self.interday_changes = self.create_histories_metrics_and_changes()
		
		self.prediction_matrix = self.create_prediction_matrix()
		self.predictions = self.make_predictions()

	def import_training_data(self):

		full_data = import_optimal_training_data()
	
		return full_data[full_data["Date"] < self.date_list[0]]

	def create_histories_metrics_and_changes(self):

		histories = {}
		interday_changes = {}
		metrics = {}

		for symbol in tracked_stocks:
			stock_history = RealTimeStockHistory(symbol, self.granularity, self.date_list)
			histories[symbol] = stock_history
			interday_changes[symbol] = InterdayChanges(stock_history)
			metrics[symbol] = InterdayMetrics(stock_history, self.volumeRecordLength, self.pressureRecordLength, self.priceRecordLength, self.interdayRecordLength)

		return histories, metrics, interday_changes
	

	def create_prediction_matrix(self):

		prediction_matrix = pd.DataFrame(columns = ["Date", "Symbol", "Volume Gradient", "Volume Concavity", "Price Gradient", 
													"Price Concavity", "Buy Pressure Mean", "Buy Pressure Gradient", "Buy Pressure Concavity",
													"Interday Mean", "Interday Gradient", "Interday Concavity", "Consecutive Interday Drops",
													"Consecutive Interday Jumps", "Prev Day Change (%)"])
		
		for date in self.date_list:
			for symbol in tracked_stocks:
				stock_interday_changes = self.interday_changes[symbol]
				stock_interday_metrics = self.metrics[symbol]
				prediction_matrix.loc[prediction_matrix.shape[0]] = [date, symbol, stock_interday_metrics.lastVolumeMetric(date)["gradient"], 
												stock_interday_metrics.lastVolumeMetric(date)["concavity"],
												stock_interday_metrics.lastPriceMetric(date)["gradient"],
												stock_interday_metrics.lastPriceMetric(date)["concavity"],
												stock_interday_metrics.lastPressureMetric(date)["mean"],
												stock_interday_metrics.lastPressureMetric(date)["gradient"],
												stock_interday_metrics.lastPressureMetric(date)["concavity"],
												stock_interday_metrics.interdayMetric(date)["mean"],
												stock_interday_metrics.interdayMetric(date)["gradient"],
												stock_interday_metrics.interdayMetric(date)["concavity"],
												stock_interday_metrics.interdayMetric(date)["consecutiveDecreases"],
												stock_interday_metrics.interdayMetric(date)["consecutiveIncreases"],
												stock_interday_changes.getInterdayChanges()[date]["prev_day_change"]
												]

		prediction_matrix = prediction_matrix.set_index("Symbol")

		return prediction_matrix


	def create_model(self):

		model = TwofoldModel(.5)

		training_X, training_y = find_drops(self.training_data, 1)

		model.fit(training_X, training_y.iloc[:, 0])
		model.fit_baseline(training_X, training_y.iloc[:, 1])
	
		return model


	def make_predictions(self):

		predictions = {}

		for date in self.date_list:

			date_predictions = self.make_predictions_for_date(date)
			predictions[date] = date_predictions

		return predictions


	def make_predictions_for_date(self, date):

		X = self.prediction_matrix[self.prediction_matrix["Date"] == date].drop(columns = "Date")
		predictions = model_predictions(self.model, X, threshold = .5), probabilities

		return dict(sorted(zip(X[predictions].index, probabilities[predictions]), key = lambda x: x[1], reverse = True))

	def get_predictions(self):
		return self.predictions

	def find_predate_data(self, training_data):

		return training_data[training_data["Date"] < self.date]



"""Functions to store predictions for future reference"""

def store_predictions(date, predictions):

	filename = root + "Models/RealTimePredictors/predictions.json"
	predictions = jh.readJSON(filename)
	predictions[date] = {}
	for symbol in tracked_stocks:
		predictions[date][symbol] = symbol in predictions

	jh.dumpJSON(predictions, filename)

"""Functions which dictate modeling."""

def create_random_forest(seed = None):
    
    if not seed:
        seed = random.randint(0, 50)
    
    return RandomForestClassifier(class_weight = "balanced", random_state=seed, n_estimators = 50)

def model_predictions(model, X, threshold):
    
    probabilities = model.predict_proba(X)[:, 1]
    return probabilities > threshold, probabilities

class TwofoldModel:
    
    def __init__(self, baseline_threshold):
        self.baseline_threshold = baseline_threshold
        self.primary_model = create_random_forest()
        self.baseline_model = create_random_forest()
        
    def fit(self, X, y):
        self.primary_model.fit(X, y)
        
    def fit_baseline(self, X, y):
        self.baseline_model.fit(X, y)
    
    def predict(self, X):
        
        return self.primary_model.predict(X)*self.baseline_model.predict(X)
    
    def predict_proba(self, X):
        
        raw_predictions = self.primary_model.predict_proba(X)
        auxiliary_predictions = self.baseline_model.predict_proba(X)

        for i in range(X.shape[0]):
            if auxiliary_predictions[i, 1] < self.baseline_threshold:
                raw_predictions[i, 0] = 1
                raw_predictions[i, 1] = 0
        
        return raw_predictions
        
	

"""Helper functions for loading data"""

def import_optimal_training_data():
    
    data = pd.read_csv("OptimalTrainingData.csv")
    data = data.drop(columns = "Unnamed: 0")
    data = remove_nonconsecutive_dates(data)
    return data

def find_drops(data, drop_threshold):
    
    data = data.copy()
    data["Is Drop"] = data["Next Day Change (%)"] <= -drop_threshold
    data["Is Decrease"] = data["Next Day Change (%)"] < 0
    
    return data.loc[:, "Volume Gradient": 'Prev Day Change (%)'], data[["Is Drop","Is Decrease"]]

def find_nonconsecutive_drop(data, drop_threshold):
    
    data = data.copy()
    data["Is Drop"] = (data["Next Day Change (%)"] <= -drop_threshold)&(data["Prev Day Change (%)"] > 0)
    data["Is Decrease"] = data["Next Day Change (%)"] < 0
    
    return data.loc[:, "Volume Gradient": 'Prev Day Change (%)'], data[["Is Drop","Is Decrease"]]

def find_predate_data(data, date):

		return data[data["Date"] < date]

def remove_nonconsecutive_dates(data):
    
    dates = list(data.query("Symbol == 'AAPL'")["Date"])
    dates_to_keep = []
    
    for i, date in enumerate(dates[:-1]):
        next_date = dates[i + 1]
        if days_between(date, next_date) == 1:
            dates_to_keep.append(date)
    
    return data[data["Date"].isin(dates_to_keep)]
        