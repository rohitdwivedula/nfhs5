import os
import pandas as pd
import requests

links = pd.read_csv("districtwise_links.csv")

for index, row in links.iterrows():
    print(f"Downloading {row['district']} or {row['state']}")
    url = "http://rchiips.org/nfhs/" + row['link']
    r = requests.get(url, allow_redirects=True)
    statename = row['state'].lower().replace(' ', '_').replace('(','').replace(')','')
    districtname = row['district'].lower().replace(' ', '_').replace('(','').replace(')','')
    os.makedirs(f"reports/{statename}", exist_ok=True)
    with open(os.path.join(f"reports/{statename}", districtname), 'wb') as f:
        f.write(r.content)