import pandas as pd
import json
import os

class htfConfirmation:

    def __init__(self):

        filePathList = [os.path.dirname(__file__), 'supportFiles', 'hdf.csv']
        self.filePath = os.path.join(*filePathList)
        self.data = pd.read_csv(self.filePath)

        configFile = open("configuration.json")
        config = json.load(configFile)
        configFile.close()

        self.parameters = config['parameters']

    def bearCheck(self):
        cond = True
        cond = cond and self.data['rsi14']>self.parameters['Bearish']['RSI']
        cond = cond and self.data['wave2']>self.parameters['Bearish']['WTWS']
        cond = cond and self.data['obv']>self.data['smaObv']
        cond = cond and self.data['minusDM']>self.data['plusDM']
        return cond

    def bullCheck(self):
        cond = True
        cond = cond and self.data['rsi14']<self.parameters['Bullish']['RSI']
        cond = cond and self.data['wave2']<self.parameters['Bullish']['WTWS']
        cond = cond and self.data['obv']<self.data['smaObv']
        cond = cond and self.data['minusDM']<self.data['plusDM']
        return cond