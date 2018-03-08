from django.shortcuts import render
from django.http import HttpResponse

def buttons(request):
	return HttpResponse("안녕하세요 친구들!")
