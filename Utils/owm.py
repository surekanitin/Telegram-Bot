from pyowm.owm import OWM
from Data.my_keys import owm_api_key
from telegram import Update
from telegram.ext import CallbackContext
import pytz, dateutil.parser

cel= u'\N{DEGREE SIGN}'
owm = OWM(owm_api_key)
#part='minutely'
#units='metric'
#lat=13.067439
#lon=80.237617
#url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units={units}&exclude={part}&appid={owm_api_key}"
quality=[" ","Good","Fair","Moderate","Poor","Very Poor"]
mgr = owm.weather_manager()
mgr2=owm.city_id_registry()
mgr1=owm.geocoding_manager()
mgr3=owm.airpollution_manager()
# print("Enter the name of the city: ",end="")
# city_name= input()
def location(city_name):
    location_by_name=mgr1.geocode(city_name,limit=3)
    city_cord=location_by_name[0]
    lat=city_cord.lat
    lon=city_cord.lon
    return lat,lon

def dir(angle):
    directions = ['↑ N', '↗ NE', '→ E', '↘ SE', '↓ S', '↙ SW', '← W', '↖ NW']
    return directions[round(angle / 45) % 8]


#location_by_cord = mgr1.reverse_geocode(lat, lon) 

def current(lat,lon):
    one_call=mgr.one_call(lat,lon)
    oc=one_call.current 
    temp=oc.temperature('celsius')
    wind = oc.wind('km_hour')
    air_status = mgr3.air_quality_at_coords(lat,lon)
    utctime = dateutil.parser.parse(oc.reference_time('iso'))
    localtime = utctime.astimezone(pytz.timezone(one_call.timezone))
    result=f'''
Time : {localtime}
Temperature : {round(temp['temp'])}{cel} C
Feels_Like : {round(temp['feels_like'])}{cel} C
Dew Point : {round(oc.dewpoint)-273}{cel} C
Wind_Speed : {dir(wind['deg'])}{ round(wind['speed'])} km/h
Humidity : {oc.humidity} %
Pressure : {oc.pressure['press']} mb
Clouds : {oc.clouds} %
Visibility : {oc.visibility('kilometers')} kms
Weather_Status : {oc.detailed_status}
UV Index : {round(oc.uvi)}
Air Quality Index : {quality[air_status.aqi]}
PM 2.5 Levels : {air_status.pm2_5}
PM 10 Levels : {air_status.pm10}
'''
    return result
    

# result_current=current(lat,lon)
# print(result_current)

def weatherbycity(update:Update,context:CallbackContext): 
    context.bot.send_chat_action(update.effective_chat.id, 'typing')
    city=' '.join(map(str,context.args))
    lat,lon=location(city)
    result_current=current(lat,lon)
    context.bot.send_chat_action(update.effective_chat.id,'typing')
    context.bot.send_message(update.effective_chat.id,result_current)





