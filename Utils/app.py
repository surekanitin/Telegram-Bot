from turtle import clear
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
URL = 'https://finance.yahoo.com/screener/unsaved/9e57e73d-fea7-48f8-b898-129f5b0c9b0d?count=100&dependentField=sector&dependentValues=&offset={offset}'
# page = requests.get(URL.format(offset='0'))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}
with open ('/home/nitin/Desktop/PROJECT/BOT/Symbols.csv','w',newline = '') as csvfile:
        my_writer = csv.writer(csvfile)
        header=(['Symbol','Name'])
        my_writer.writerow(header)
        def getDetails(url):
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")
            tableContainer = soup.find(id="scr-res-table")
            tableBody = tableContainer.find("tbody")
            tableRows = tableBody.find_all("tr")
            for row in tableRows:
                symbol = row.find_all("td")[0].text.strip()
                name = row.find_all("td")[1].text.strip()
                input=([symbol,name])
                my_writer.writerow(input)
        for offset in range(0, 5887, 100):
            getDetails(URL.format(offset=offset))

stock_symbols=pd.read_csv('tickers.csv')
print(stock_symbols)