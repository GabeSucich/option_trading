import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import numpy as np
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier

from Stocks.stockhistoricals import *
from Models.Stocks.StockHistory import *
from Models.MetricLoggers.InterdayMetrics import *
from Models.EventLoggers.InterdayChanges import *

import Utils.jsonHelper as jh
root = '/Users/gabrielsucich/Desktop/option_trading/'
tracked_stocks_JSON = jh.readJSON(root + "stocks/stockJSON/tracked_stocks.json")
tracked_stocks = list(tracked_stocks_JSON.keys())

nonconsecutive_model_parameters = {
	"baseline_threshold": .5,
	"model_threshold": .65,
	"drop_threshold": .5,
	"granularity": "quartile",
	"volumeRecordLength": 2,
	"pressureRecordLength": 3,
	"priceRecordLength": 3,
	"interdayRecordLength": 4
}

consecutive_model_parameters = {
	"baseline_threshold": .6,
	"model_threshold": .65,
	"drop_threshold": .5,
	"granularity": "quartile",
	"volumeRecordLength": 3,
	"pressureRecordLength": 3,
	"priceRecordLength": 3,
	"interdayRecordLength": 4
}

class InterdayDropPredictor:

	def __init__(self, date_list, nonconsecutive_model_params = nonconsecutive_model_parameters, consecutive_model_params = consecutive_model_parameters):

		self.nonconsecutive_baseline_threshold, self.nonconsecutive_model_threshold, self.nonconsecutive_drop_threshold = nonconsecutive_model_params["baseline_threshold"], nonconsecutive_model_params["model_threshold"], nonconsecutive_model_params["drop_threshold"]
		self.consecutive_baseline_threshold, self.consecutive_model_threshold, self.consecutive_drop_threshold = consecutive_model_params["baseline_threshold"], consecutive_model_params["model_threshold"], consecutive_model_params["drop_threshold"]

		self.nonconsecutive_granularity, self.nonconsecutive_volumeRecordLength, self.nonconsecutive_pressureRecordLength, self.nonconsecutive_priceRecordLength, self.nonconsecutive_interdayRecordLength = nonconsecutive_model_params["granularity"], nonconsecutive_model_params["volumeRecordLength"], nonconsecutive_model_params["pressureRecordLength"], nonconsecutive_model_params["priceRecordLength"], nonconsecutive_model_params["interdayRecordLength"]
		self.consecutive_granularity, self.consecutive_volumeRecordLength, self.consecutive_pressureRecordLength, self.consecutive_priceRecordLength, self.consecutive_interdayRecordLength = consecutive_model_params["granularity"], consecutive_model_params["volumeRecordLength"], consecutive_model_params["pressureRecordLength"], consecutive_model_params["priceRecordLength"], consecutive_model_params["interdayRecordLength"]

		self.date_list = date_list
		self.date_list.sort()

		self.nonconsecutive_training_data, self.consecutive_training_data = self.import_training_data()

		# self.nonconsecutive_stock_histories, self.nonconsecutive_metrics, self.nonconsecutive_interday_changes = self.create_nonconsecutive_histories_metrics_and_changes()
		self.consecutive_stock_histories, self.consecutive_metrics, self.consecutive_interday_changes = self.create_consecutive_histories_metrics_and_changes()

		# self.nonconsecutive_prediction_matrix = self.create_nonconsecutive_prediction_matrix()
		self.consecutive_prediction_matrix = self.create_consecutive_prediction_matrix()

		self.predictions = self.make_predictions()

	def import_training_data(self):

		nonconsecutive_data, consecutive_data = import_optimal_training_data()
	
		return nonconsecutive_data[nonconsecutive_data["Date"] < self.date_list[0]], consecutive_data[consecutive_data["Date"] < self.date_list[0]]

	def create_nonconsecutive_histories_metrics_and_changes(self):

		histories = {}
		interday_changes = {}
		metrics = {}

		for symbol in tracked_stocks:
			stock_history = RealTimeStockHistory(symbol, self.nonconsecutive_granularity, self.date_list)
			histories[symbol] = stock_history
			interday_changes[symbol] = InterdayChanges(stock_history)
			metrics[symbol] = InterdayMetrics(stock_history, self.nonconsecutive_volumeRecordLength, self.nonconsecutive_pressureRecordLength, self.nonconsecutive_priceRecordLength, self.nonconsecutive_interdayRecordLength)

		return histories, metrics, interday_changes

	def create_consecutive_histories_metrics_and_changes(self):

		histories = {}
		interday_changes = {}
		metrics = {}

		for symbol in tracked_stocks:
			stock_history = RealTimeStockHistory(symbol, self.consecutive_granularity, self.date_list)
			histories[symbol] = stock_history
			interday_changes[symbol] = InterdayChanges(stock_history)
			metrics[symbol] = InterdayMetrics(stock_history, self.consecutive_volumeRecordLength, self.consecutive_pressureRecordLength, self.consecutive_priceRecordLength, self.consecutive_interdayRecordLength)

		return histories, metrics, interday_changes
	

	def create_nonconsecutive_prediction_matrix(self):

		prediction_matrix = pd.DataFrame(columns = ["Date", "Symbol", "Volume Gradient", "Volume Concavity", "Price Gradient", 
													"Price Concavity", "Buy Pressure Mean", "Buy Pressure Gradient", "Buy Pressure Concavity",
													"Interday Mean", "Interday Gradient", "Interday Concavity", "Consecutive Interday Drops",
													"Consecutive Interday Jumps", "Prev Day Change (%)"])
		
		for date in self.date_list:
			for symbol in tracked_stocks:
				stock_interday_changes = self.nonconsecutive_interday_changes[symbol]
				stock_interday_metrics = self.nonconsecutive_metrics[symbol]
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

	def create_consecutive_prediction_matrix(self):

		prediction_matrix = pd.DataFrame(columns = ["Date", "Symbol", "Volume Gradient", "Volume Concavity", "Price Gradient", 
													"Price Concavity", "Buy Pressure Mean", "Buy Pressure Gradient", "Buy Pressure Concavity",
													"Interday Mean", "Interday Gradient", "Interday Concavity"
													# , "Consecutive Interday Drops", "Consecutive Interday Jumps", "Prev Day Change (%)"
													])
		
		for date in self.date_list:
			for symbol in tracked_stocks:
				stock_interday_changes = self.consecutive_interday_changes[symbol]
				stock_interday_metrics = self.consecutive_metrics[symbol]
				prediction_matrix.loc[prediction_matrix.shape[0]] = [date, symbol, stock_interday_metrics.lastVolumeMetric(date)["gradient"], 
												stock_interday_metrics.lastVolumeMetric(date)["concavity"],
												stock_interday_metrics.lastPriceMetric(date)["gradient"],
												stock_interday_metrics.lastPriceMetric(date)["concavity"],
												stock_interday_metrics.lastPressureMetric(date)["mean"],
												stock_interday_metrics.lastPressureMetric(date)["gradient"],
												stock_interday_metrics.lastPressureMetric(date)["concavity"],
												stock_interday_metrics.interdayMetric(date)["mean"],
												stock_interday_metrics.interdayMetric(date)["gradient"],
												stock_interday_metrics.interdayMetric(date)["concavity"]
												# stock_interday_metrics.interdayMetric(date)["consecutiveDecreases"],
												# stock_interday_metrics.interdayMetric(date)["consecutiveIncreases"],
												# stock_interday_changes.getInterdayChanges()[date]["prev_day_change"]
												]

		prediction_matrix = prediction_matrix.set_index("Symbol")

		return prediction_matrix


	def create_nonconsecutive_model(self):

		model = TwofoldModel(self.nonconsecutive_baseline_threshold)

		training_X, training_y = find_nonconsecutive_drops(self.nonconsecutive_training_data, self.nonconsecutive_drop_threshold)

		model.fit(training_X, training_y.iloc[:, 0])
		model.fit_baseline(training_X, training_y.iloc[:, 1])
	
		return model

	def create_consecutive_model(self):

		model = TwofoldModel(self.consecutive_baseline_threshold)

		training_X, training_y = find_drops(self.consecutive_training_data, self.consecutive_drop_threshold)

		model.fit(training_X, training_y.iloc[:, 0])
		model.fit_baseline(training_X, training_y.iloc[:, 1])
	
		return model


	def make_predictions(self):

		predictions = {}

		for date in self.date_list:

			predictions[date] = {}

			for i in range(5):

				date_predictions = self.make_predictions_for_date(date)

				for symbol, probability in date_predictions.items():

					if symbol in predictions[date]:
						predictions[date][symbol].append(probability)

					else:
						predictions[date][symbol] = [probability]


		return predictions


	def make_predictions_for_date(self, date):

		# self.nonconsecutive_model = self.create_nonconsecutive_model()
		self.consecutive_model = self.create_consecutive_model()

		# nonconsecutive_X = self.nonconsecutive_prediction_matrix[self.nonconsecutive_prediction_matrix["Date"] == date].drop(columns = "Date")
		consecutive_X = self.consecutive_prediction_matrix[self.consecutive_prediction_matrix["Date"] == date].drop(columns = "Date")

		# nonconsecutive_predictions, nonconsecutive_probabilities = model_predictions(self.nonconsecutive_model, nonconsecutive_X, threshold = self.nonconsecutive_model_threshold)
		consecutive_predictions, consecutive_probabilities = model_predictions(self.consecutive_model, consecutive_X, threshold = self.consecutive_model_threshold)

		# pred_dct = dict(sorted(zip(nonconsecutive_X[nonconsecutive_predictions].index, nonconsecutive_probabilities[nonconsecutive_predictions]), key = lambda x: x[1], reverse = True))
		pred_dct = {}
		pred_dct.update(dict(sorted(zip(consecutive_X.index[consecutive_predictions], consecutive_probabilities[consecutive_predictions]), key = lambda x: x[1], reverse = True)))

		return pred_dct

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

def evaluate_single_prediction(symbol, prediction_date, drop_threshold):

	historicals = jh.loadStockHistoricals(symbol)
	stockDay1 = None
	stockDay2 = None

	for date, priceData in historicals.items():

		if stockDay1 and stockDay2:

			break

		elif date == prediction_date:

			stockDay1 = StockDay(date, priceData)

		elif stockDay1:

			stockDay2 = StockDay(date, priceData)


	if openClosePercentChange(stockDay1, stockDay2) <= -drop_threshold:

		return True

	return False

def evaluate_all_predictions(predictions, drop_threshold):

	evaluations = {}

	for date, date_predictions in predictions.items():

		evaluations[date] = {}

		for symbol in date_predictions.keys():

			evaluations[date][symbol] = evaluate_single_prediction(symbol, date, drop_threshold)

	return evaluations



"""Functions which dictate modeling."""

def create_random_forest(seed = None):
    
    if not seed:
        seed = random.randint(0, 50)
    
    return RandomForestClassifier(class_weight = "balanced", random_state=seed, n_estimators = 100)

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
    
    nonconsecutive_data = pd.read_csv("OptimalTrainingDataNonconsecutive.csv")
    consecutive_data = pd.read_csv("OptimalTrainingDataConsecutive.csv")
    nonconsecutive_data = nonconsecutive_data.drop(columns = "Unnamed: 0")
    consecutive_data = consecutive_data.drop(columns = "Unnamed: 0")

    nonconsecutive_data = remove_nonconsecutive_dates(nonconsecutive_data)
    consecutive_data = remove_nonconsecutive_dates(consecutive_data)
    
    return nonconsecutive_data, consecutive_data

def find_drops(data, drop_threshold):
    
    data = data.copy()
    data["Is Drop"] = data["Next Day Change (%)"] <= -drop_threshold
    data["Is Decrease"] = data["Next Day Change (%)"] < 0
    
    return data.loc[:, "Volume Gradient": 'Interday Concavity'], data[["Is Drop","Is Decrease"]]

def find_nonconsecutive_drops(data, drop_threshold):
    
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
        