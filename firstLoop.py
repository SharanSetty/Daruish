import json


class htfConfirmation:

    def __init__(self):
        configFile = open("configuration.json")
        config = json.load(configFile)
        configFile.close()

        self.parameters = config['parameters']

    def bearCheck(self, rsi, wave2, obv, smaObv, minusDM, plusDM):
        return all([
            rsi > self.parameters['Bearish']['RSI'],
            wave2 > self.parameters['Bearish']['WTWS'],
            obv > smaObv,
            plusDM > minusDM,
        ])

    def bullCheck(self, rsi, wave2, obv, smaObv, minusDM, plusDM):
        return all([
            rsi < self.parameters['Bullish']['RSI'],
            wave2 < self.parameters['Bullish']['WTWS'],
            obv < smaObv,
            plusDM < minusDM
        ])
