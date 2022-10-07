import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)


df = pd.read_html('https://kworb.net/spotify/country/tr_daily.html')[0]
print(df)