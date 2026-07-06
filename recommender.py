def get_recommendation(current, predicted):

    profit = (
        (predicted - current)
        / current
    ) * 100

    if profit > 3:
        signal = "Strong Buy"

    elif profit > 1:
        signal = "Buy"

    elif profit > 0:
        signal = "Hold"

    else:
        signal = "Sell"

    return profit, signal