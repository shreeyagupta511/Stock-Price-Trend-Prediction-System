import numpy as np


# ---------------- LINEAR REGRESSION ----------------
def linear_method(x, y):

    coeff = np.polyfit(x, y, 1)
    slope = coeff[0]
    intercept = coeff[1]

    y_pred = slope * x + intercept
    next_x = x[-1] + 1
    next_price = slope * next_x + intercept

    # Errors
    mae = np.mean(np.abs(y - y_pred))
    mre = np.mean(np.abs((y - y_pred) / y)) * 100

    return y_pred, next_price, slope, mae, mre


# ---------------- NUMERICAL DIFFERENTIATION ----------------
def numerical_differentiation(y):

    dy = np.gradient(y)
    avg_rate = np.mean(dy)

    return dy, avg_rate


# ---------------- EULER METHOD ----------------
def euler_method(y):

    dy = np.gradient(y)
    avg_rate = np.mean(dy)

    next_value = y[-1] + avg_rate

    # Estimate Euler fitted values
    y_euler_pred = y[:-1] + avg_rate

    mae = np.mean(np.abs(y[1:] - y_euler_pred))
    mre = np.mean(np.abs((y[1:] - y_euler_pred) / y[1:])) * 100

    return next_value, mae, mre


# ---------------- INTERPOLATION (POLYNOMIAL DEGREE 2) ----------------

def interpolation_method(x, y):

    # Fit polynomial of degree 2
    coeffs = np.polyfit(x, y, 2)

    # Create polynomial function
    poly = np.poly1d(coeffs)

    # Predicted values for existing x
    y_pred = poly(x)

    # Predict next value
    next_x = x[-1] + 1
    next_value = poly(next_x)

    # Errors
    mae = np.mean(np.abs(y - y_pred))
    mre = np.mean(np.abs((y - y_pred) / y)) * 100

    return y_pred, next_value, mae, mre