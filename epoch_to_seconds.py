import datetime
import pandas as pd

df=pd.read_csv('datasets2/data.csv')
print(df.head())

data=pd.DataFrame(df['Symbol'])
data.to_csv('datasets2/nifty50.csv')

ts = datetime.datetime.fromtimestamp(1646236633).strftime('%Y-%m-%d %H:%M:%S')
print(type(ts))

## 00 - 3:30 fir 8-12
