from bs4 import BeautifulSoup
import requests
import csv
from difflib import get_close_matches
import pandas as pd
from telegram import Update
from telegram.ext import CallbackContext

URL='https://www.worldometers.info/coronavirus/#countries'
# page = requests.get(URL.format(offset='0'))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
}
with open ('/home/nitin/Desktop/PROJECT/Telegram-Bot/Data/countries_covid_data.csv','w',newline = '') as csvfile:
        my_writer = csv.writer(csvfile)
        header=(['Country','Total Cases','New Cases','Total Deaths','New Deaths','Total Recovered','New Recovered','Active Cases'])
        my_writer.writerow(header)
        def getDetails(url):
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")
            tableContainer = soup.find(id="main_table_countries_yesterday")
            tableBody = tableContainer.find("tbody")
            tableRows = tableBody.find_all("tr")
            for row in tableRows:
                #sno=row.find_all("td")[0].text.strip()
                country = row.find_all("td")[1].text.strip()
                tcases = row.find_all("td")[2].text.strip()
                ncases = row.find_all("td")[3].text.strip()
                tdeaths = row.find_all("td")[4].text.strip()
                ndeaths = row.find_all("td")[5].text.strip()
                trecover= row.find_all("td")[6].text.strip()
                nrecover = row.find_all("td")[7].text.strip()
                acases = row.find_all("td")[8].text.strip()
                input=([country,tcases,ncases,tdeaths,ndeaths,trecover,nrecover,acases])
                my_writer.writerow(input)
                #print("Symbol:", symbol, "Name:", name)
        
        getDetails(URL.format())


covid_data=pd.read_csv("/home/nitin/Desktop/PROJECT/Telegram-Bot/Data/countries_covid_data.csv")
country_name = pd.read_csv("/home/nitin/Desktop/PROJECT/Telegram-Bot/Data/countries.csv")
countries=country_name['Country'].tolist()


def check_country(country):
    country_split = country.split(' ')
    country = ' '.join([x.title() for x in country_split if x != 'and'])
    if country not in countries:
        closest_match = get_close_matches(country, countries, n=4, cutoff=.6)
        if len(closest_match) < 1:
            closest_match = get_close_matches(country, countries, n=4, cutoff=0.4)
            if len(closest_match) < 1:
                closest_match = get_close_matches(country, countries, n=4, cutoff=0.2)
                if len(closest_match) < 1:
                    return None, False
        return closest_match, False
    else:
        return country, True

#for getting covid updates
def covid(update:Update,context:CallbackContext):    
    detail=[]
    data=[]
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    country=' '.join(map(str,context.args))
    if country in ('usa','uae','uk','Uk','Usa','Uae','USA','UK','UAE'):
        country=country.upper()
    else:
        country=country.capitalize()
    result,res=check_country(country)
    if res==True:
        data=covid_data.loc[covid_data['Country']==country]
        for col in data.iloc[-1]:
            detail.append(col)
        cases=f'''
📌Country :{detail[0]}
📌Total Cases :{detail[1]}
📌New Cases :{detail[2]}
📌Total Deaths :{detail[3]}
📌New Deaths :{detail[4]}
📌Total Recovered :{detail[5]}
📌New Recovered :{detail[6]}
📌Active Cases :{detail[7]}
    '''
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,cases)
    else:
        case=f'Did you mean {result}'
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,case)

    
# print("Enter the name of the country: ", end="")
# country=input()
# result,res=check_country(country)
# print(result)
# if res==True:
#     data=covid_data.loc[covid_data['Country']==country]
#     print(data['Country'])
    


