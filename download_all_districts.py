import os
import pandas as pd
import requests

links = pd.read_csv("districtwise_links.csv")

for index, row in links.iterrows():
    print(f"Downloading {row['district']} or {row['state']}")
    url = "http://rchiips.org/nfhs/" + row['link']
    r = requests.get(url, allow_redirects=True)
    statename = row['state'].lower().replace('&', '').replace(' ', '_').replace('(','').replace(')','')
    districtname = row['district'].lower().replace('&', '').replace(' ', '_').replace('(','').replace(')','')
    os.makedirs(f"districtwise_data/pdfs/{statename}", exist_ok=True)
    with open(os.path.join(f"districtwise_data/{statename}", districtname), 'wb') as f:
        f.write(r.content)