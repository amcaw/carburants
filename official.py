import pandas as pd
from datetime import datetime, timedelta
import datetime

#Import data

df = pd.read_csv('https://bestat.statbel.fgov.be/bestat/api/views/939c67bb-39fa-4f49-9d05-c446187bef1d/result/CSV')

#Put the shit in the right shape

df = df.groupby(['Jour','Produit'], sort=False)['Prix TVA incl.'].mean().unstack().reset_index().rename(columns={'Jour':'Date', 'Essence 95 RON E10 (€/L)':'E95', 'Essence 98 RON E5 (€/L)':'E98', 'Diesel B7 (€/L)':'D7', 'Gasoil chauffage 50S (moins de 2000 l) (€/L)':'Mazout_moins', 'Gasoil chauffage 50S (à partir de 2000 l) (€/L)':'Mazout_plus'   })

#Select columns

df = df[["Date", "E95", "E98","D7","Mazout_moins","Mazout_plus"]]

#Clean the dates

df['Date'] = df['Date'].replace({'fev':'feb', 'avr':'apr', 'mai':'may', 'aou':'aug'}, regex = True)

#Convert to datetime

df['Date']= pd.to_datetime(df['Date'])

#Set when is today, tomorrow, one year ago (most ancient date is 364 days ago)

today = datetime.datetime.today().strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
one_year_ago = (datetime.datetime.now() + datetime.timedelta(days=-364)).strftime("%Y-%m-%d")

#Filter based on today, tomorrow, one year ago

df_filter = df.loc[((df['Date'] == today) | (df['Date'] == tomorrow) | (df['Date'] == one_year_ago) )]

#Reformat date in French

df['Date'] = df['Date'].dt.strftime('%d/%m/%y')
df_filter['Date'] = df['Date'].dt.strftime('%d/%m/%y')

df.to_csv("./official_histo.csv", index=False)
df_filter.to_csv("./official.csv", index=False)
