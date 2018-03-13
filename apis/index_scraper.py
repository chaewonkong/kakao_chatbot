"""Stock Market Scraper

Scrape and return KOSPI and KOSDAQ INDEX of Korean Stock Market"""

from bs4 import BeautifulSoup
import requests

from django.http import HttpResponse
from django.db import models


class Index(models.Model):
	"""Store KOSPI and KOSDAQ Index to DB"""

	id = models.AutoField(primary_key=True)
	market_name = models.CharField(max_length=30, default="")
	index = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.index


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


# Index Scraping
def create_index(market_name, index):
	"""Create and save index with market_name in DB"""
	Index.objects.create(
		market_name = market_name,
		index = index
		)


def scraper():
	"""Delete existing DB and Create new DB"""
	index_db = Index.objects.all()
	index_db.delete()

	create_index('코스피', get_stock_index('코스피'))
	create_index('코스닥', get_stock_index('코스닥'))

# Run scraper
scraper()