from django.http import JsonResponse
from django.shortcuts import render


def buttons(request):
	return JsonResponse({
		'type': 'buttons',
		'buttons': ["코스피", "코스닥"]
		})
