import os
from datetime import datetime, timedelta

import pandas as pd


class ltfCheck:

    def __init__(self, timeStamp):

        self.timeStamp = (datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S+00:00") + timedelta(hours=4)).strftime(
            "%Y-%m-%d %H:%M:%S+00:00")

        self.signToggle = lambda num1, num2: num1 * num2 < 0
        self.macdHistSwitchTS = [(0, 0), (0, 0), (0, 0), (0, 0)]

        filePathList = [os.path.dirname(__file__), 'supportFiles', 'ldf.csv']
        self.filePath = os.path.join(*filePathList)
        self.data = pd.read_csv(self.filePath)

        self.macdHistSwitchTS[3] = (self.timeStamp, self.data[self.data['datetime'] == self.timeStamp].index.item())

        self.timeStamp = []
        self.resultCol = []

    def coDivBear(self):

        for i in range(self.macdHistSwitchTS[3][1], len(self.data) - 1):

            if (self.signToggle(self.data['macd3'].iloc[i], self.data['macd3'].iloc[i + 1])):
                self.macdHistSwitchTS[0] = self.macdHistSwitchTS[1]
                self.macdHistSwitchTS[1] = self.macdHistSwitchTS[2]
                self.macdHistSwitchTS[2] = self.macdHistSwitchTS[3]
                self.macdHistSwitchTS[3] = (self.data['datetime'].iloc[i], i)

                rsiM1 = self.data['rsi14'].iloc[self.macdHistSwitchTS[0][1]:self.macdHistSwitchTS[1][1]].max()
                rsiM2 = self.data['rsi14'].iloc[self.macdHistSwitchTS[2][1]:self.macdHistSwitchTS[3][1]].max()
                priceM1 = self.data['close'].iloc[self.macdHistSwitchTS[0][1]:self.macdHistSwitchTS[1][1]].max()
                priceM2 = self.data['close'].iloc[self.macdHistSwitchTS[2][1]:self.macdHistSwitchTS[3][1]].max()

                if (rsiM2 < rsiM1 and priceM2 >= priceM1):
                    return [self.macdHistSwitchTS[3][0], priceM2, self.data['close'].iloc[i+1]]

    def coDivBull(self):

        for i in range(self.macdHistSwitchTS[3][1], len(self.data) - 1):

            if (self.signToggle(self.data['macd3'].iloc[i], self.data['macd3'].iloc[i + 1])):
                self.macdHistSwitchTS[0] = self.macdHistSwitchTS[1]
                self.macdHistSwitchTS[1] = self.macdHistSwitchTS[2]
                self.macdHistSwitchTS[2] = self.macdHistSwitchTS[3]
                self.macdHistSwitchTS[3] = (self.data['datetime'].iloc[i], i)

                rsiM1 = self.data['rsi14'].iloc[self.macdHistSwitchTS[0][1]:self.macdHistSwitchTS[1][1]].max()
                rsiM2 = self.data['rsi14'].iloc[self.macdHistSwitchTS[2][1]:self.macdHistSwitchTS[3][1]].max()
                priceM1 = self.data['close'].iloc[self.macdHistSwitchTS[0][1]:self.macdHistSwitchTS[1][1]].max()
                priceM2 = self.data['close'].iloc[self.macdHistSwitchTS[2][1]:self.macdHistSwitchTS[3][1]].max()

                if (rsiM1 > rsiM2 and priceM1 >= priceM2):
                    return [self.macdHistSwitchTS[3][0], priceM1, self.data['close'].iloc[i+1]]
