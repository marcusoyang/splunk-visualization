## Overview
This is a Splunk App using [Modular Input](https://dev.splunk.com/enterprise/docs/developapps/manageknowledge/custominputs/modinputsoverview/) to fetch cryptocurrency data from the [CoinGecko Public API](https://www.coingecko.com/en/api/documentation). It is utilizes [checkpointing](https://docs.splunk.com/Documentation/Splunk/latest/AdvancedDev/ModInputsCheckpoint) to maintain state and paging to iterate through data based on market capitalization. It is also capable of fetching historical data.

The front end visualization built using the [Splunk UI Toolkit](https://splunkui.splunk.com/) based on [React](https://reactjs.org/) can be found in [this](https://github.com/marcusoyang/splunk-visualization-ui) repository.

### Custom Search Command

A [custom search command](https://dev.splunk.com/enterprise/docs/devtools/customsearchcommands/) has also been built to fetch BTC-to-currency exchange rates. This is done by using the [Splunk SDK for Python](https://dev.splunk.com/enterprise/docs/devtools/python/sdk-python/). The command is called `btctocurrency` and can be used as follows:

```bash
| btctocurrency <currency>
```

Note: Not all currencies are supported. The list of supported currencies can be found [here](https://www.coingecko.com/en/api/documentation#explore-api).

<br>

![BTC to currency custom command](/static/part3.PNG)

<br>

The front end visualization built using the [Splunk UI Toolkit](https://splunkui.splunk.com/) based on [React](https://reactjs.org/) can be found in [this](https://github.com/marcusoyang/splunk-visualization-ui) repository.

<br>

![Part 1 of the Dashboard](/static/part1.PNG)

<br>

![Part 2 of the Dashboard](/static/part2.PNG)
