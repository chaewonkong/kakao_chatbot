# Web scraper
from apis.scraper import get_stock_index
from bs4 import BeautifulSoup
import requests

# Django App
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json


def buttons(request):
	return JsonResponse({
		'type': 'buttons',
		'buttons': ["코스피", "코스닥"],
		})


@csrf_exempt
def message(request):
	json_str = ((request.body).decode('utf-8'))
	json_data = json.loads(json_str)
	market_name = json_data['content']
	index = get_stock_index(market_name)


	return JsonResponse({
		'message': {
			'text': market_name + '의' + '지수입니다: \n\n' + index
			},
		'keyboard': {
			'type': 'buttons',
			'buttons': ["코스피", "코스닥"]
			}
		})