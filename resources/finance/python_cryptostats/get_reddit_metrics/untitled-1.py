import requests


a = requests.get('http://www.google.com/trends/fetchComponent?q=nepal&cid=TIMESERIES_GRAPH_0&export=3')
a.text