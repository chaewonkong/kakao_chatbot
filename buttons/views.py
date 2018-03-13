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
from django.template import loader
import json


def index(request):
	template = loader.get_template('buttons/index.html')

	return HttpResponse(template.render())


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
	#price = get_stock_price(get_corp_code(request))

	if action == "코스피/코스닥 지수":
		return JsonResponse({
			'message': {
				'text':  '#KOSPI의 지수 입니다: \n\n    ' + index[0] + 
						'\n\n\n\n' +
						'#KOSDAQ의 지수 입니다: \n\n    ' + index[1]
				},
			'keyboard': {
				'type': 'buttons',
				'buttons': ["코스피/코스닥 지수", "종목 검색"]
				}
			})

	elif action == "종목 검색":
		return JsonResponse({
			'message': {
				'text': '검색하고자 하는 회사명을 입력하세요. \n\n띄어쓰기에 신경써주세요~ \nex) NAVER\nex) 삼성전자\nex) CJ CGV'
				}
			})

	else: # Post stock price and time to user
		post_stock_price(action)


def scraper(request):
	"""Delete existing DB and Create new DB"""
	index_db = Index.objects.all()
	index_db.delete()

	create_index('코스피', get_stock_index('코스피'))
	create_index('코스닥', get_stock_index('코스닥'))
	time.sleep(3)

	return HttpResponse("크롤링이 진행 중입니다~!!")


def corp_code_scraper():
	code_db = Code.objects.all()
	code_db.delete()

	create_code()



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
				corp_name = row[1],
				corp_code = row[0]
				)


def get_index():
	"""Return index of given market_name from DB"""

	kospi = Index.objects.get(market_name='코스피').index
	kosdaq = Index.objects.get(market_name='코스닥').index

	return [kospi, kosdaq]


def get_corp_code(request):
	"""Return corporation code of given corporation name"""

	request = request.upper()

	try:
		code = Code.objects.get(corp_name=request).corp_code
	
	except:
		return None
	
	else:
		return code


def get_corp_name(request):
	"""Return corporation name of given corporation code"""

	return Code.objects.get(corp_code=request).corp_name


def get_generated_time():
	"""Return time value when data generated"""
	
	date = list(time.localtime())

	if date[3] >= 15:
		return [date[1], date[2], 15, 0]
	elif date[3] < 9:
		return [date[1], date[2]-1, 15, 0]
	else:
		return date[1:5]


def post_stock_price(action):
	"""Post requested company's stock price as message to user"""

	if action.isdecimal():
		code = action
		action = get_corp_name(code)
	else:
		code = get_corp_code(action)
		action = action.upper()
		date = get_generated_time()
		
	if code:
		return JsonResponse({
			'message': {
					'text': action + '(' + code + ')' + '의 현재가(종가) 입니다:\n\n    ' 
							+ get_stock_price(code) + ' 원(KRW)\n'
							+ '    ({}월 {}일 {}시 {}분 기준)'.format(date[0], date[1], date[2], date[3])
							+ '\n\n\n 네이버금융에서 자세히 알아보기\n'
							+ 'http://finance.naver.com/item/main.nhn?code=' + code
					},
			'keyboard':{
					'type': 'buttons',
					'buttons': ["코스피/코스닥 지수", "종목 검색"]
					}
				})
	else:
		return JsonResponse({
			'message': {
					'text': '죄송합니다. 종목 찾기에 실패했습니다.' + 
							'\n\n종목명의 경우 한글/영어와 띄어쓰기를 구분합니다.\n다시 한번 검색해주세요~!!'
					}

				})


