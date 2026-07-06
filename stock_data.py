import yfinance as yf

def get_stock_data(symbol):

    stock = yf.Ticker(symbol)

    data = stock.history(
        period="1mo",
        interval="1d"
    )

    return data