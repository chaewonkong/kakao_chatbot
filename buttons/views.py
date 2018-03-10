# Web scraper
from apis.scraper import get_stock_index
from bs4 import BeautifulSoup
import requests
import time

# Django App
from buttons.models import Index
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


def buttons(request):
	return JsonResponse({
		'type': 'buttons',
		'buttons': ["코스피/코스닥 지수", "종목 검색"],
		})


@csrf_exempt
def message(request):
	json_str = ((request.body).decode('utf-8'))
	json_data = json.loads(json_str)
	menu = json_data['content']
	index = get_index()

	if menu == "코스피/코스닥 지수":
		return JsonResponse({
			'message': {
				'text':  'KOSPI의 지수입니다: \n\n' + index[0] + '\n\nKOSDAQ의 지수입니다: \n\n' + index[1]
				},
			'keyboard': {
				'type': 'buttons',
				'buttons': ["코스피/코스닥 지수", "종목 검색"]
				}
			})
	else:
		return JsonResponse({
			'message': {
				'text': '검색하고자 하는 회사명을 입력하세요'
				}
			})


def scraper(request):
	"""Delete existing DB and Create new DB"""
	index_db = Index.objects.all()
	index_db.delete()

	create_index('코스피', get_stock_index('코스피'))
	create_index('코스닥', get_stock_index('코스닥'))
	time.sleep(3)

	return HttpResponse("크롤링이 진행 중입니다~!!")


def create_index(market_name, index):
	"""Create and save index with market_name in DB"""
	Index.objects.create(
		market_name = market_name,
		index = index
		)


def get_index():
	"""Return index of given market_name from DB"""

	kospi = Index.objects.get(market_name='코스피').index
	kosdaq = Index.objects.get(market_name='코스닥').index

	return [kospi, kosdaq]

