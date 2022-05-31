# importing modules
import requests, json
from telegram import Update
from telegram.ext import CallbackContext
from Data.my_keys import owm_api_key


#air_url='http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
temp=[]


def temperature(city):
    temp_URL = "https://api.openweathermap.org/data/2.5/weather?q={city}&appid={owm_api_key}}"
    response = requests.get(temp_URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temp.append(main['temp'])
        temp.append(main['feels_like']) 
        temp.append(main['humidity'])
        temp.append(main['pressure'])
        temp.append(data['weather'])
        temp.append(data['wind'])
    else:
        print("Error in the HTTP request")
    return temp

# print("Enter city name: ",end="")
# city = input()
# result=temperature(city)
# print(result)

def weather(update:Update,context:CallbackContext): 
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    city=' '.join(map(str,context.args))
    result=temperature(city)
    result=(f'''
        Temperature: {temp[0]}\n
        Feel Like: {temp[1]}\n   
        Humidity: {temp[2]}\n
        Pressure: {temp[3]}\n
        Weather Report: {temp[4]}\n
        Wind Speed: {temp[5]}\n
        Time Zone: \n''')
    context.bot.send_chat_action(update.effective_chat.id,'typing')
    context.bot.send_message(update.effective_chat.id,result)
