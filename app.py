from datetime import datetime as dt
import time
import pandas as pd
import os, csv
import talib
import plotly.graph_objects as go
from flask import Flask, request, render_template
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from patterns import candlestick_patterns

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def myform():
    if request.method=="POST":
        pd1 = request.form.get('sdate')
        pd2 = request.form.get('edate')
        pd1=str(pd1)
        pd2=str(pd2)
        with open('datasets/symbols.csv') as f:
            for line in f:
                if "," not in line:
                    continue
                symbol = line.split(",")[0]
                period1=int(time.mktime(dt(int(pd1.split("-")[0]),int(pd1.split("-")[1]),int(pd1.split("-")[2])).timetuple()))
                period2=int(time.mktime(dt(int(pd2.split("-")[0]),int(pd2.split("-")[1]),int(pd2.split("-")[2])).timetuple()))
                interval='1d'

                req = Request(f'https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true')
                try:
                    response = urlopen(req)
                    df=pd.read_csv(response)
                    fig = go.Figure(data=[go.Candlestick(x=df['Date'],open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'])])
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    fig.write_image('datasets/images/{}.jpeg'.format(symbol))
                    df.to_csv('datasets/daily/{}.csv'.format(symbol))
                except HTTPError as e:
                    print('The server couldn\'t fulfil request for', symbol)
                    continue
                except URLError as e:
                    print('We failed to reach a server.')
                    continue
    pattern  = request.args.get('pattern', False)
    stocks = {}

    with open('datasets/symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir('datasets/daily'):
            df = pd.read_csv('datasets/daily/{}'.format(filename))
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]
            

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception as e:
                print('failed on filename: ', filename)
    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)


@app.route('/minutewise') # , methods=['POST','GET'])
def myform2():
    # if request.method=="GET":
        # pd1 = request.form.get('sdate')
        # pd2 = request.form.get('edate')
        # pd1
        # pd1=str(pd1)
        # pd2=str(pd2)
    with open('datasets2/symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            # period1=int(time.mktime(dt(int(pd1.split("-")[0]),int(pd1.split("-")[1]),int(pd1.split("-")[2])).timetuple()))
            # period2=int(time.mktime(dt(int(pd2.split("-")[0]),int(pd2.split("-")[1]),int(pd2.split("-")[2])).timetuple()))
            # interval='1d'
            req = Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=1648575454&period2=1649093854&useYfid=true&interval=10m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=k6guoqE6dXg&corsDomain=finance.yahoo.com')
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
                    op= y['indicators']['quote'][0]['open']
                    hi= y['indicators']['quote'][0]['high']
                    lo=  y['indicators']['quote'][0]['low']
                    cl= y['indicators']['quote'][0]['close']
                    data2=pd.DataFrame(list(zip(time,op,hi,lo,cl)),columns=['timestamp','open','high','low','close'])
                    data2.to_csv('datasets2/hourly/{}.csv'.format(symbol))
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
    return{ 'code' : 'success' }

@app.route('/nifty', methods=['POST','GET'])
def myform3():
    # if request.method=="POST":
        # pd1 = request.form.get('sdate')
        # pd2 = request.form.get('edate')
        # pd1
        # pd1=str(pd1)
        # pd2=str(pd2)
    with open('datasets3/nifty50.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            # period1=int(time.mktime(dt(int(pd1.split("-")[0]),int(pd1.split("-")[1]),int(pd1.split("-")[2])).timetuple()))
            # period2=int(time.mktime(dt(int(pd2.split("-")[0]),int(pd2.split("-")[1]),int(pd2.split("-")[2])).timetuple()))
            # interval='1d'
            req = Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?symbol={symbol}&period1=1648577588&period2=1649095988&useYfid=true&interval=60m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=k6guoqE6dXg&corsDomain=finance.yahoo.com')
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
                    op= y['indicators']['quote'][0]['open']
                    hi= y['indicators']['quote'][0]['high']
                    lo=  y['indicators']['quote'][0]['low']
                    cl= y['indicators']['quote'][0]['close']
                    data2=pd.DataFrame(list(zip(time,op,hi,lo,cl)),columns=['timestamp','open','high','low','close'])
                    data2.to_csv('datasets3/hourly/{}.csv'.format(symbol))
                    fig = go.Figure(data=[go.Candlestick(x=data2['timestamp'],open=data2['open'],high=data2['high'],low=data2['low'],close=data2['close'])])
                    fig.update_layout(xaxis_rangeslider_visible=False)
                    fig.write_image('datasets3/images/{}.jpeg'.format(symbol))
                except KeyError as k:
                    print('keyError for', symbol)
                    continue
            except HTTPError as e:
                print('The server couldn\'t fulfil request for', symbol)
                continue
            except URLError as e:
                print('We failed to reach a server.')
                continue
    return { "code" : "SUCCESS"}