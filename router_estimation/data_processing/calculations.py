import numpy as np
from scipy.optimize import minimize
import math


def mse(x, locations, distances, weights):
    mserror = 0.0
    num_data = 0
    for location, distance, weight in zip(locations, distances, weights):
        distance_calculated = great_circle_distance(x[0], x[1], location[0], location[1])
        mserror += weight*math.pow(distance_calculated - distance, 2.0)
        num_data += weight
    return mserror/num_data


def great_circle_distance(lon1, lat1, lon2, lat2):
    """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)

        All args must be of equal length.

        returns meters
        """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km * 1000


def get_coordinates(locations, distances, weights):
    initial_location = np.array((0.0, 0.0))
    result = minimize(
        mse,                         # The error function
        initial_location,            # The initial guess
        args=(locations, distances, weights), # Additional parameters for mse
        method='Nelder-Mead',           # The optimisation algorithm
        options={
            'ftol':1e-6,         # Tolerance
            'maxiter': 1e+5      # Maximum iterations
        })
    location = result.x
    return location


def euc_dist(lat1, lon1, lat2, lon2):
    return math.sqrt(pow(lon1-lon2, 2) + pow(lat1 - lat2, 2))


def get_dist(freq, signal):
    exp = (27.55 - (20 * np.log10(freq)) + np.abs(signal)) / 20.0  # path loss model for wifi
    dist = 10**exp
    return dist
