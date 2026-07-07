import requests

API_KEY = "VAfOBEKuPAcsRvF2bASpOF0XrIbHu03g"

def search_stock(keyword, market="global"):

    if market == "india":
        exchange = "NSE"

    elif market == "usa":
        exchange = "NASDAQ"

    else:
        exchange = ""

    url = (
        f"https://financialmodelingprep.com/stable/search-symbol"
        f"?query={keyword}"
        f"&exchange={exchange}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    results = []

    for item in data:

        results.append({
            "symbol": item.get("symbol"),
            "name": item.get("name"),
            "exchange": item.get("exchangeShortName")
        })

    return results