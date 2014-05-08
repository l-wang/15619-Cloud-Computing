#!/usr/bin/python
import sys

dateviews={}

oldArticle = None
sum = 0
limit = 100000
# limit = 0

for line in sys.stdin:
    article,info=line.split("\t")   # #info is like 201306010000001

    date=info[0:8]      # 20130601
    hour=info[8:14]     # 000000
    views=info[14:]     # 1

    if oldArticle != article:    # New article
        if oldArticle!=None and sum>limit:
            print oldArticle + '\t' + str(sum) + "\t"+ "\t".join([d + ":" + str(v) for d,v in dateviews.items()])
        oldArticle = article
        sum = int(views)
        dateviews.clear()
        dateviews[str(date)] = int(views)
    else:       # Same old article
        oldArticle = article
        sum += int(views)
        if str(date) in dateviews:
            dateviews[str(date)] += int(views)
        else:
            dateviews[str(date)] = int(views)
        


if oldArticle and sum>limit:
    print oldArticle + '\t' + str(sum) + "\t"+ "\t".join([d + ":" + str(v) for d,v in dateviews.items()])
# <total month views>\t<article name>\t<date1:page views for date1>\t <date2:page views for date2> ...    

