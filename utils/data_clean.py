def clean_data(df_prices, 
               mkt_symbol,
               thresh_valid_data = 0.95,
               size_train = 0.75):
    """
    Clean stock price data, removing tickers with low ammount of observations
    
    PARAMETERS
    ----------
        df_prices : pandas.DataFrame
            A dataframe with prices in the long format
        
        mkt_symbol : str
            The symbol for the market index (e.g., "^GSPC", "^BVSP", etc.)
            
        thresh_valid_data : float, optional, default=0.95
            Minimum proportion of valid rows (relative to market index)
            required for a ticker to be kept.

        size_train : float, optional, default=0.75
            Proportion of the dataset to use for training (remaining for testing).

    RETURNS
    -------
    df_ret : pandas.DataFrame
        DataFrame of returns for all tickers.
    df_train : pandas.DataFrame
        Training subset of returns.
    df_test : pandas.DataFrame
        Testing subset of returns.
    """

    # Save the information of the index
    df_sp500 = df_prices.query("ticker == @mkt_symbol")

    print(df_prices.info())

    # Count the number of rows
    rows_sp500 = df_sp500.shape[0]

    # Creates a minimun threshold
    threshold_rows = rows_sp500*thresh_valid_data
    
    # Counts the number of rows for every share
    ticker_count = df_prices["ticker"].value_counts()

    # If the number of rows >= threshold, save the share's ticket, else discard the ticket
    valid_tickers = ticker_count[ticker_count >= threshold_rows].index

    # Creates a boolean list, True for the shares that should keept
    # and False for those that should be discarded
    idx = df_prices["ticker"].isin(valid_tickers)

    # Creates a dataframe with the cleaned data
    df_prices_cleaned = df_prices[idx]

    print(f"Size original: {df_prices.shape}")
    print(f"Size reduced: {df_prices_cleaned.shape}")

    df_prices_cleaned.dropna(inplace=True)
    # change to wide table
    df_prices_pivot = df_prices_cleaned.pivot(
        columns='ticker', 
        values='Adj Close'
        )

    # calculate returns
    df_ret = df_prices_pivot.pct_change(fill_method=None)
    df_ret.dropna(inplace=True)
    n_obs = df_ret.shape[0]
    ref_dates = df_ret.index
    cut_point = int(n_obs*size_train)
    cut_date = ref_dates[cut_point]

    df_train = df_ret[df_ret.index < cut_date]
    df_test = df_ret[df_ret.index >= cut_date]

    return df_ret, df_train, df_test
    