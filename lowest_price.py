import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://carbu.com/belgique//index.php/meilleurs-prix/Belgique/BE/0"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

table = soup.find('table', class_='table table-bordered')

# Defining of the dataframe
df = pd.DataFrame(columns=['province', 'Super 95 (E10)', 'Super 98 (E5)', 'Diesel (B7)'])

# Collecting Ddata
for row in table.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        province = columns[0].text.strip()
        E95 = columns[1].text.strip()
        E98 = columns[3].text.strip()
        D7 = columns[5].text.strip()

        df = df.append({'province': province,  'Super 95 (E10)': E95, 'Super 98 (E5)': E98, 'Diesel (B7)' : D7}, ignore_index=True)

df_E95 = df[["province", "Super 95 (E10)"]]
df_E98 = df[["province", "Super 98 (E5)"]]
df_D7 = df[["province", "Diesel (B7)"]]

df_E95.sort_values(by=['Super 95 (E10)'], inplace=True)
df_E98.sort_values(by=['Super 98 (E5)'], inplace=True)
df_D7.sort_values(by=['Diesel (B7)'], inplace=True)

df_E95.to_csv("./E95.csv", index=False)
df_E98.to_csv("./E98.csv", index=False)
df_D7.to_csv("./D7.csv", index=False)
