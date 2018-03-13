"""Stock Market Scraper

Scrape and return KOSPI and KOSDAQ INDEX of Korean Stock Market"""

from bs4 import BeautifulSoup
import requests


def get_stock_index():
	"""Return requested KOSPI/KOSDAQ Index by scraping from KRX.co.kr"""

	headers = {"User-Agent": "Mozilla/5.0"}
	req = requests.get("http://www.krx.co.kr/main/main.jsp")
	html = req.text
	soup = BeautifulSoup(html, "html.parser")
	index = soup.findAll("span", {"class": "index-price"})

	
	kospi = index[1].get_text()
	kosdaq = index[3].get_text()

	return [kospi, kosdaq]
