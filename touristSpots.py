from bs4 import BeautifulSoup
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from the custom .env file
load_dotenv(dotenv_path="local.env")

class TouristSpots:
    def __init__(self, city):
        self.city = city
        self.api_key = os.getenv("MS_API_KEY")  # Assuming the API key is used elsewhere

    def get_tourist_spots(self):
        # URL of the city-specific tourist spots page
        url = f"http://www.{self.city}.gov.bd/en/site/view/TouristSpot"
        response = requests.get(url)
        
        # Check if the request is successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page for {self.city}. HTTP Status Code: {response.status_code}")
            return []

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find the table that contains the tourist spots
        spots_table = soup.find('table', class_='table table-bordered')
        if not spots_table:
            print("No spots table found.")
            return []

        # Find all rows within the table
        spots_info = spots_table.find_all('tr')

        tourist_spots = []

        # Loop through each row and extract the tourist spot names
        for row in spots_info:
            cells = row.find_all('td')  # Find all table cells in the row
            
            if len(cells) > 1:  
                spot_name = cells[0].text.strip() 
                if "তালিকা" in spot_name:
                    continue
                spot_location = cells[1].text.strip()
                spot_description = cells[2].text.strip()
                spot = {
                    "name": spot_name,
                    "location": spot_location,
                    "description": spot_description
                } 
                tourist_spots.append(spot)

        # Store the result in a JSON file
        data = {"city": self.city, "tourist_spots": tourist_spots}
        with open(f"tourist_spots_{self.city}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        # Return the list of tourist spots
        return tourist_spots
