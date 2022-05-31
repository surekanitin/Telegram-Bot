# importing modules
import requests, json

api_key = "c1e8bfbc1e802cd9ef2e31f0309d3499"

air_url='http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'

def temp(city):
    # API base URL
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + api_key
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        temp_feel_like = main['feels_like']  
        humidity = main['humidity']
        pressure = main['pressure']
        weather_report = data['weather']
        wind_report = data['wind']
        print(f"{city:-^35}")
        print(f"City ID: {data['id']}")   
        print(f"Temperature: {temperature}")
        print(f"Feel Like: {temp_feel_like}")    
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {weather_report[0]['description']}")
        print(f"Wind Speed: {wind_report['speed']}")
        print(f"Time Zone: {data['timezone']}")
    else:
        print("Error in the HTTP request")
    
print("Enter city name: ",end="")
city = input()
temp(city)


