import requests
"""
This API parses data from a weather information database. This implementation specifically retreives 
temperature and wind speed based on the city chosen.

note: for future reference, http get request returns a status code
note2: 

# this api's response.json specifically returns a dictionary, when a valid city is entered
    Ex:
        { "coord": {"lon": -84.388, "lat": 33.749}, "weather": [{"id": 800,"main": "Clear","description": "clear sky","icon": "01n"}],
        "base": "stations", "main": {"temp": 292.47, "feels_like": 292.6, "temp_min": 290.75, "temp_max": 293.65,
        "pressure": 1021, "humidity": 82, "sea_level": 1021, "grnd_level": 987},"visibility": 10000,"wind": {
        "speed": 0.45, "deg": 152, "gust": 1.79},"clouds": {"all": 0},"dt": 1743846431, "sys": {"type": 2, "id": 2006620,"country": "US",
        "sunrise": 1743851952,"sunset": 1743897643},"timezone": -14400,"id": 4180439,"name": "Atlanta","cod": 200}
        more ex: reponses can be found on rapid api website
    
"""
def get_city_temp_wspd(city):

    # A correct return from the get_city_temp_wdsp looks like: {'temperature': 42, 'wind speed': 0}

    url = "https://weather-api138.p.rapidapi.com/weather"

    headers = {
	"x-rapidapi-key": "57196037fdmsh90d56e037ea94bep1b9d40jsn595913a15546",
	"x-rapidapi-host": "weather-api138.p.rapidapi.com"
    }

    # uses my city string parameter to look for the information in 
    # the dictionary I want to use. (note: Think of this as the outer keys of a large dictionary of dictionaries)
    querystring = {"city_name": city}
    response = requests.get(url, headers=headers, params=querystring)
    weather_data = response.json()
    city_data_to_return = {}

    # check the status_code instance variable of the response, 200 means the input used for the city request was appropriate and has data that can be pulled
    if response.status_code != 200:
        return {"error": "Failed to fetch data. Please try again later."}

    elif "main" not in weather_data or "wind" not in weather_data: # if "main" and "wind" keys containing temp and wind speed data are missing, throw an error
        return {"error": 'City data in weather_data for ' + city + " is missing. Try again."}

    elif "speed" not in weather_data["wind"] or "temp" not in weather_data["main"]: # if "temp" and "speed" sub keys are missing, throw an error
        return {"error": 'City data in weather_data for ' + city + " is missing. Try again."}
    
    else:
        kelvin_temp = weather_data["main"]["temp"]
        city_data_to_return["temperature"] = int((kelvin_temp - 273.15) * (9/5) + 32) # convert to fahrenheit
        city_data_to_return["windspeed"] = int(weather_data["wind"]["speed"])
        return city_data_to_return

if __name__ == "__main__":
    city = input("Enter a city: ")
    print(get_city_temp_wspd(city))
