from pyowm.owm import OWM
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../Data")
from Data import my_keys
from telegram import  Update
from telegram.ext import CallbackContext
import pytz, dateutil.parser as dp


cel= u'\N{DEGREE SIGN}'
quality=[" ","Good","Fair","Moderate","Poor","Very Poor"]
cloud_emojis ={
        "few clouds" : u'\U0001F324',
        "scattered clouds" : u'\U000026C5',
        "broken clouds" : u'\U0001F325',
        "overcast clouds" :  u'\U00002601',
        }

emojis ={
    "Clear" : u'\U00002600',    
    "Drizzle" : u'\U0001F327',
    "Rain" : u'\U00002614',     
    "Thunderstorm" : u'\U0001F329',
    "Snow" : u'\U00002744',
    "Haze" : u'\U0001F32B',
    "Fog" : u'\U0001F32B',
    "Mist" : u'\U0001F32B',
    "Torando" : u'\U0001F32A',
    }

owm = OWM(my_keys.owm_api_key)


def location(city_name):
    mgr1=owm.geocoding_manager()
    location_by_name=mgr1.geocode(city_name,limit=3)
    city_cord=location_by_name[0]
    lat=city_cord.lat
    lon=city_cord.lon
    return lat,lon


def dir(angle):
    directions = ['↑ N', '↗ NE', '→ E', '↘ SE', '↓ S', '↙ SW', '← W', '↖ NW']
    return directions[round(angle / 45) % 8]    


def local_time(utc,timezone):
    iso = dp.parse(utc)
    localtime=iso.astimezone(pytz.timezone(timezone))
    localtime=localtime.strftime("%I:%M:%S %p")
    return localtime
    

def weather(city):
    lat,lon=location(city)
    mgr = owm.weather_manager()
    one_call=mgr.one_call(lat,lon)
    wr=mgr.weather_at_coords(lat,lon).weather
    mgr2=owm.airpollution_manager()
    air_status = mgr2.air_quality_at_coords(lat,lon)
    mtemp=wr.temperature('celsius')
    oc=one_call.current
    wind = oc.wind('km_hour')
    current_time = dp.parse(oc.reference_time('iso')).astimezone(pytz.timezone(one_call.timezone))
    sunrise=local_time(oc.sunrise_time('iso'),one_call.timezone)
    sunset=local_time(oc.sunset_time('iso'),one_call.timezone)
    if oc.status=='Clouds':
        emoji=cloud_emojis[oc.detailed_status]
    else:
        emoji=emojis[oc.status]
    result=f'''
Current Time : {current_time}
Sunrise Time : {sunrise} 
Sunset Time :  {sunset} 
Temperature : {round(mtemp['temp'])}{cel} C
Feels_Like : {round(mtemp['feels_like'])}{cel} C
Min Temp   : {round(mtemp['temp_min'])}{cel} C
Max Temp   : {round(mtemp['temp_max'])}{cel} C
Dew Point : {round(oc.dewpoint-273.15)}{cel} C
Wind_Speed : {dir(wind['deg'])} {round(wind['speed'])} km/h
Humidity : {oc.humidity} %
Pressure : {oc.pressure['press']} mb
Clouds : {oc.clouds} %
Visibility : {oc.visibility('kilometers')} kms
Weather_Status : {oc.detailed_status} {emoji}
Precipitation : {oc.precipitation_probability}
Rain : {oc.rain} 
UV Index : {round(oc.uvi)}
Air Quality Index : {quality[air_status.aqi]}
PM 2.5 Levels : {air_status.pm2_5}
PM 10 Levels : {air_status.pm10}
'''
    return result


def weather_result(update:Update,context:CallbackContext): 
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    city=' '.join(map(str,context.args))
    if city == '':
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,text="Please type the city name like \"/weather Pondicherry\".\n")
    else:
        context.bot.send_chat_action(update.effective_chat.id,'typing')
        context.bot.send_message(update.effective_chat.id,text="Displaying Results for "+city)
        try:
            result_weather=weather(city)
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            context.bot.send_message(update.effective_chat.id,result_weather)
        except:
            context.bot.send_chat_action(update.effective_chat.id,'typing')
            context.bot.send_message(update.effective_chat.id,text="City does not exist!!")
 