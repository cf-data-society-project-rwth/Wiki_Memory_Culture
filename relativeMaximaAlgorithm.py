import numpy as np
from scipy.signal import argrelmax
import requests
import json


class Article:  # class for storing each article as object
    def __init__(self):
        self.id = ""
        self.visits = []
        self.monthList = []

    def setid(self, id):
        self.id = id

    def appendvisits(self, visit):
        self.visits.append(visit)

    def setvisits(self, visit):
        self.visits = visit

    def setmonthList(self, monthList):
        self.monthList.append(monthList)


def calculateMaxDailyVisit(month, year, article):  # Getting exact peak dates of an article
    maxVisit = 0
    peakDate = None
    endDate = None
    if (int(month) == 1 or int(month) == 3 or int(month) == 5 or int(month) == 7 or int(month) == 8 or int(
            month) == 10 or int(month) == 12):
        endDate = "31"
    elif int(month) == 4 or int(month) == 6 or int(month) == 9 or int(month) == 11:
        endDate = "30"
    else:
        endDate = "28"
    if int(month) < 10:
        month = "0" + str(month)
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + article + "/daily/" + year + str(
        month) + "0100/" + year + str(month) + endDate + "00"
    resp = requests.get(url)
    if resp.status_code == 200:
        y = json.loads(resp.text)
        for a in y["items"]:
            if maxVisit < a["views"]:
                maxVisit = a["views"]
                peakDate = a["timestamp"]
                peakDate = peakDate[-4:-2]
    return peakDate


# getting number of views of each Wikipedia page from july 2015 - oct 2018
# based on the top 1000 articles of each month
f = open("top_1000_ranked_pages.txt", encoding="utf8")
fout = open("new_maxima_result.csv", "w", encoding="utf8")
count = 0

for line in f:
    print(count)
    count += 1
    templist = []
    yearlyeventlist = []
    visitlist = []
    peakDateList = []
    maxVisit = 0
    breakloop = False
    article = line.replace("\n", "")
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + article + "/monthly/2015070100/2018103100"
    resp = requests.get(url)
    if resp.status_code == 200:
        y = json.loads(resp.text)
        myarticle = Article()
        for a in y["items"]:
            myarticle.setid(a["article"])
            myarticle.appendvisits(a["views"])
        if len(myarticle.visits) > 1:
            if len(myarticle.visits) < 40:
                x = 40 - len(myarticle.visits)
                k = 0
                while k < x:
                    templist.append(0)
                    k += 1
                while k < 40:
                    templist.append(myarticle.visits[k - x])
                    k += 1
                del myarticle.visits[:]
                myarticle.setvisits(templist)
            total_views = sum(myarticle.visits)
            example = np.array(myarticle.visits)
            # algorithm to check and get the peak views of each page based on relative maxima
            # ref: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.argrelmax.html
            x = argrelmax(example, order=10)
            peaks = x[0]
            min = np.amin(myarticle.visits)
            max = np.amax(myarticle.visits)
            range = np.arange(min, max)
            p = np.percentile(range, 50)

            i = 0
            while i < len(peaks):
                if myarticle.visits[peaks[i]] < p:
                    breakloop = True
                    break
                if i < len(peaks) - 1:
                    difference = peaks[i + 1] - peaks[i]
                    if difference < 10 or difference > 13:
                        breakloop = True
                        break
                i += 1

            if breakloop:
                continue
            if len(peaks) > 2:
                for a in peaks:
                    temp = a + 7
                    month = temp
                    if temp > 12:
                        month = temp % 12
                        if month == 0:
                            month = 12
                    if 7 <= temp <= 12:
                        returnValue = calculateMaxDailyVisit(month, "2015", myarticle.id)
                        if returnValue is not None:
                            peakDate = returnValue + "-" + str(month) + "-2015"
                            month = str(month) + "-2015"
                    elif 13 <= temp <= 24:
                        returnValue = calculateMaxDailyVisit(month, "2016", myarticle.id)
                        if returnValue is not None:
                            peakDate = returnValue + "-" + str(month) + "-2016"
                            month = str(month) + "-2016"
                    elif 25 <= temp <= 36:
                        returnValue = calculateMaxDailyVisit(month, "2017", myarticle.id)
                        if returnValue is not None:
                            peakDate = returnValue + "-" + str(month) + "-2017"
                            month = str(month) + "-2017"
                    elif 37 <= temp <= 46:
                        returnValue = calculateMaxDailyVisit(month, "2018", myarticle.id)
                        if returnValue is not None:
                            peakDate = returnValue + "-" + str(month) + "-2018"
                            month = str(month) + "-2018"
                    yearlyeventlist.append(month)
                    visitlist.append(myarticle.visits[a])
                    peakDateList.append(peakDate)
                fout.write(myarticle.id)
                # storing the result into csv file
                j = 0
                while j < len(peaks):
                    percentage = round(((visitlist[j] * 100) / total_views), 2)
                    fout.write(";" + str(visitlist[j]))
                    fout.write(";" + str(percentage) + "%")
                    fout.write(";" + str(yearlyeventlist[j]))
                    fout.write(";" + peakDateList[j])
                    yearmonth = yearlyeventlist[j].split('-')
                    if len(yearmonth[0]) == 1:
                        month = '0' + str(yearmonth[0])
                    else:
                        month = str(yearmonth[0])
                    parameter = str(yearmonth[1]) + '/' + month
                    # Check the rank of articles in top 1000
                    resp_rank = requests.get(
                        'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/' + parameter + '/all-days')
                    result_rank = resp_rank.text
                    rank_dict = json.loads(result_rank)
                    rank_list = rank_dict["items"][0]["articles"]
                    rank_loop = 0
                    should_write = False
                    while rank_loop < len(rank_list):
                        name = rank_list[rank_loop].get("article")
                        rank = rank_list[rank_loop].get("rank")
                        if myarticle.id == name:
                            should_write = True
                            fout.write(';' + str(rank))
                            break
                        rank_loop += 1
                    if not should_write:
                        fout.write(';Not in the Top 1000')
                    j += 1
                fout.write("\n")
# FINISH #