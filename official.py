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

df['Date'] = df['Date'].replace({'jan21':'/01/2021', 'fev21':'/02/2021', 'mar21':'/03/2021', 'avr21':'/04/2021', 'mai21':'/05/2021', 'jun21':'/06/2021', 'jul21':'/07/2021', 'aou21':'/08/2021', 'sep21':'/09/2021', 'oct21':'/10/2021', 'nov21':'/11/2021', 'dec21':'/12/2021', 'jan22':'/01/2022', 'fev22':'/02/2022', 'mar22':'/03/2022', 'avr22':'/04/2022', 'mai22':'/05/2022', 'jun22':'/06/2022', 'jul22':'/07/2022', 'aou22':'/08/2022', 'sep22':'/09/2022', 'oct22':'/10/2022', 'nov22':'/11/2022', 'dec22':'/12/2022'}, regex = True)

#Convert to datetime

df['Date']= pd.to_datetime(df['Date'])

#Set when is today, tomorrow, one year ago (most ancient date is 361 days ago)

today = datetime.datetime.today().strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
one_year_ago = (datetime.datetime.now() + datetime.timedelta(days=-361)).strftime("%Y-%m-%d")

#Filter based on today, tomorrow, one year ago

df = df.loc[((df['Date'] == today) | (df['Date'] == tomorrow) | (df['Date'] == one_year_ago) )]

#Reformat date in French

df['Date'] = df['Date'].dt.strftime('%d/%m/%y')

df.to_csv("./official.csv", index=False)
