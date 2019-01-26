import pandas as pd
import numpy as np
import statistics as st
import matplotlib.pyplot as plt
import mplcursors


class Article:  # class for storing each article as object
    def __init__(self):
        self.name = ""
        self.category = ""
        self.dates = ""
        self.avgpercent = 0.0

    def setname(self, name):
        self.name = name

    def setdates(self, dates):
        self.dates = dates

    def setcategory(self, category):
        self.category = category

    def setavgpercent(self, avgpercent):
        self.avgpercent = avgpercent


def arrange_name(name):
    name_explode = name.split('_')
    name_string = ''
    for part in name_explode:
        name_string = name_string + ' ' + part
    return name_string


hist_articles = []
nat_articles = []
sci_articles = []
rel_articles = []
tech_articles = []
death_articles = []
birth_articles = []
hist = []
nat = []
sci = []
rel = []
tech = []
death = []
birth = []
peak_dates = []
names = []
reader = pd.read_csv('new_indo_stddev_result.csv', header=None, encoding='utf8', delimiter=';')
np_array = np.array(reader)
np.transpose(np_array)
for row in np_array:
    myarticle = Article()
    myarticle.setname(row[0])
    myarticle.setcategory(row[1])
    view1 = row[2]
    view2 = row[7]
    view3 = row[12]
    if len(row) > 17:
        if pd.isnull(row[17]):
            view4 = 0
        else:
            view4 = row[17]
    else:
        view4 = 0

    if view4 != 0:
        list = [view1, view2, view3, view4]
    else:
        list = [view1, view3, view3]
    avg = st.mean(list)
    myarticle.setavgpercent(avg)
    date1 = row[5]
    date2 = row[10]
    date3 = row[15]
    if len(row) > 20:
        if pd.isnull(row[20]):
            date4 = ''
        else:
            date4 = '\n'+row[20]
    else:
        date4 = ''
    dates = date1+'\n'+date2+'\n'+date3+date4
    myarticle.setdates(dates)
    if myarticle.category == 'HIST':
        hist_articles.append(myarticle)
    elif myarticle.category == 'NAT':
        nat_articles.append(myarticle)
    elif myarticle.category == 'SCI':
        sci_articles.append(myarticle)
    elif myarticle.category == 'TECH':
        tech_articles.append(myarticle)
    elif myarticle.category == 'REL':
        rel_articles.append(myarticle)
    elif myarticle.category == 'DEATH':
        death_articles.append(myarticle)
    elif myarticle.category == 'BIRTH':
        birth_articles.append(myarticle)

for record in hist_articles:
    hist.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in nat_articles:
    nat.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in sci_articles:
    sci.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in tech_articles:
    tech.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in rel_articles:
    rel.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in death_articles:
    death.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

for record in birth_articles:
    birth.append(record.avgpercent)
    arranged_name = arrange_name(record.name)
    names.append(arranged_name)

fig, ax = plt.subplots()
temp_length = len(hist)+len(nat)+len(sci)+len(tech)+len(rel)+len(death)+len(birth)

bar_width = 0.9

start_point = 0
end_point = 0
prev_len = 0

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []

if len(hist) > 0:
    end_point += len(hist)
    index_1 = np.arange(start_point,len(hist))
    list1 = index_1.tolist()
    prev_len = end_point

if len(nat) > 0:
    start_point = prev_len + 1
    end_point += len(nat) + 1
    index_2 = np.arange(start_point,end_point)
    list2 = index_2.tolist()
    prev_len = end_point

if len(sci) > 0:
    start_point = prev_len + 1
    end_point += len(sci)+ 1
    index_3 = np.arange(start_point,end_point)
    list3 = index_3.tolist()
    prev_len = end_point

if len(tech) > 0:
    start_point = prev_len + 1
    end_point += len(tech) + 1
    index_4 = np.arange(start_point,end_point)
    list4 = index_4.tolist()
    prev_len = end_point

if len(rel) > 0:
    start_point = prev_len + 1
    end_point += len(rel) + 1
    index_5 = np.arange(start_point,end_point)
    list5 = index_5.tolist()
    prev_len = end_point

if len(death) > 0:
    start_point = prev_len + 1
    end_point += len(death) + 1
    index_6 = np.arange(start_point,end_point)
    list6 = index_6.tolist()
    prev_len = end_point

if len(birth) > 0:
    start_point = prev_len + 1
    end_point += len(birth) + 1
    index_7 = np.arange(start_point,end_point)
    list7 = index_7.tolist()
    prev_len = end_point

combined_list = list1+list2+list3+list4+list5+list6+list7
combined_content = hist + nat + sci + tech + rel + death + birth

opacity = 0.4
error_config = {'ecolor': '0.3'}

# Visualisation using library matplotlib
# https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
if len(list1) > 0:
    ax.bar(index_1, hist, bar_width,
                alpha=opacity, color='b', error_kw=error_config,
                label='Historical events')

if len(list2) > 0:
    ax.bar(index_2, nat, bar_width,
                alpha=opacity, color='r', error_kw=error_config,
                label='National events')

if len(list3) > 0:
    ax.bar(index_3, sci, bar_width,
                alpha=opacity, color='g', error_kw=error_config,
                label='Natural/Scientific events')

if len(list4) > 0:
    ax.bar(index_4, tech, bar_width,
                alpha=opacity, color='y', error_kw=error_config,
                label='Technology events')

if len(list5) > 0:
    ax.bar(index_5, rel, bar_width,
                alpha=opacity, color='m', error_kw=error_config,
                label='Religious events')

if len(list6) > 0:
    ax.bar(index_6, death, bar_width,
                alpha=opacity, color='k', error_kw=error_config,
                label='Death events')

if len(list7) > 0:
    ax.bar(index_7, birth, bar_width,
                alpha=opacity, color='c', error_kw=error_config,
                label='Birthday events')

ax.set_xlabel('Articles')
ax.set_ylabel('Average number of views')
ax.set_title('Wiki Yearly Events')
ax.set_xticks(combined_list)
ax.set_xticklabels(names, rotation=90, size = 6)
ax.legend()

# interactive hover using mpl cursor https://mplcursors.readthedocs.io/en/stable/
cursor = mplcursors.cursor(hover=True)


@cursor.connect("add")
def on_add(sel):
    label = sel.artist.container.get_label()
    if 'hist' in label.lower():
        date_pop = hist_articles[sel.target.index].dates
    elif 'nat'in label.lower():
        date_pop = nat_articles[sel.target.index].dates
    elif 'sci'in label.lower():
        date_pop = sci_articles[sel.target.index].dates
    elif 'tech'in label.lower():
        date_pop = tech_articles[sel.target.index].dates
    elif 'rel'in label.lower():
        date_pop = rel_articles[sel.target.index].dates
    elif 'death'in label.lower():
        date_pop = death_articles[sel.target.index].dates
    elif 'birth'in label.lower():
        date_pop = birth_articles[sel.target.index].dates

    sel.annotation.set(text=date_pop, ha="center", va="bottom")


fig.tight_layout()
plt.show()
