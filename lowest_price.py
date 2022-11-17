import requests
import pandas as pd
from bs4 import BeautifulSoup

# Get page

url = "https://carbu.com/belgique//index.php/meilleurs-prix/Belgique/BE/0"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

table = soup.find('table', class_='table table-bordered')

# Defining of the dataframe
df = pd.DataFrame(columns=['Province', 'Super 95 (E10)', 'Super 98 (E5)', 'Diesel (B7)'])

# Collecting data
for row in table.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        Province = columns[0].text.strip()
        E95 = columns[1].text.strip()
        E98 = columns[3].text.strip()
        D7 = columns[5].text.strip()

        df = df.append({'Province': Province,  'E95': E95, 'E98': E98, 'D7' : D7}, ignore_index=True)

# Call base
        
df_base = pd.read_csv('https://raw.githubusercontent.com/amcaw/carburants/main/best_carbu_base.csv')

# Merged base with today's data

df_all = pd.merge(df, df_base, on='Province')

# Export to CSV

df_all.to_csv("./best_carbu.csv", index=False)
