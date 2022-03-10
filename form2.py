from datetime import datetime as dt
import time
import pandas as pd
import plotly.graph_objects as go
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from patterns import candlestick_patterns

with open('datasets2/nifty50.csv') as f:
    for line in f:
        if "," not in line:
            continue
        symbol = line.split(",")[0]
        # period1=int(time.mktime(dt(int(pd1.split("-")[0]),int(pd1.split("-")[1]),int(pd1.split("-")[2])).timetuple()))
        # period2=int(time.mktime(dt(int(pd2.split("-")[0]),int(pd2.split("-")[1]),int(pd2.split("-")[2])).timetuple()))
        # interval='1d'
        req = Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=1646047569&period2=1646565969&useYfid=true&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=k6guoqE6dXg&corsDomain=finance.yahoo.com')
        try:
            response = urlopen(req)
            df=pd.read_json(response)
            y=df.chart.result
            y=y[0]
            ctr=0
            try:
                time= y['timestamp']
                for i in time:
                    ts = dt.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
                    time[ctr] = ts
                    ctr=ctr+1
                open= y['indicators']['quote'][0]['open']
                high= y['indicators']['quote'][0]['high']
                low=  y['indicators']['quote'][0]['low']
                close= y['indicators']['quote'][0]['close']
                data2=pd.DataFrame(list(zip(time,open,high,low,close)),columns=['timestamp','open','high','low','close'])
                data2.to_csv('datasets2/daily/{}.csv'.format(symbol))
                fig = go.Figure(data=[go.Candlestick(x=data2['timestamp'],open=data2['open'],high=data2['high'],low=data2['low'],close=data2['close'])])
                fig.update_layout(xaxis_rangeslider_visible=False)
                fig.write_image('datasets2/images/{}.jpeg'.format(symbol))
            except KeyError as k:
                print('keyError for', symbol)
                continue
        except HTTPError as e:
            print('The server couldn\'t fulfil request for', symbol)
            continue
        except URLError as e:
            print('We failed to reach a server.')
            continue