

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

'''

# For advanced users, if you want to create single instance mod input, uncomment this method.

def use_single_instance_mode():

    return True

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

    # In single instance mode, to get arguments of a particular input, use

    # opt_vs_currency = helper.get_arg('vs_currency', stanza_name)

    # opt_order = helper.get_arg('order', stanza_name)

    # opt_results_per_page = helper.get_arg('results_per_page', stanza_name)

    # opt_page = helper.get_arg('page', stanza_name)



    # get input type

    # helper.get_input_type()



    # The following examples get input stanzas.

    # get all detailed input stanzas

    # helper.get_input_stanza()

    # get specific input stanza with stanza name

    # helper.get_input_stanza(stanza_name)

    # get all stanza names

    # helper.get_input_stanza_names()



    # The following examples get options from setup page configuration.

    # get the loglevel from the setup page

    # loglevel = helper.get_log_level()

    # get proxy setting configuration

    # proxy_settings = helper.get_proxy()

    # get account credentials as dictionary

    # account = helper.get_user_credential_by_username("username")

    # account = helper.get_user_credential_by_id("account id")

    # get global variable configuration

    # global_userdefined_global_var = helper.get_global_setting("userdefined_global_var")



    # The following examples show usage of logging related helper functions.

    # write to the log for this modular input using configured global log level or INFO as default

    # helper.log("log message")

    # write to the log using specified log level

    # helper.log_debug("log message")

    # helper.log_info("log message")

    # helper.log_warning("log message")

    # helper.log_error("log message")

    # helper.log_critical("log message")

    # set the log level for this modular input

    # (log_level can be "debug", "info", "warning", "error" or "critical", case insensitive)

    # helper.set_log_level(log_level)

    def getResults(page):
        
        opt_vs_currency = helper.get_arg('currency')
    
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        parameters = {"vs_currency":opt_vs_currency, "order":"market_cap_desc", "per_page":100, "page":page}
        url = "https://api.coingecko.com/api/v3/coins/markets"
        
        pageResults = []
    
        response = helper.send_http_request(url, 'GET', parameters=parameters, payload=None,
                                            headers=None, cookies=None, verify=True, cert=None,
                                            timeout=None, use_proxy=True)
       
        r_status = response.status_code
        if r_status != 200:
            # check the response status, if the status is not sucessful, raise requests.HTTPError
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

