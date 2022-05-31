from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# ---------- FREE API KEY examples ---------------------

owm = OWM('c1e8bfbc1e802cd9ef2e31f0309d3499')
mgr = owm.weather_manager()


# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('Kolkata,India')
w = observation.weather

print(w.detailed_status)     # 'clouds'
print(w.wind())                  # {'speed': 4.6, 'deg': 330}
print(w.humidity)             # 87
print(w.temperature('celsius')) # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
print(w.rain)                   # {}
print(w.clouds)                # 75




