import pandas as pd
import json

def smoothObv(obv):
    sObv = pd.Series(obv.rolling(window=200).mean(), name="smaObv")
    return sObv

#allowed units for timeframe: 'min' and 'H'
def convertTimefrmae(df, timeframe):
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.groupby(pd.Grouper(freq=timeframe)).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    })
    return df