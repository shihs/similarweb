# -*- coding: utf-8 -*-
#  
from login import login
from bs4 import BeautifulSoup
import requests
import json
import csv

def code_info():
	s = login()
	url = "https://pro.similarweb.com/api/startup"
	res = s.get(url)
	# print res.text.encode("utf-8")
	
	js = json.loads(res.text)
	
	# get countries code
	data = []
	data.append(["id", "code", "country"])
	for i in js["countries"]["countriesClient"]:
		data.append([i["id"], i["code"].encode("utf-8", "ignore"), i["text"].encode("utf-8", "ignore")])
	
	with open("country_code.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)
	
	# get categories
	data = []
	data.append(["category", "small category"])
	for i in js["categories"]:
		category = i["name"].encode("utf-8", "ignore")
		for j in i["sons"].keys():
			data.append([category, j])
	
	with open("../code info/category.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)

code_info()