import requests
import pandas as pd
import json
import io
import Haiku
"""
fetch weather code
"""
weather_code = requests.get("https://www.worldweatheronline.com/feed/wwoConditionCodes.txt")
print("weather code status: {0}\n".format(weather_code.status_code))
if weather_code.status_code != 200:
        raise Exception("Failed to fetch weather code. GET status code is {0}".format(weather_code.status_code))


"""
clean up weather code
"""
weather_code = weather_code.text.replace("\t", ",")
# print(weather_code)
code_df = pd.read_csv(io.StringIO(weather_code))
# print(len(code_df.index))

"""
fetch weather data
"""
weather_data = requests.get("https://wttr.in/Seattle?format=j1")
if weather_data.status_code != 200:
        raise Exception("Failed to fetch weather data. GET status code is {0}".format(weather_data.status_code))
print("weather data status: {0}\n".format(weather_data.status_code))


"""
parse JSON data
"""
weather_JSON = json.loads(weather_data.text)


"""
Do stuff with JSON data
"""
print("Location: {0}\n".format(weather_JSON["nearest_area"][0]["region"][0]["value"]))
for day in weather_JSON["weather"]:
  print("DATE: " + day["date"])
  for hour in day["hourly"]:
    print("time: {0} Weather Code: {1}, Weather Desc: {2} C:{3} F:{4}"
          .format(hour["time"], hour["weatherCode"], hour["weatherDesc"][0]["value"], hour["tempC"], hour["tempF"]))
    for haiku in Haiku.haikus:
         if hour["weatherCode"] == haiku.code:
              print("Haiku:\n" + haiku.haiku + "\n")