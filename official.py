import pandas as pd
from datetime import datetime, timedelta
import datetime

# Import data

df = pd.read_csv('https://bestat.statbel.fgov.be/bestat/api/views/939c67bb-39fa-4f49-9d05-c446187bef1d/result/CSV')

# Put the shit in the right shape

df = df.groupby(['Jour','Produit'], sort=False)['Prix TVA incl.'].mean().unstack().reset_index().rename(columns={'Jour':'Date', 'Essence 95 RON E10 (€/L)':'E95', 'Essence 98 RON E5 (€/L)':'E98', 'Diesel B7 (€/L)':'D7', 'Gasoil chauffage 50S (moins de 2000 l) (€/L)':'Mazout_moins', 'Gasoil chauffage 50S (à partir de 2000 l) (€/L)':'Mazout_plus'   })

# Select columns

df = df[["Date", "E95", "E98","D7","Mazout_moins","Mazout_plus"]]

# Clean the dates

df['Date'] = df['Date'].replace({'fev':'feb', 'avr':'apr', 'mai':'may', 'aou':'aug'}, regex = True)

# Convert to datetime

df['Date']= pd.to_datetime(df['Date'])

# First export of historical data

df_histo = df.rename(columns={"E95": "Essence 95 RON E10", "E98": "Essence 98 RON E5", "D7": "Diesel B7", "Mazout_moins": "Gasoil chauffage 50S (moins de 2000 l)", "Mazout_plus": "Gasoil chauffage 50S (à partir de 2000 l)"})

df_histo.to_csv('./official_histo.csv')

# Set when is today, tomorrow, one year ago (most ancient date is 364 days ago)

today = datetime.datetime.today().strftime("%Y-%m-%d")
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Filter based on today, tomorrow, one year ago

df = df.loc[((df['Date'] == today) | (df['Date'] == tomorrow) )]

# Reformat date in French

df['Date'] = df['Date'].dt.strftime('%d/%m/%y')

# Keep 2 after comma

df["E95"] = df["E95"].map('{:.2f}'.format)
df["E98"] = df["E98"].map('{:.2f}'.format)
df["D7"] = df["D7"].map('{:.2f}'.format)
df["Mazout_moins"] = df["Mazout_moins"].map('{:.2f}'.format)
df["Mazout_plus"] = df["Mazout_plus"].map('{:.2f}'.format)

# Add today's date

df['today']= datetime.datetime.today().strftime('%d/%m/%Y %H:%M')

df.to_csv("./official.csv", index=False)
