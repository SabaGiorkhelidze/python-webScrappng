import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('binebi.db')
cur = conn.cursor()
cur.execute('''
    create table if not exists binebi(id INTEGER PRIMARY KEY, price NUMBER, rooms VARCHAR)
''')

def extract_numbers_from_price(price_text):
    if not price_text:
        return None

    numeric_chars = []
    for char in price_text:
        if char.isdigit():
            numeric_chars.append(char)

    if numeric_chars:
        return int(''.join(numeric_chars))
    else:
        return None

for i in range(1, 3):
    url = f"https://binebi.ge/gancxadebebi?deal_types=3&city=1&urban=15&page={i}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all("div", class_="item-info")
    binebi = []

    for item in items:
        # Extract id, name, price, and rooms
       
        price_element = item.find('span', class_="convert_sp")
        price_text = price_element.text if price_element else "N/A"
        price = extract_numbers_from_price(price_text)

        room_element = item.find('span', class_="bpg_rioni")
        room = room_element.text if room_element else "N/A"

        binebi.append(( price, room))

    for property_data in binebi:
        cur.execute("INSERT INTO binebi (price, rooms) VALUES ( ?, ?)", property_data)

    conn.commit()

# Close the connection after inserting all the data
conn.close()
