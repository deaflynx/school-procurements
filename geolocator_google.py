import pandas as pd 
from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter


API = ""
PATH = ""

df = pd.read_excel(PATH, dtype=str)
geolocator = GoogleV3(api_key=API)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df["location"] = df["Address"].apply(geocode)
df["Longitude"] = df["location"].apply(lambda loc: loc.longitude if loc else "ERROR")
df["Latitude"] = df["location"].apply(lambda loc: loc.latitude if loc else "ERROR")
df.to_excel("./data/coordinates.xlsx", index=False)