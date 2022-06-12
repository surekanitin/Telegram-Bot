from bs4 import BeautifulSoup
import requests
import csv
from difflib import get_close_matches
import pandas as pd
from telegram import Update
from telegram.ext import CallbackContext

# OFFSET = 127462 - ord('A')
# def flag(code):
#     return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

URL='https://www.worldometers.info/coronavirus/#countries'

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
        
        getDetails(URL.format())

flag_code = pd.read_csv("/home/nitin/Desktop/PROJECT/Telegram-Bot/Data/flag_code.csv")
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
def covid(country):
    detail=[]
    data=[]
    # emoji=[]
    if country in ('usa','uae','uk','Uk','Usa','Uae','USA','UK','UAE'):
        country=country.upper()
    else:
        country=country.capitalize()
    result,res=check_country(country)
    if res==True:
        data=covid_data.loc[covid_data['Country']==country]
        for col in data.iloc[-1]:
            detail.append(col)
        case=f'''
📌Country :{detail[0]} 
📌Total Cases :{detail[1]}
📌New Cases :{detail[2]}
📌Total Deaths :{detail[3]}
📌New Deaths :{detail[4]}
📌Total Recovered :{detail[5]}
📌New Recovered :{detail[6]}
📌Active Cases :{detail[7]}
    '''
    else:
        case=f'Did you mean {result}'
    return case

def covid_result(update:Update,context:CallbackContext):    
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    try:
        country=' '.join(map(str,context.args))
        if country == '':
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            context.bot.send_message(update.effective_chat.id,text="Please type the country name like \"/covid India\".\n")
        else:
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            try:
                ans=covid(country)
                context.bot.send_chat_action(update.effective_chat.id,'typing')
                context.bot.send_message(update.effective_chat.id,text="Displaying Results for "+country)
                context.bot.send_message(update.effective_chat.id,ans)
            except:
                context.bot.send_chat_action(update.effective_chat.id,'typing')
                context.bot.send_message(update.effective_chat.id,text="Country does not exist!!")
    except:
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,text="Please type the country name like \"/covid India\".\n")

            
    


