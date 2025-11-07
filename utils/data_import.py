import yfinance as yf
import pandas as pd
from multiprocessing import Pool
from itertools import repeat
import requests
from io import StringIO



def get_sp100(FIRST_DATE, LAST_DATE):
    """Returns constitutents of SP100 index and the index itself 
    
    Parameters
    ----------
        None
        
    Returns
    -------
    list
        A list of tickers.


    Examples
    --------
    >>> print(get_sp100_constitution())
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

