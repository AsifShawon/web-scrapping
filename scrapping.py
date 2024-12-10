import requests
from bs4 import BeautifulSoup

city = input("Enter the city name: ")
query = f"accuweather {city}"

api_key = "695ed88fdb5f48278f0e3409a0975159"  
url = f"https://api.bing.microsoft.com/v7.0/search?q={query}"

headers = {"Ocp-Apim-Subscription-Key": api_key}

# Send request
response = requests.get(url, headers=headers)

def get_wether_info(link):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    html_req = requests.get(link, headers=headers)
    soup = BeautifulSoup(html_req.text, 'lxml')
    weather_info = soup.find('div', class_='temp').text
    print(f"Weather info: {weather_info}")


if response.status_code == 200:
    results = response.json()
    if 'webPages' in results:
        first_link = results['webPages']['value'][0]['url']
        print(f"First result link: {first_link}")
        get_wether_info(first_link)
    else:
        print("No results found.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
