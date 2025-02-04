import requests

def get_city_temp_wspd(city):
    url = "https://cities-temperature.p.rapidapi.com/weather/v1/current"

    headers = {
        "x-rapidapi-key": "57196037fdmsh90d56e037ea94bep1b9d40jsn595913a15546",
        "x-rapidapi-host": "cities-temperature.p.rapidapi.com"
    }

    querystring = {"location": city}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        return {"error": "Failed to fetch data. Please try again later."}

    weather = response.json()

    # Check if the response contains valid weather data
    if not weather or "temperature" not in weather or "wind_speed" not in weather:
        return {"error": f"'{city}' not found. Check the spelling and try again."}

    return {
        f"{city} temperature": int((9/5 * weather["temperature"]) + 32),
        f"{city} wind speed": int(weather["wind_speed"])
    }

if __name__ == "__main__":
    city = input("Enter a city: ")
    print(get_city_temp_wspd(city))
