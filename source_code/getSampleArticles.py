import requests
import json

# getting top 1000 visited pages of each month from July 2015 to Oct 2018 (total more than 10.000 distinct articles)
# api link source: https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews
top_list = []
file = open("top_1000_ranked_pages.txt", "w", encoding="utf-8")
for year in range(2015, 2019):

    if year < 2016:
        i = 7
    else:
        i = 1

    if year > 2017:
        month = 11
    else:
        month = 13

    while i < month:
        x = str(i)
        if len(x) < 2:
            x = "0" + x
        else:
            x = x

        resp1 = requests.get('https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/'+str(year)+'/' + x + '/all-days')
        if resp1.status_code == 200:
            result = resp1.text
            new_dict = json.loads(result)
            article_list = new_dict["items"][0]["articles"]
            loop_list = 0
            while loop_list < len(article_list):
                name = article_list[loop_list].get("article")
                exclusion = "main_page 404.php xhamster Halaman_utama"
                exclusion1 = "special:"
                exclusion2 = "template:"
                if (name.lower() not in exclusion) and (exclusion1 not in name.lower()) and (exclusion2 not in name.lower()):
                    if len(top_list) < 1:
                        top_list = [name]
                    else:
                        top_list.append(name)
                loop_list += 1
        i += 1
    year += 1

a = 0
final_list = [b for n, b in enumerate(top_list) if b not in top_list[:n]]  # Excluding the duplicates
# storing the top visited pages in csv file
while a < len(final_list):
    if a == (len(final_list) - 1):
        new_line = ""
    else:
        new_line = "\n"
    file.write(final_list[a] + new_line)
    print(final_list[a])
    a += 1

file.close()
# finished getting top 1000 visited pages
