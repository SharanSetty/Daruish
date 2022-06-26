import pandas as pd
import json
import os
from datetime import datetime, timedelta


class fetchOpp:

    def __init__(self, bigTs, timeStamp, peakPrice, entryPrice):

        self.timeStamp = timeStamp
        self.entryPrice = entryPrice
        self.endTs = (datetime.strptime(bigTs, "%Y-%m-%d %H:%M:%S+00:00") + timedelta(hours=4)).strftime(
            "%Y-%m-%d %H:%M:%S+00:00")

        configFile = open("configuration.json")
        config = json.load(configFile)
        configFile.close()

        filePathList = [os.path.dirname(__file__), 'supportFiles', 'hdf.csv']
        filePath = os.path.join(*filePathList)
        self.data = pd.read_csv(filePath)

        self.stopLoss = peakPrice
        param1 = int(config['parameters']['RiskRewardRatio'].split(':')[0])
        param2 = int(config['parameters']['RiskRewardRatio'].split(':')[1])
        self.targetProfit = self.stopLoss*param2/param1

        resFilePathList = [os.path.dirname(__file__), 'result', 'report.csv']
        self.resFilePath = os.path.join(*resFilePathList)

    def exploit(self):
        stInd = self.data[self.data['datetime'] == self.timeStamp].index.item()
        enInd =self.data[self.data['datetime'] == self.endTs].index.item()

        if (self.entryPrice > self.stopLoss):
            trend = 'Bull'
        else:
            trend = 'Bear'

        for i in range(stInd, enInd):
            if (trend == 'Bear' and self.data['close']> self.stopLoss):
                break
            elif (trend == 'Bear' and self.data['close']< self.targetProfit):
                break
            elif (trend == 'Bull' and self.data['close']< self.stopLoss):
                break
            elif (trend == 'Bull' and self.data['close']> self.targetProfit):
                break
            else:
                res = None

        if (res != None):
            exitPrice = self.data['close'].iloc[i]
        else:
            exitPrice = None

        logStr = ""
        logStr += self.data['datetime'].iloc[stInd] + "\t"
        logStr += self.entryPrice + "\t" + "position entered" + "\n"
        logStr += self.data['datetime'].iloc[i] + "\t"
        logStr += exitPrice + "position exited" + "\n"

        if (exitPrice == None):
            logStr += "Couldn't find exit conditionals in the data" + "\n\n"
        else:
            profit = float(exitPrice) - float(self.entryPrice)
            per = profit / self.entryPrice
            logStr += "Profit: " + str(profit) + "\t" + "Profit percentage" + str(per) + "\n\n"

        resFile = open(self.resFilePath)
        resFile.write(logStr)
        resFile.close()