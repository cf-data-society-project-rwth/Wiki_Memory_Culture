import requests
import json
import pandas as pd
import numpy as np


# get translated article of Wikipedia
reader = pd.read_csv('finalize with cat/resultwithcategory.csv', header=None, encoding = 'utf8', delimiter=';')
fout = open("indo_article/resultindo.txt", "w", encoding="utf-8")
file_map = open("indo_article/maptranslated_resultindo.csv", "w", encoding="utf-8")
np_array = np.array(reader)
np.transpose(np_array)
top_list = []
counter = 0
for row in np_array:
    article = row[0]
    file_map.write(article+";")
    url = "https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles=" + article + "&languages=en&format=json"
    resp = requests.get(url)
    if resp.status_code == 200:
        print(counter)
        result = resp.text
        new_dict = json.loads(result)
        articles = new_dict["entities"]
        for ids in articles.values():
            if "sitelinks" in ids:
                if "idwiki" in ids["sitelinks"]:
                    name = ids["sitelinks"]["idwiki"]["title"]
                    name = name.replace(" ", "_")
                    fout.write(name + '\n')
                    file_map.write(name + '\n')
                else:
                    file_map.write('\n')
            else:
                file_map.write('\n')
    counter += 1
fout.close()
