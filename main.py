import requests
import os

# Your https://www.alphavantage.co/ API key
# ot use the following string of code add STOCK_API_KEY variable
# to the environment variables (or just substitute API key directly to code)
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")


def request(params):
    try:
        response = requests.get("https://www.alphavantage.co/query", params=params)
    except:
        print(f"Error occured, responcse status code: {response.status_code}")
        return None
    else:
        return response.json()


def get_daily_info(ticker, output_size="compact"):
    '''return dictionary with price info'''
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": output_size,
        "apikey": STOCK_API_KEY,
    }
    return request(params)


def get_intraday_info(ticker, interval="5min", adjusted=True, output_size="compact"):
    '''return dictionary with price info'''
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": ticker,
        "adjusted": str(adjusted),
        "outputsize": output_size,
        "interval": interval,
        "apikey": STOCK_API_KEY,
    }
    return request(params)


def get_price(time_dict, price_type="3. low", chronically=True):
    """
    time_dict - dictionary that is outut of get_..._info functions
    price_type - possible values \in ['1. open', '2. high', '3. low', '4. close']
    chronically - if True return data in chronical order (first - oldest)
    return list with price data
    """
    assert type(time_dict) == dict
    assert price_type in ['1. open', '2. high', '3. low', '4. close']

    time = list(time_dict.keys())[-1]
    price = [float(time_dict[time][key]["3. low"])
             for key in time_dict[time]]

    if chronically:
        return price[::-1]

    return price
