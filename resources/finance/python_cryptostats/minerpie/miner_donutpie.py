from bokeh.charts import Donut, show, output_file
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

import pandas as pd
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
    #print(response)
    data = response.read().decode("utf-8")
    print(data)
    return json.loads(data)

# utilize utility to make it easy to get json/dict data converted to a dataframe

url = ("https://api.blockchain.info/pools?timespan=10days")

first_df = get_jsonparsed_data(url)
print(first_df)

df = df_from_json(first_df)

# filter by countries with at least one medal and sort by total medals
#df = df[df['total'] > 8]
#df = df.sort("total", ascending=False)
#df = pd.melt(df, id_vars=['abbr'],
             #value_vars=['bronze', 'silver', 'gold'],
             #value_name='medal_count', var_name='medal')

# original example
print(df[:, 0])
d = Donut(df, label = df[:, 0], values = df[:, 1], 
          text_font_size='8pt', hover_text='blocks mined')

output_file("donut.html", title="donut.py example")

show(d)