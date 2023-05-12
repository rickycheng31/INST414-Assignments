import requests
import pandas as pd
import matplotlib.pyplot as plt

cities = ["New York", "Boston", "Washington, D.C.", "Miami", "Wilmington", "Charlotte","Philadelphia"]
api_key = "e5d59637301e36e5607c5ea52db06c55"
url = "http://api.openweathermap.org/data/2.5/weather"


data = {"City": [],"Temperature": [], "Humidity": []}

for city in cities:
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    json_data = response.json()
    print(json_data)
    if 'main' in json_data:
        temp = json_data['main']['temp']
        humidity = json_data['main']['humidity']
    else:
        humidity = None
        temp = None
        print(f"No temperature data for {city}")
    data["City"].append(city)
    data["Temperature"].append(temp)
    data["Humidity"].append(humidity)

df = pd.DataFrame(data)
df = df.sort_values('Humidity')

plt.bar(df['City'], df['Temperature'])
plt.xlabel('Cities')
plt.ylabel('Temperature')
plt.title('Temperature in Cities(Celsius)')
plt.xticks(rotation=45, ha='right')
plt.ylim(20, None)
plt.show()
