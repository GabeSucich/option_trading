from sklearn.linear_model import LinearRegression
import numpy as np

def find_average(values):

	return np.mean(values)

def fit_linear_model(values):

	model = LinearRegression()
	xs = np.arange(0, len(values), 1).reshape(-1, 1)
	ys = np.array(values)
	model.fit(xs, ys)
	return model.coef_[0], model.intercept_

def fit_quadratic_model(values):

	model = LinearRegression()
	xs = np.zeros((len(values), 2))
	xs[:, 0] = np.arange(0, len(values))
	xs[:, 1] = xs[:, 0]**2
	ys = np.array(values)
	model.fit(xs, ys)
	return model.coef_[1], model.coef_[0], model.intercept_

def fit_cubic_model(values):

	model = LinearRegression()
	xs = np.zeros((len(values), 3))
	xs[:, 0] = np.arange(0, len(values))
	xs[:, 1] = xs[:, 0]**2
	xs[:, 2] = xs[:, 0]**3
	ys = np.array(values)
	model.fit(xs, ys)
	return model.coef_[2], model.coef_[1], model.coef_[0], model.intercept_