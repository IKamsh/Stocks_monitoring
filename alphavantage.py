import requests
import os


# https://habr.com/ru/company/ods/blog/327242/
# Your https://www.alphavantage.co/ API key
# or use the following string of code add STOCK_API_KEY variable
# to the environment variables (or just substitute API key directly to code)
#STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
STOCK_API_KEY = 'KJOJHXF1H6A6VV2W'

class API_exception(BaseException):
    pass


def request(params):
    response = requests.get("https://www.alphavantage.co/query", params=params).json()
    if 'Error Message' in response.keys():
        raise API_exception(str(response['Error Message']))
        
    return response


def get_daily(ticker, output_size="compact"):
    '''
    output_size = "compact" by default (return only 100 data points), use "full"
    to get all data
    return dictionary with price info
    '''
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": output_size,
        "apikey": STOCK_API_KEY,
    }
    return request(params)


def get_intraday(ticker, interval="5min", adjusted=True, output_size="compact"):
    '''
    output_size = "compact" by default (return only 100 data points), use "full"
    to get all data
    return dictionary with price info
    '''
    
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
    time_dict - dictionary that is output of get_daily etc. functions
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


def get_price_oc(time_dict, price_type="3. low", chronically=True):
    """
    time_dict - dictionary that is output of get_daily etc. functions
    price_type - possible values \in ['1. open', '2. high', '3. low', '4. close']
    chronically - if True return data in chronical order (first - oldest)
    return list with open and close prices
    """
    assert type(time_dict) == dict
    
    price = []
    
    time = list(time_dict.keys())[-1]
    for key in time_dict[time]:
        price.append(float(time_dict[time][key]["1. open"]))
        price.append(float(time_dict[time][key]["4. close"]))

    if chronically:
        return price[::-1]

    return price