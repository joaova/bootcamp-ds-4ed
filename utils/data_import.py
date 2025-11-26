import yfinance as yf
import pandas as pd
import requests
from io import StringIO



def get_sp100(FIRST_DATE, LAST_DATE):
    """Returns constitutents of SP100 index and the index itself 
    
    Parameters
    ----------
        FIRST_DATE : str or datetime
            Start date for price data (e.g. "2020-01-01")
        LAST_DATE : str or datetime
            End date for price data (e.g. "2024-12-31")
        
    Returns
    -------
    list
        A list of tickers.


    Examples
    --------
    >>> df = get_sp100("2020-01-01", "2024-12-31")
    """

    
    
    print("Fetching SP100 components")
    wiki_url =  "https://en.wikipedia.org/wiki/S%26P_100"

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(wiki_url, headers=header)
    
    table = pd.read_html(StringIO(r.text))[2]
    
    tickers = table["Symbol"].tolist()
    
    print(f"\t-> got {len(tickers)} tickers", end="\n\n")
        
    # add SP500 index itself
    tickers.append("^SP100") 

    data = yf.download(tickers, start=FIRST_DATE, end=LAST_DATE)["Close"]

    data = data.reset_index()

    data.set_index('Date', inplace = True)
               
    return data

def get_ibv(FIRST_DATE, LAST_DATE):
    """Returns constitutents of SP100 index and the index itself 
    
    Parameters
    ----------
        FIRST_DATE : str or datetime
            Start date for price data (e.g. "2020-01-01")
        LAST_DATE : str or datetime
            End date for price data (e.g. "2024-12-31")
        
    Returns
    -------
    list
        A list of tickers.


    Examples
    --------
    >>> df = get_sp100("2020-01-01", "2024-12-31")
    """

    
    
    print("Fetching IBOV components")
    wiki_url =  "https://en.wikipedia.org/wiki/List_of_companies_listed_on_B3"

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    r = requests.get(wiki_url, headers=header)
    
    table = pd.read_html(StringIO(r.text))[0]
    
    tickers = table["Ticker"].tolist()

    tickers = list(map(lambda x: str(x) + ".SA", tickers))
    
    print(f"\t-> got {len(tickers)} tickers", end="\n\n")
        
    # add SP500 index itself
    tickers.append("^BVSP") 

    data = yf.download(tickers, start=FIRST_DATE, end=LAST_DATE)["Close"]

    data = data.reset_index()

    data.set_index('Date', inplace = True)
               
    return data

