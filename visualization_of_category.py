import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


reader = pd.read_csv('finalize with cat/argrelmax50withcategory.csv', header=None, encoding='utf8', delimiter=';')
np_array = np.array(reader)
np.transpose(np_array)
hist_count = 0
nat_count = 0
sci_count = 0
tech_count = 0
rel_count = 0
death_count = 0
birth_count = 0

for row in np_array:
    category = row[1]
    if category == 'HIST':
        hist_count += 1
    elif category == 'NAT':
        nat_count += 1
    elif category == 'SCI':
        sci_count += 1
    elif category == 'TECH':
        tech_count += 1
    elif category == 'REL':
        rel_count += 1
    elif category == 'DEATH':
        death_count += 1
    elif category == 'BIRTH':
        birth_count += 1

fig, ax = plt.subplots()

bar_width = 0.4
opacity = 0.4
error_config = {'ecolor': '0.3'}

countlist = [hist_count, nat_count, sci_count, tech_count, rel_count, death_count, birth_count]
index = np.arange(len(countlist))

reader = pd.read_csv('german results/argrelmax75withcategory.csv', header=None, encoding = 'utf8', delimiter=';')
np_array = np.array(reader)
np.transpose(np_array)
hist_count = 0
nat_count = 0
sci_count = 0
tech_count = 0
rel_count = 0
death_count = 0
birth_count = 0

for row in np_array:
    category = row[1]
    if category == 'HIST':
        hist_count += 1
    elif category == 'NAT':
        nat_count += 1
    elif category == 'SCI':
        sci_count += 1
    elif category == 'TECH':
        tech_count += 1
    elif category == 'REL':
        rel_count += 1
    elif category == 'DEATH':
        death_count += 1
    elif category == 'BIRTH':
        birth_count += 1

bar_width = 0.4
opacity = 0.4
error_config = {'ecolor': '0.3'}

countlist2 = [hist_count, nat_count, sci_count, tech_count, rel_count, death_count, birth_count]
index2 = np.arange(len(countlist), len(countlist) + len(countlist2))

reader = pd.read_csv('indo_with_rank/argrelmax75indos.csv', header=None, encoding = 'utf8', delimiter=';')
np_array = np.array(reader)
np.transpose(np_array)
hist_count = 0
nat_count = 0
sci_count = 0
tech_count = 0
rel_count = 0
death_count = 0
birth_count = 0

for row in np_array:
    category = row[1]
    if category == 'HIST':
        hist_count += 1
    elif category == 'NAT':
        nat_count += 1
    elif category == 'SCI':
        sci_count += 1
    elif category == 'TECH':
        tech_count += 1
    elif category == 'REL':
        rel_count += 1
    elif category == 'DEATH':
        death_count += 1
    elif category == 'BIRTH':
        birth_count += 1

bar_width = 0.4
opacity = 0.4
error_config = {'ecolor': '0.3'}

countlist3 = [hist_count, nat_count, sci_count, tech_count, rel_count, death_count, birth_count]
index3 = np.arange(len(countlist) + len(countlist2), len(countlist) +  len(countlist2) + len(countlist3))

# Visualisation using library matplotlib
# https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
ax.bar(index, countlist, bar_width,
                alpha=opacity, color=('b'), error_kw=error_config,
                label='English')

ax.bar(index2, countlist2, bar_width,
                alpha=opacity, color=('r'), error_kw=error_config,
                label='German')

ax.bar(index3, countlist3, bar_width,
                alpha=opacity, color=('g'), error_kw=error_config,
                label='Bahasa Indonesia')

ax.set_xlabel('Categories')
ax.set_ylabel('Total Articles Based on Yearly Events')
ax.set_title('Wiki Yearly Events')
ax.set_xticks(index.tolist() + index2.tolist() + index3.tolist())
ax.set_xticklabels(['HISTORICAL EVENTS', 'NATIONAL EVENTS', 'NATURAL/SCIENTIFIC EVENTS', 'TECHNOLOGICAL EVENTS', 'RELIGIOUS EVENTS', 'DEATHS', 'BIRTHDAYS', 'HISTORICAL EVENTS', 'NATIONAL EVENTS', 'NATURAL/SCIENTIFIC EVENTS', 'TECHNOLOGICAL EVENTS', 'RELIGIOUS EVENTS', 'DEATHS', 'BIRTHDAYS', 'HISTORICAL EVENTS', 'NATIONAL EVENTS', 'NATURAL/SCIENTIFIC EVENTS', 'TECHNOLOGICAL EVENTS', 'RELIGIOUS EVENTS', 'DEATHS', 'BIRTHDAYS'], rotation=90)
ax.legend()

fig.tight_layout()
plt.show()