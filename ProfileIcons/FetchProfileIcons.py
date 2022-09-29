import requests
import json
import shutil

x = requests.get(
    "http://ddragon.leagueoflegends.com/cdn/12.18.1/data/en_US/profileicon.json").json()

images = x.get("data")
for k,v in images.items():
    url = images[k]["image"]["full"]
    print(f"Downloading Profile Icon {url}...")
    y = requests.get(
        f"http://ddragon.leagueoflegends.com/cdn/12.18.1/img/profileicon/{url}", stream=True)
    with open(f'./ProfileIcons/{url}', 'wb') as out_file:
        shutil.copyfileobj(y.raw, out_file)
    


