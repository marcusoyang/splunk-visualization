# encoding = utf-8
import os
import sys
import time
from datetime import datetime
import json

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''

def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # vs_currency = definition.parameters.get('vs_currency', None)
    # order = definition.parameters.get('order', None)
    # results_per_page = definition.parameters.get('results_per_page', None)
    # page = definition.parameters.get('page', None)
    pass

def collect_events(helper, ew):

    def getResults(page):
        
        opt_vs_currency = helper.get_arg('currency')
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        parameters = {"vs_currency":opt_vs_currency, "order":"market_cap_desc", "per_page":200, "page":page}
        url = "https://api.coingecko.com/api/v3/coins/markets"
        
        pageResults = []
        response = helper.send_http_request(url, 'GET', parameters=parameters, payload=None,
                                            headers=None, cookies=None, verify=True, cert=None,
                                            timeout=None, use_proxy=True)
       
        r_status = response.status_code
        if r_status != 200:
            # check the response status, if the status is not successful, raise requests.HTTPError
            response.raise_for_status()
             
        r_json = response.json()
        for coin in r_json:
            state = helper.get_check_point(coin["symbol"])
            
            if state is None:
                pageResults.append(coin)
                helper.save_check_point(coin["symbol"], coin["last_updated"])
                continue
    
            date_saved = datetime.strptime(state, date_format)
            date_resp = datetime.strptime(coin["last_updated"], date_format)
    
            # check is response date is after saved date
            if date_saved < date_resp:
                pageResults.append(coin)
                helper.delete_check_point(coin["symbol"])
                helper.save_check_point(coin["symbol"], coin["last_updated"])
                
        return pageResults
        
    # Starting page
    page = 1
    minimum_market_cap = int(helper.get_arg('minimum_market_cap'))
    result = []
    below_threshold = False
    
    while not below_threshold:
        page_results = getResults(page)
        for coin in page_results:
            if coin["market_cap"] < minimum_market_cap:
                # Set the flag to True to exit the loop
                below_threshold = True
                break
            else:
                result.append(coin)
        # Increment the page number for the next iteration
        page += 1

    event = helper.new_event(json.dumps(result), time=None, host=None, index=None, source=None, sourcetype=None, done=True, unbroken=True)
    ew.write_event(event)

