from __future__ import absolute_import, division, print_function, unicode_literals
import os,sys
import time
import json
import requests as req
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators

@Configuration(type="reporting")
class btctocurrency(GeneratingCommand):
    currency = Option(require=True)

    def coingecko_api_call(self, requestURL):
        response=req.get(url=requestURL)
        if response.status_code !=200:
            print('Status: ',response.status_code,'Headers: ',response.headers,'Error Response: ',response.json())
            exit()
        data=response.json()
        return json.dumps(data)

    def get_currency_exchange(self, currency):
        requestURL = "https://api.coingecko.com/api/v3/exchange_rates"
        exchange_rates = self.coingecko_api_call(requestURL)
        data = json.loads(exchange_rates)
        return data["rates"][currency]["value"]

    def generate(self):
        exchange_rate = self.get_currency_exchange(self.currency)
        yield {'_time': time.time(),'coin' : self.currency, 'exchange_rate' : exchange_rate, '_raw': str(self.currency) + "," + str(exchange_rate)}

dispatch(btctocurrency, sys.argv, sys.stdin, sys.stdout, __name__)