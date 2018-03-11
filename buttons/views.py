# Web scraper
from apis.scraper import get_stock_index, get_stock_price
from bs4 import BeautifulSoup
import csv
import requests
import time

# Django App
from buttons.models import Index, Code
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
	action = json_data['content']
	index = get_index()

	if action == "코스피/코스닥 지수":
		return JsonResponse({
			'message': {
				'text':  '#KOSPI의 지수 입니다: \n\n' + index[0] + '\n\n-----------------------\n\n'
						'#KOSDAQ의 지수 입니다: \n\n' + index[1]
				},
			'keyboard': {
				'type': 'buttons',
				'buttons': ["코스피/코스닥 지수", "종목 검색"]
				}
			})

	elif action == "종목 검색":
		return JsonResponse({
			'message': {
				'text': '검색하고자 하는 회사명을 입력하세요'
				}
			})

	else: # Return specific stock price and keyboard to users
		return JsonResponse({
			'message': {
				'text': action + '의 현재가(종가) 입니다:\n\n' + index[0] + ' 원(KRW)'
				},
			'keyboard':{
				'type': 'buttons',
				'buttons': ["코스피/코스닥 지수", "종목 검색"]
				}
			})


def scraper(request):
	"""Delete existing DB and Create new DB"""
	index_db = Index.objects.all()
	code_db = Code.objects.all()
	index_db.delete()
	code_db.delete()

	create_index('코스피', get_stock_index('코스피'))
	create_index('코스닥', get_stock_index('코스닥'))
	create_code()
	time.sleep(3)

	return HttpResponse("크롤링이 진행 중입니다~!!")


def create_index(market_name, index):
	"""Create and save index with market_name in DB"""
	Index.objects.create(
		market_name = market_name,
		index = index
		)


def create_code():

	with open('apis/data.csv') as datafile:
		reader = csv.reader(datafile)

		for row in reader:
			Code.objects.create(
				corp_name = row[0],
				corp_code = row[1]
				)


def get_index():
	"""Return index of given market_name from DB"""

	kospi = Index.objects.get(market_name='코스피').index
	kosdaq = Index.objects.get(market_name='코스닥').index

	return [kospi, kosdaq]


def get_corp_code(request):
	"""Return corporation code of given corporation name"""

	code = Code.objects.get(corp_name=request).corp_code

	return code

