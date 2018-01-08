# -*- coding: utf-8 -*-
# 爬取similarweb該網址geogrphy traffic和該網址資訊
from bs4 import BeautifulSoup
from login import login
import requests
import json
import csv
import time
import datetime
import urllib
import os
import calendar



def collect_web(file_name):
	'''Collect websites from a file.
	Args:
		file_name:excel file's name, with websites at first column  

	Return:
		webs:Websites collection list 
	'''
	webs = []
	with open(file_name, "r") as f:
		reader = csv.reader(f, delimiter = ",")
		next(reader, None)  # ignore column name
		for i in reader:
			webs.append(i[0])

	return webs

def collect_country(file_name):
	'''Collect country names and codes mapping
	Args:
		file_name:exel file's, with country names and codes

	Return:
		countries:Countries collection dictionary
	'''
	countries = {}
	with open(file_name, "r") as f:
		reader = csv.reader(f, delimiter = ",")
		next(reader, None)  # ignore column name
		for i in reader:
			countries[i[0]] = i[2]
	
	return countries


def similarweb_crawler(file_name):

	webs = collect_web(file_name)
	countries = collect_country("../code info/country_code.csv")

	s = login()
	print "There are " + str(len(webs)) + " websites needs to crawl."
	
	headers = {
		"referer":"https://pro.similarweb.com/",
		"user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
		"authority":"pro.similarweb.com",
		"method":"GET",
		"path":"/api/startup",
		"scheme":"https"
	}
	
	# category traffic data
	data_category = []
	data_category.append(["web", "Country traffic rank", "Country code", "Country", "Traffic share", "Avg. Visit Duration", "PagePerVisit", "BounceRate", "Rank"])
	# info data
	data_info = []
	data_info.append(["web", "main Domain Name", "tags", "global Ranking", "category", "category Ranking", "highest Traffic Country", "highest Traffic Country Ranking"])

	# date for url
	date_to = datetime.datetime.now()
	day = date_to.day
	
	if day < 15:
		last_month_day = calendar.monthrange(date_to.year, date_to.month)[1]
		date_to = date_to - datetime.timedelta(days = day+last_month_day)
		date_from = datetime.datetime.now() - datetime.timedelta(days = 90 + day + last_month_day)
	
	if day > 15:
		date_to = date_to - datetime.timedelta(days = day)
		date_from = datetime.datetime.now() - datetime.timedelta(days = 60 + day)
		
	date_to = str(date_to.year) + "|" + str(date_to.month).zfill(2) + "|" + str(date_to.day).zfill(2)
	date_from = str(date_from.year) + "|" + str(date_from.month).zfill(2) + "|" + str(date_from.day).zfill(2)
	

	for web in webs:
		print web

		# WEB info
		url = "https://pro.similarweb.com/api/websiteanalysis/getheader?includeCrossData=true&keys=" + web + "&mainDomainOnly=true"
		try:
			res = s.get(url, headers = headers)
		except:
			continue
		
		try:
			js = json.loads(res.text)[web]
		except:
			continue

		# websites info
		highestTrafficCountry = js["highestTrafficCountry"]

		if highestTrafficCountry == 0:
			print web + " NO DATA."
			data_category.append([web])
			data_info.append([web])
			continue

		tags = ""
		for i in js["tags"]:
			tags = tags + i.encode("utf-8", "ignore") + "\n"
		
		mainDomainName = js["mainDomainName"]
		tags = tags.strip()
		globalRanking = js["globalRanking"]
		category = js["category"]
		categoryRanking = js["categoryRanking"]
		highestTrafficCountry = js["highestTrafficCountry"]
		highestTrafficCountryRanking = js["highestTrafficCountry"]
		
		data_info.append([web, mainDomainName, tags, globalRanking, category, categoryRanking, highestTrafficCountry, highestTrafficCountryRanking])

		
		# Geography statistics
		url = "https://pro.similarweb.com/widgetApi/WebsiteGeographyExtended/GeographyExtended/Table?country=999&from=" + urllib.quote(date_from) + "&includeSubDomains=true&isWindow=false&keys=" + web + "&metric=GeographyExtended&orderBy=TotalShare+desc&timeGranularity=Monthly&to=" + urllib.quote(date_to)
		res = s.get(url, headers = headers)

		ratio_ranking = 1

		try:
			js = json.loads(res.text)
		except:
			continue

		for i in js["Data"][:5]:
			country_code = i["Country"]
			ratio = round(i["Share"]*100, 2) # 國家流量佔比
			AvgVisitDuration = round(i["AvgVisitDuration"], 2) # 平均造訪停留時間
			PagePerVisit = round(i["PagePerVisit"], 2) # 訪客瀏覽平均頁數
			BounceRate = round(i["BounceRate"], 2)# 進入網站後在特定時間內只瀏覽了一個網頁就離開的訪客百分比
			Rank = i["Rank"] # country ranking
			data_category.append([web, ratio_ranking, country_code, countries[str(country_code)], ratio, AvgVisitDuration, PagePerVisit, BounceRate, Rank])
			ratio_ranking += 1
				
		print web + " is DONE!"
		time.sleep(3)
	
	file_name = file_name[(file_name.rfind("/")+1):-4]
	with open(file_name + "_WEB Geography Traffice.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data_category)

	with open(file_name + "_WEB info.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data_info)

	print "Done!"




