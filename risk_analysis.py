def calculate_risk(data):

    returns = data['Close'].pct_change()

    volatility = returns.std()

    if volatility < 0.01:
        return "Low"

    elif volatility < 0.03:
        return "Medium"

    else:
        return "High"