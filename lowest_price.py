import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://carbu.com/belgique//index.php/meilleurs-prix/Belgique/BE/0"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

table = soup.find('table', class_='table table-bordered')

# Defining of the dataframe
df = pd.DataFrame(columns=['Province', 'Super 95 (E10)', 'Super 98 (E5)', 'Diesel (B7)'])

# Collecting Ddata
for row in table.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        Province = columns[0].text.strip()
        E95 = columns[1].text.strip()
        E98 = columns[3].text.strip()
        D7 = columns[5].text.strip()

        df = df.append({'Province': Province,  'Super 95 (E10)': E95, 'Super 98 (E5)': E98, 'Diesel (B7)' : D7}, ignore_index=True)

df.to_csv("./best_carbu.csv", index=False)
