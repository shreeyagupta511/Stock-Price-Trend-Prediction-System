from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from stock_data import get_stock_data
from stock_list import search_stock
from datetime import datetime

from methods import (
    linear_method,
    numerical_differentiation,
    euler_method,
    interpolation_method   # ✅ NEW
)

from graph_utils import (
    linear_dashboard,
    diff_dashboard,
    euler_dashboard,
    interpolation_dashboard   # ✅ NEW
)

app = Flask(__name__)


# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return render_template('web.html')


# ---------------- INDEX PAGE ----------------
@app.route('/index')
def index():
    return render_template('index.html')


# ---------------- INPUT PAGE ----------------
@app.route('/input')
def input_page():
    return render_template('input.html')


# ---------------- ABOUT PAGE ----------------
@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- CONTACT PAGE ----------------
@app.route('/contact')
def contact():
    return render_template('contact.html')

# --------------- SEARCH STOCK ------------------------
@app.route("/search-stock")
def search_stock_route():

    keyword = request.args.get("q", "")

    market = request.args.get("market", "global")

    results = search_stock(keyword, market)

    return jsonify(results)

# ---------------- FILE UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():

    symbol = request.form.get("symbol")
    df = get_stock_data(symbol)
    if df.empty:
        return "Invalid stock symbol or no data found"
    current_price = round(df['Close'].iloc[-1], 2)
    today = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # Detect close column
    close_col = None
    for col in df.columns:
        if "close" in col:
            close_col = col
            break

    if close_col is None:
        return "Close column not found in dataset"

    # Remove NaN values
    y = df[close_col].dropna().values
    x = np.arange(len(y))
    
    current_price = round(df[close_col].iloc[-1], 2)


    # -------- LINEAR REGRESSION --------
    y_pred, next_linear, slope, mae1, mre1 = linear_method(x, y)


    # -------- DIFFERENTIATION --------
    dy, avg_rate = numerical_differentiation(y)

    volatility = np.std(dy)

    if volatility < 1000:
        volatility_msg = "Low Volatility"
    elif volatility < 3000:
        volatility_msg = "Moderate Volatility"
    else:
        volatility_msg = "High Volatility"


    # -------- EULER --------
    euler_next, mae2, mre2 = euler_method(y)


    # -------- INTERPOLATION --------
    y_interp, interp_next, mae3, mre3 = interpolation_method(x, y)


    # -------- BEST METHOD --------
    mae_values = {
        "Linear Regression": mae1,
        "Euler Method": mae2,
        "Interpolation": mae3
    }

    best_method = min(mae_values, key=mae_values.get)

    if best_method == "Linear Regression":
        best_prediction = next_linear
    elif best_method == "Euler Method":
        best_prediction = euler_next
    else:
        best_prediction = interp_next

    profit_percent = ((best_prediction - current_price)/ current_price) * 100
    profit_percent = round(profit_percent, 2)
    
    if profit_percent > 3:
        recommendation = "STRONG BUY"
    
    elif profit_percent > 1:
        recommendation = "BUY"
    
    elif profit_percent > 0:
        recommendation = "HOLD"
        
    else:
        recommendation = "SELL"


    # -------- INTERPRETATION --------
    if slope > 0:
        trend_msg = "Overall Upward Trend 📈"
    else:
        trend_msg = "Overall Downward Trend 📉"

    if avg_rate > 0:
        momentum_msg = "Positive Momentum"
    else:
        momentum_msg = "Negative Momentum"


    # -------- GRAPHS --------
    linear_html = linear_dashboard(x, y, y_pred, next_linear, mae1)
    euler_html = euler_dashboard(x, y, euler_next, mae2)
    diff_html = diff_dashboard(x, dy)
    interp_html = interpolation_dashboard(x, y, y_interp, interp_next, mae3)


    return render_template(
        "result.html",
        linear_html=linear_html,
        euler_html=euler_html,
        diff_html=diff_html,
        interp_html=interp_html,   # ✅ NEW

        trend_msg=trend_msg,
        volatility_msg=volatility_msg,
        momentum_msg=momentum_msg,

        best_method=best_method,
        best_prediction=round(best_prediction, 2),

        mae1=round(mae1, 2),
        mre1=round(mre1, 2),

        mae2=round(mae2, 2),
        mre2=round(mre2, 2),

        mae3=round(mae3, 2),   # ✅ NEW
        mre3=round(mre3, 2),    # ✅ NEW
        
        current_price=current_price,

        stock_name=symbol,
        
        profit_percent=profit_percent,

        recommendation=recommendation,
        
        today=today
    )

#top 5 stocks

@app.route("/topstocks")
def top_stocks():

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ITC.NS",
        "SBIN.NS"
    ]

    results = []

    for stock in stocks:

        df = get_stock_data(stock)

        if df.empty:
            continue

        y = df["Close"].dropna().values
        x = np.arange(len(y))

        y_pred, next_linear, slope, mae1, mre1 = linear_method(x, y)

        current_price = y[-1]

        profit = (
            (next_linear - current_price)
            / current_price
        ) * 100

        results.append({
            "stock": stock,
            "profit": round(profit, 2)
        })

    results.sort(
        key=lambda x: x["profit"],
        reverse=True
    )

    top5 = results[:5]

    return render_template(
        "top_stocks.html",
        stocks=top5
    )

#portfolio recommendation

@app.route("/portfolio", methods=["POST"])
def portfolio():

    investment = float(request.form["investment"])

    stocks = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ITC.NS",
        "SBIN.NS"
    ]

    results = []

    for stock in stocks:

        df = get_stock_data(stock)

        if df.empty:
            continue

        y = df["Close"].dropna().values

        x = np.arange(len(y))

        y_pred, next_linear, slope, mae1, mre1 = linear_method(x, y)

        current_price = y[-1]

        profit = ((next_linear - current_price)/ current_price) * 100

        if profit > 0:

            results.append({
                "stock": stock,
                "profit": profit
            })

    results.sort(key=lambda x: x["profit"],reverse=True)

    top3 = results[:3]

    total_profit = sum(stock["profit"] for stock in top3)

    for stock in top3:

        allocation = (stock["profit"]/ total_profit) * investment

        stock["allocation"] = round(allocation,2)

    return render_template(
        "portfolio.html",
        stocks=top3,
        investment=investment
    )

#portfolio input

@app.route("/portfolio_input")
def portfolio_input():
    return render_template("portfolio_input.html")

# ---------------- DASHBOARD PAGE ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)