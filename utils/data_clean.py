def clean_data(df_prices, 
               thresh_valid_data = 0.95,
               size_train = 0.75):
    """Clean stock price data, removing tickers with low ammount of observations
    
    PARAMETERS
    ----------
        df_prices : pandas.DataFrame
            A dataframe with prices in the long format
        
        mkt_symbol : str
            The symbol for the market index (e.g. "^GSPC" or 
            
        thresh_valid_data - float

    
    """

    missing = df_prices.isna().sum() / len(df_prices)

    idx = missing[missing > .20].index

    df_prices.drop(idx, axis=1, inplace = True)

    df_prices.bfill(inplace = True)


    # calculate returns
    df_ret = df_prices.pct_change(fill_method=None)
    df_ret.dropna(inplace=True)
    n_obs = df_ret.shape[0]
    ref_dates = df_ret.index
    cut_point = int(n_obs*size_train)
    cut_date = ref_dates[cut_point]

    df_train = df_ret[df_ret.index < cut_date]
    df_test = df_ret[df_ret.index >= cut_date]

    return df_ret, df_train, df_test
    