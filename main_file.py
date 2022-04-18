import talib as ta
import pandas as pd
import numpy as np
import json

import WTO
import customFuncs

detFile = open('initDetails.json','r')
details = json.load(detFile)
detFile.close()
data = pd.read_csv(details['fileName'])

data['rsi14'] = ta.func.RSI(data.close, 14)
data['macd1'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[0]
data['macd2'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[1]
data['macd3'] = ta.func.MACD(data.close, fastperiod=12, slowperiod=26, signalperiod=9)[2]
obv = ta.func.OBV(data.close, data.volume)
data['obv'] = obv
data['smaObv'] = customFuncs.smoothObv(obv)
data['wave1'] = WTO.wtoFunc(data)[0]
data['wave2'] = WTO.wtoFunc(data)[1]
data['minusDM'] = ta.func.MINUS_DM(data.high, data.low)
data['plusDM'] = ta.func.PLUS_DM(data.high, data.low)


result = []
tDateTime = []

for i in range(len(data)):
    if (details['trend']=='Bear'):
        cond = True
        cond = cond and (data['rsi14'].iloc[i]>details['BearConditionals']['rsi'])
        cond = cond and (data['macd1'].iloc[i]>data['macd2'].iloc[i])
        cond = cond and (data['wave2'].iloc[i]>details['BearConditionals']['wave'])
        cond = cond and (data['obv'].iloc[i]>data['smaObv'].iloc[i])
        cond = cond and (data['plusDM'].iloc[i]>data['minusDM'].iloc[i])
        if cond:
            result.append(True)
            tDateTime.append(data['datetime'].iloc[i])
        else:
            result.append(False)

    elif (details['trend']=='Bull'):
        cond = True
        cond = cond and (data['rsi14'].iloc[i] < details['BullConditionals']['rsi'])
        cond = cond and (data['macd1'].iloc[i] < data['macd2'].iloc[i])
        cond = cond and (data['wave2'].iloc[i] < details['BullConditionals']['wave'])
        cond = cond and (data['obv'].iloc[i] < data['smaObv'].iloc[i])
        cond = cond and (data['plusDM'].iloc[i] < data['minusDM'].iloc[i])
        if cond:
            result.append(True)
            tDateTime.append(data['datetime'].iloc[i])
        else:
            result.append(False)

toW = '\n'.join(tDateTime)
wfile = open(details['outputFileName'],'w')
wfile.write(toW)
wfile.close()

data['result'] = result
data.to_csv(details['dataDumpFileName'])

customFuncs.divergence(details['dataDumpFileName'])

