import requests
import json
import statistics


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


def calculateMaxDailyVisit(month, year, article):   # Getting exact peak dates of an article
    maxVisit = 0
    peakDate = None
    endDate = None
    if int(month) == 1 or int(month) == 3 or int(month) == 5 or int(month) == 7 or int(month) == 8 or int(month) == 10 or int(month) == 12:
        endDate = "31"
    elif int(month) == 4 or int(month) == 6 or int(month) == 9 or int(month) == 11:
        endDate = "30"
    else:
        endDate = "28"
    if int(month) < 10:
        month = "0" + str(month)
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" + article + "/daily/" + year + str(month) + "0100/" + year + str(month) + endDate + "00"
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
fout = open("new_stddev_result.csv", "w", encoding="utf8")

for line in f:
    mylist = []
    templist = []
    yearlyeventlist = []
    peakDateList = []
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
            stdev = statistics.stdev(myarticle.visits)
            mean = statistics.mean(myarticle.visits)
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

            i = 7
            noOfPeaks = 0
            total_views = sum(myarticle.visits)
            # algorithm to check and get the peak views of each page
            # reference: https://stats.stackexchange.com/questions/41145/simple-way-to-algorithmically-identify-a-spike-in-recorded-errors
            while i < 7 + len(myarticle.visits):
                factor = (myarticle.visits[i - 7] - mean) / stdev
                if factor >= 2:
                    checkYearly = False
                    length = len(myarticle.monthList)
                    if length != 0:
                        currentMonth = i
                        difference = currentMonth - int(myarticle.monthList[length - 1])
                        if 10 < difference <= 13:
                            checkYearly = True
                    if checkYearly is True or len(myarticle.monthList) == 0:
                        myarticle.setmonthList(i)
                        if i > 12:
                            month = int(i) % 12
                            if month == 0:
                                month = 12
                        else:
                            month = i
                        if 7 <= i <= 12:
                            returnValue = calculateMaxDailyVisit(month, "2015", myarticle.id)
                            if returnValue is not None:
                                peakDate = returnValue + "-" + str(month) + "-2015"
                                month = str(month) + "-2015"
                        elif 13 <= i <= 24:
                            returnValue = calculateMaxDailyVisit(month, "2016", myarticle.id)
                            if returnValue is not None:
                                peakDate = returnValue + "-" + str(month) + "-2016"
                                month = str(month) + "-2016"
                        elif 25 <= i <= 36:
                            returnValue = calculateMaxDailyVisit(month, "2017", myarticle.id)
                            if returnValue is not None:
                                peakDate = returnValue + "-" + str(month) + "-2017"
                                month = str(month) + "-2017"
                        elif 37 <= i <= 46:
                            returnValue = calculateMaxDailyVisit(month, "2018", myarticle.id)
                            if returnValue is not None:
                                peakDate = returnValue + "-" + str(month) + "-2018"
                                month = str(month) + "-2018"
                        yearlyeventlist.append(month)
                        peakDateList.append(peakDate)
                        mylist.append(myarticle.visits[i - 7])
                        noOfPeaks += 1
                    else:
                        break
                i += 1

            print(noOfPeaks)
            if 2 < noOfPeaks <= 4:
                print(article + "is possibly a yearly event")
                for a in myarticle.monthList:
                    print("Peak views in Month: " + str(a))
            else:
                print("Not a yearly event")

            if 2 < noOfPeaks <= 4:
                fout.write(myarticle.id)
                j = 0
                #storing the result into csv file
                while j < noOfPeaks:
                    percentage = round(((mylist[j] * 100) / total_views),2)
                    fout.write(";" + str(mylist[j]))
                    fout.write(";" + str(percentage)+"%")
                    fout.write(";" + yearlyeventlist[j])
                    fout.write(";" + peakDateList[j])
                    print("Peak date on: " + peakDateList[j])
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