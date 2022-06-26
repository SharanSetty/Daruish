"""
Third party fetched function definitions
"""
import pandas as pd
import numpy as np

def TP(ohlc):
    """Typical Price refers to the arithmetic average of the high, low, and closing prices for a given period.
    Source: https://github.com/peerchemist/finta/blob/master/finta/finta.py"""
    return pd.Series((ohlc["high"] + ohlc["low"] + ohlc["close"]) / 3, name="TP")

def wtoFunc(
        ohlc,
        channel_length: int = 10,
        average_length: int = 21,
        adjust: bool = True,
):
    """
    Wave Trend Oscillator
    source: http://www.fxcoaching.com/WaveTrend/
    Source: https://github.com/peerchemist/finta/blob/master/finta/finta.py
    """

    ap = TP(ohlc)
    esa = ap.ewm(span=channel_length, adjust=adjust).mean()
    d = pd.Series(
        (ap - esa).abs().ewm(span=channel_length, adjust=adjust).mean(), name="d"
    )
    ci = (ap - esa) / (0.015 * d)

    wt1 = pd.Series(ci.ewm(span=average_length, adjust=adjust).mean(), name="WT1.")
    wt2 = pd.Series(wt1.rolling(window=4).mean(), name="WT2.")

    return [wt1, wt2]