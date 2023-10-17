import requests
import time
import json
import csv

BASE_URL = "https://explorer.moken.io/api/"

def get_location_from_name(hotspot_name):
    # Step 1: Search for the hotspot name to get the identifier
    search_endpoint = BASE_URL + "get-hotspots"
    response = requests.get(search_endpoint, params={"name": hotspot_name})
    data = response.json()
    if not data:  # If no results found
        return None

    # You might want to add error handling in case there are multiple results with the same name.
    # For now, we're just taking the first result.
    hotspot_data = data[0]
    
    # Extract the relevant location data
    lat = hotspot_data['location']['lat']
    lng = hotspot_data['location']['lng']

    # Return the data in the desired format
    return {"name": hotspot_name, "latitude": lat, "longitude": lng}

def save_to_csv(data, filename="hotspots.csv"):
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(["name", "latitude", "longitude"])
        # Write the data
        for item in data:
            writer.writerow([item["name"], item["latitude"], item["longitude"]])


hotspot_names = [
    "Cheesy Jade unicorn",
    "decent pear ant",
    "cuddly peach barracuda",
    "short stone porcupine",
    "wild iron quail",
    "jovial ultraviolet stallion",
    "Large Rainbow Wombat",
    "huge frost bull",
    "petite pineapple dragonfly",
    "howling iron platypus",
    "Energetic Licorice Giraffe",
    "deep glossy chicken",
    "silly pearl sidewinder",
    "fierce scarlet bull",
    "curly olive squid",
    "radiant seaweed gerbil",
    "Basic Fuchsia Shark",
    "long fuzzy sealion",
    "Careful Powder Cougar",
    "Quiet brick mole",
    "Chilly peanut bear",
    "Brisk pebble whale",
    "Bubbly Red Barbel",
    "Brisk myrtle koala",
    "Round paisley liger",
    "mini marigold mammoth",
    "Big viridian woodpecker",
    "Melodic iris wasp",
    "Blunt latte mouse",
    "Oblong daffodil yeti",
    "Strong teal ant",
    "fluffy ocean dachshund",
    "expert cream tadpole",
    "prehistoric rainbow pangolin",
    "mammoth licorice griffin",
    "proper cyan raven",
    "Glamorous Banana Grasshopper",
    "Formal stone alpaca",
    "Slow ultraviolet Hippo",
    "Sneaky amethyst pangolin",
    "perfect latte caterpillar",
    "Lively Latte Stallion",
    "Uneven crepe mantis",
    "Urban Coal alpaca",
    "Small mustard falcon",
    "Best daffodil Python",
    "Energetic pebble pike",
    "hot nylon beaver",
    "real lace hornet",
    "cheesy indigo oyster",
    "short smoke hawk",
    "early mahogany fly",
    "atomic steel wolverine",
    "quiet ivory python"
]

print(len(hotspot_names))

results = []

for name in hotspot_names:
    location = get_location_from_name(name)
    if location:
        results.append(location)

save_to_csv(results)
