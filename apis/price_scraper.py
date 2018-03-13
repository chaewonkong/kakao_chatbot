"""Stock Market Scraper

Scrape and return KOSPI and KOSDAQ INDEX of Korean Stock Market"""

from bs4 import BeautifulSoup
import requests


def get_stock_price(request):
	""" Return Stock price of the requested company code"""

	headers = {"User-Agent": "Mozilla/5.0"}
	req = requests.get('http://finance.naver.com/item/main.nhn?code='+request, headers=headers)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	price = soup.findAll('span', {'class': 'blind'}) 
	

	return price[21].get_text()



