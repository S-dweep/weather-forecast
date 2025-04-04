import requests

API_KEY = "922dc3750bb101c1a2632b10a640ec43"


# collecting data from api
def get_data(place, days):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"][:8 * days]
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Kolkata", days=3))
