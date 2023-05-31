import requests
import csv
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus"

response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("tbody").find_all('tr')

activeCase_country = dict()
totalCases_country = dict()
final_data = [activeCase_country, totalCases_country]
for row in table:
    data = row.find('a', {'class': 'mt_a'})
    total_cases = row.find('td', {
        'style': 'font-weight: bold; text-align:right'
    })
    total_nums = row.find('td', {
        'style': 'text-align:right;font-weight:bold;'
    })
    if data is not None and total_nums is not None and total_cases is not None:
        activeCase_numbers = ''.join(filter(str.isdigit, total_nums.text))
        totalCase_numbers = ''.join(filter(str.isdigit, total_cases.text))
        activeCase_country[data.text] = activeCase_numbers
        totalCases_country[data.text] = totalCase_numbers


f = open('statistics.csv', 'w')
writer = csv.writer(f)

header = [' country ', ' totalCase ', ' activeCase ']

with open('statistics.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter='-')
    writer.writerow(header)
    for country in totalCases_country.keys():
        row = [country, totalCases_country[country], activeCase_country[country]]
        writer.writerow(row)
