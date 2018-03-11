"""Stock Market Scraper

Scrape and return KOSPI and KOSDAQ INDEX of Korean Stock Market"""

from bs4 import BeautifulSoup
import requests


def get_stock_index(request):
	"""Return requested KOSPI/KOSDAQ Index by scraping from KRX.co.kr"""

	# headers = {"User-Agent": "Mozilla/5.0"}
	req = requests.get("http://www.krx.co.kr/main/main.jsp")
	html = req.text
	soup = BeautifulSoup(html, "html.parser")
	index = soup.findAll("span", {"class": "index-price"})

	if request == '코스피':
		index = index[1].get_text()
	else:
		index = index[3].get_text()

	return index


def get_stock_price(request):
	""" Return Stock price of the requested company code"""

	headers = {"User-Agent": "Mozilla/5.0"}
	req = requests.get('http://finance.naver.com/item/main.nhn?code='+request, headers=headers)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	price = soup.findAll('span', {'class': 'blind'}) 
	

	return price[21].get_text()



