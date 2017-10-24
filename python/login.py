# -*- coding: utf-8 -*-
# log in similarweb 
from bs4 import BeautifulSoup
import requests


def login():

	s = requests.Session()
	
	email = "email address"
	password = "password"
	
	payload = {
		"userName":email,
		"password":password,
		"munchkinLeadSource":"Pro",
		"captchaAnswer":"",
		"browserId":browserId
	}
	
	headers = {
		"Host":"www.similarweb.com",
		"Origin":"https://www.similarweb.com",
		"Referer":"https://www.similarweb.com/account/logout",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
	}
	
	url = "https://www.similarweb.com/sdk/login"
	res = s.put(url, data = payload)
	return s

