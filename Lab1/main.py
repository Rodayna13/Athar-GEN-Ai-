import os
import requests
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()
API_KEY = os.getenv("MAPTILER_API_KEY")


class Place:

    def __init__(self, name, place_type, longitude, latitude):
        self.name = name
        self.place_type = place_type
        self.longitude = longitude
        self.latitude = latitude

    def summary(self):
        return (
            f"Name      : {self.name}\n"
            f"Type      : {self.place_type}\n"
            f"Latitude  : {self.latitude}\n"
            f"Longitude : {self.longitude}"
        )


def search_places(query):
    if not API_KEY:
        raise ValueError("API key not found. Check your .env file.")

    url = f"https://api.maptiler.com/geocoding/{query}.json"
    params = {"key": API_KEY, "limit": 5}

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # يطلع error لو الطلب فشل
    data = response.json()

    places = []
    for feature in data.get("features", []):
        lon, lat = feature["center"]
        place_type = (feature.get("place_type") or ["unknown"])[0]
        places.append(
            Place(feature.get("place_name", "Unknown"), place_type, lon, lat)
        )
    return places


def main():
    query = input("Enter a place name: ").strip()
    try:
        places = search_places(query)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    if not places:
        print("No results found.")
        return

    print(f"\n===== Results for '{query}' =====")
    for i, place in enumerate(places, start=1):
        print(f"\n--- Result {i} ---")
        print(place.summary())


if __name__ == "__main__":
    main()