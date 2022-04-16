import pandas as pd
import json

signToggle = lambda num1, num2: num1*num2<0
macdHistSwitchTS = [(0,0), (0,0), (0,0), (0,0)]

fileName = "./outputFiles/dataDumpFile.csv"

data = pd.read_csv(fileName)
macdHistSwitchTS[3] = (data['datetime'].iloc[0], 0)

timeStamp = []
resultCol = []

for i in range(len(data)-1):

    if (signToggle(data['macd3'].iloc[i], data['macd3'].iloc[i+1])):

        macdHistSwitchTS[0] = macdHistSwitchTS[1]
        macdHistSwitchTS[1] = macdHistSwitchTS[2]
        macdHistSwitchTS[2] = macdHistSwitchTS[3]
        macdHistSwitchTS[3] = (data['datetime'].iloc[i], i)

        #print(data['rsi14'].iloc[macdHistSwitchTS[0][1]:macdHistSwitchTS[1][1]])
        rsiM1 = data['rsi14'].iloc[macdHistSwitchTS[0][1]:macdHistSwitchTS[1][1]].max()
        rsiM2 = data['rsi14'].iloc[macdHistSwitchTS[2][1]:macdHistSwitchTS[3][1]].max()
        priceM1 = data['close'].iloc[macdHistSwitchTS[0][1]:macdHistSwitchTS[1][1]].max()
        priceM2 = data['close'].iloc[macdHistSwitchTS[2][1]:macdHistSwitchTS[3][1]].max()

        if (rsiM2<rsiM1 and priceM2>=priceM1):
            result = "Bearish"
        elif (rsiM1>rsiM2 and priceM1>=priceM2):
            result = "Bullish"
        else:
            result = "Unknown"

        timeStamp.append(data['datetime'].iloc[i])
        resultCol.append(result)
        resCol = pd.DataFrame(timeStamp, resultCol)
        #resCol['timeStamp'] = timeStamp
        #resCol['result'] = resultCol

resCol.to_csv('./outputFiles/divergenceRes.csv')
