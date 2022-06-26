import os

import pandas as pd


class ltfConfirm:

    def __init__(self, timeStamp):
        self.timeStamp = timeStamp

        filePathList = [os.path.dirname(__file__), 'supportFiles', 'ldf.csv']
        self.filePath = os.path.join(*filePathList)
        self.data = pd.read_csv(self.filePath)

    def bearConfirm(self):
        ind = self.data[self.data['datetime'] == self.timeStamp].index.item()
        cond = True
        cond = cond and self.data['9ema'].iloc[ind] < self.data['21ema'].iloc[ind]
        cond = cond and self.data['obv'].iloc[ind] < self.data['smaObv'].iloc[ind]
        cond = cond and self.data['minusDM'].iloc[ind] > self.data['plusDM'].iloc[ind]
        return cond

    def bullConfirm(self):
        ind = self.data[self.data['datetime'] == self.timeStamp].index.item()
        cond = True
        cond = cond and self.data['9ema'].iloc[ind] > self.data['21ema'].iloc[ind]
        cond = cond and self.data['obv'].iloc[ind] > self.data['smaObv'].iloc[ind]
        cond = cond and self.data['minusDM'].iloc[ind] < self.data['plusDM'].iloc[ind]
        return cond
