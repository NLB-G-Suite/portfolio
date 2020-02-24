"""
Make a pie chart - see
http://matplotlib.sf.net/matplotlib.pylab.html#-pie for the docstring.

This example shows a basic pie chart with labels optional features,
like autolabeling the percentage, offsetting a slice with "explode",
adding a shadow, and changing the starting angle.

"""
from pylab import *

import json

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

url = ("https://api.blockchain.info/pools?timespan=10days")


labels=[]
fracs=[]

data=get_jsonparsed_data(url)
data=data
print(data)
print(type(data))
for key,value in data.items():
    labels.append(key)
    fracs.append(value)

print(labels)
print(fracs)

## make a square figure and axes
figure(1, figsize=(6,6))
#ax = axes([0.1, 0.1, 0.8, 0.8])

## The slices will be ordered and plotted counter-clockwise.
#labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
#fracs = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)

pie(fracs,  labels=labels,
    autopct='%1.1f%%', explode=explode,shadow=True, startangle=90)
    ## The default startangle is 0, which would start
    ## the Frogs slice on the x-axis.  With startangle=90,
    ## everything is rotated counter-clockwise by 90 degrees,
    ## so the plotting starts on the positive y-axis.

title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})

show()