import requests
import re
from bs4 import BeautifulSoup
import sqlite3 as sl

con = sl.connect('my_data.db', check_same_thread=False)
c = con.cursor()

result = requests.get("https://blacksunshinemedia.com/music/1001-albums-you-must-hear-before-you-die/")

soup = BeautifulSoup(result.content, 'lxml')

for str_li in soup.ol.find_all('li'):
    text = str_li.text
    name, year = text[:-7], int(text[-5:-1])
    with con:
        c.execute("INSERT INTO albums (name, year) values(?, ?)", (name, year))
