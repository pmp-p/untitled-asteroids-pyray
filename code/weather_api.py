import requests
import sys

def get_city_temp_wspd(city):
    # URL of weather api endpoint to collect weather data
    url = "https://cities-temperature.p.rapidapi.com/weather/v1/current"

    headers = {"x-rapidapi-key": "57196037fdmsh90d56e037ea94bep1b9d40jsn595913a15546",
	"x-rapidapi-host": "cities-temperature.p.rapidapi.com"}

    # string contains the city name you want to look up data for
    querystring = {"location": str(city)}

    # make a GET request to the weather api to retreive weather data for a city
    weather = (requests.get(url, headers=headers, params=querystring)).json()

    # extract only the city temperature and wind speed to be used for program
    city_weather_data = {}
    temp = (9/5 * weather["temperature"]) + 32
    wspd = weather["wind_speed"]
    city_weather_data[str(city) + " temperature"] = int(temp)
    city_weather_data[str(city) + " wind speed"] = int(wspd)

    return city_weather_data
    # 0.42 for Oymmyakon
    # 2.06 for Dallas
    # 6 for Perth
if __name__ == "__main__":
    print(get_city_temp_wspd("Perth"))
