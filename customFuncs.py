import pandas as pd

def smoothObv(obv):
    sObv = pd.Series(obv.rolling(window=200).mean(), name="smaObv")
    return sObv