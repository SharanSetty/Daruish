import talib as ta
import pandas as pd
import numpy as np
import json
import os

import WTO
import customFuncs

class prepareData:

    def __init__(self):
        def indicators(data):
            data['rsi14'] = ta.func.RSI(data.close, 14)
            data['macd1'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[0]
            data['macd2'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[1]
            data['macd3'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[2]
            data['obv'] = ta.func.OBV(data.close, data.volume)
            data['smaObv'] = customFuncs.smoothObv(data['obv'])
            data['wave1'] = WTO.wtoFunc(data)[0]
            data['wave2'] = WTO.wtoFunc(data)[1]
            data['minusDM'] = ta.func.MINUS_DM(data.high, data.low)
            data['plusDM'] = ta.func.PLUS_DM(data.high, data.low)
            data['9ema'] = ta.func.EMA(data.close, timeperiod = 9)
            data['21ema'] = ta.func.EMA(data.close, timeperiod = 21)
            return data

        configFile = open("configuration.json")
        config = json.load(configFile)
        configFile.close()

        filePathList = [os.path.dirname(__file__), 'files', config['assetPair'] + '.csv']
        filePath = os.path.join(*filePathList)

        df = pd.read_csv(filePath)
        hdf = customFuncs.convertTimefrmae(df, config['higherTimeframe'])
        ldf = customFuncs.convertTimefrmae(df, config['lowerTimeframe'])
        hdf.dropna(inplace=True)
        ldf.dropna(inplace=True)

        hdf = indicators(hdf)
        ldf = indicators(ldf)
        print(hdf)
        print(ldf)

        os.makedirs('supportFiles',exist_ok=True)
        hdfFilePathList = [os.path.dirname(__file__), 'supportFiles', 'hdf.csv']
        ldfFilePathList = [os.path.dirname(__file__), 'supportFiles', 'ldf.csv']
        hdfFilePath = os.path.join(*hdfFilePathList)
        ldfFilePath = os.path.join(*ldfFilePathList)

        hdf.to_csv(hdfFilePath)
        ldf.to_csv(ldfFilePath)
